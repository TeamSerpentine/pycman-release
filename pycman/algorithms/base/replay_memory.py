"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

from abc import ABC

import json
import pandas as pd
import psutil

from collections import namedtuple
from pycman.algorithms.base.persistent_storage import PersistentStorage
from pycman.algorithms.base.algorithm_compressor import DataIO
from uuid import uuid4
import os
import pickle


class ReplayMemory(ABC):

    def __init__(self, game_name, save_folder, preprocessor, preprocessor_settings, previous_session, session_name,
                 algorithm, algorithm_settings, compressor, store_data, store_video):
        """
             Constructor

             Parameters
             ----------
             game_name: string
                The name of the OpenAI gym environment.
             save_folder:
                The path where the database and the checkpoints will be saved.
             preprocessor: string
                The name of the used preprocessor.
             preprocessor_settings: dict
                A dictionary containing all construction parameters for the preprocessor.
             previous_session: string
                A string describing the running_session_id of the previous session. Is None if nothing is loaded.
             session_name: string
                Name for the session. Results are stored in this folder.
             algorithm: string
                Class name of the algorithm class.
             algorithm_settings: dict
                A dictionary containing all construction parameters for the algorithm.
             compressor: string
                A string containing the name of the compressor used to compress frames.
             can_train: bool
                Is the model able to train, or should it just show how it is doing.
             store_data: bool
                Whether to store any data on the disk.
             store_video: bool
                Whether to store evaluation videos on the disk.
        """

        # Dataframe column names for step based entities
        self.__evaluation_step_columns = ['step_id', 'evaluation_id', 'running_session_id', 'observation', 'reward', 'done', 'info', 'action']
        self.__training_step_columns = ['step_id', 'game_id', 'running_session_id', 'reward', 'done', 'info', 'action']

        # Namedtuple initialization
        self.__evaluation_step = namedtuple("evaluation_info", self.__evaluation_step_columns)
        self.__training_step = namedtuple("training_info", self.__training_step_columns)

        # Counters
        self._running_session_id = str(uuid4())
        self.__game_number = -1
        self.__nr_games = 0

        self._reset_frames()
        self.__store_video = store_video
        self.__store_data = store_data

        if self.__store_data:
            # Initializes the Persistent Storage, and make the path game_name dependent
            self.__persistent_storage = PersistentStorage(
                    # Predefined processor, can be set to None if not applicable
                    compressor=DataIO(),
                    # Replace the placeholder 'game name' with the actual game_name
                    save_folder=save_folder)

        # Flag whether the data is already compiled. Makes sure users always receive compiled dataframes.
        self.__data_is_compiled = False
        self.__save_folder = save_folder

        # Display whether continuing or restoring. Also set epoch in case of restarting
        if previous_session == 'None':
            print("Started a new session with ID:", self._running_session_id)
            self._epoch = 1  # Epoch counter
        else:
            print("Successfully loaded session with ID:", previous_session,
                  " Continuing with ID:", self._running_session_id)


        self.__dataframe_running_session = pd.DataFrame({
            "running_session_id": self._running_session_id,
            "session_name": session_name,
            "previous_session": previous_session,
            "algorithm_name": algorithm,
            "algorithm_config_file": json.dumps(algorithm_settings),
            "compressor_name": compressor,
            "preprocessor_name": preprocessor,
            "preprocessor_config_file": json.dumps(preprocessor_settings),
            "hardware": "TO DO: hardware",      # TODO:
            "game_name": game_name,
            "platform": "TO DO: platform",      # TODO:
            "user": "TO DO: user",
            "algorithm_field_1_name": "TO DO: From settings: field1",   # TODO:
            "algorithm_field_2_name": "TO DO: From settings: field2",   # TODO:
            "algorithm_field_3_name": "TO DO: From settings: field3"    # TODO:
        }, index=[0])

    def _reset_frames(self):
        # Fast appending lists for adding frames.
        self.__list_evaluation_step = []
        self.__list_training_step = []
        self.__list_preprocessed_observations = []

        # All dataframe variables. Most will be compiled before accessing data getter.
        self.__dataframe_evaluation_step = None
        self.__dataframe_training_step = None
        self.__dataframe_evaluation_game = None
        self.__dataframe_training_game = None
        self.__dataframe_epoch = None

    def get_info(self):
        """
            Receive info about the state of the ReplayMemory (e.g. number of games and used ram)

            Returns
            -------
            Dict with fields nr_games, nr_steps, ram_used and epoch
        """
        return {"nr_steps": len(self.__list_preprocessed_observations),
                "nr_games": self.__nr_games,
                "ram_used": psutil.virtual_memory().percent,  # Percentage of virtual ram usage (0-100)
                "epoch": self._epoch
                }

    def get_training_data(self):
        """
        Acts as a getter for the internal data of the ReplayMemory for the Algorithm class. Treat as read-only.

        Returns
        -------
        list
            A list containing all preprocessed observations required for training.
        panda dataframe
            Passes a reference to the training step dataframe.
        """
        if not self.__data_is_compiled:
            self._compile_data()

        return dict(observations=self.__list_preprocessed_observations, metadata=self.__dataframe_training_step)

    def get_all_data(self):
        """
           Acts as a getter for the internal data of the ReplayMemory for the Agent class. Treat as read-only.

           Returns
           -------
           all data: dict
               Passes a reference to the panda dataframes of the ReplayMemory
               giving reading capabilities to the Algorithm
        """
        if not self.__data_is_compiled:
            self._compile_data()

        return {'evaluation_step_data':     self.__dataframe_evaluation_step,
                'evaluation_game_data':     self.__dataframe_evaluation_game,
                'training_step_data':       self.__dataframe_training_step,
                'training_game_data':       self.__dataframe_training_game,
                'epoch_data':               self.__dataframe_epoch,
                'running_session_data':     self.__dataframe_running_session}

    def _flush(self, increase_epoch=True):
        """
           Removes all the data from the ReplayMemory. Also increases epoch by one.

           Parameters
           ----------
           checkpoint_path: string
                The path that contains the algorithm checkpoint
           increase_epoch=True: bool
               Determines whether the epoch should be increased, default is true.

           Returns
           -------
           running session data: panda dataframe
                Returns the data that can be used to restore a session

           """

        if self.__store_data:

            # If not compiled, compile
            if not self.__data_is_compiled:
                self._compile_data()

            # Get the data from TemporalMemory and store it in the PersistentStorage
            self.__persistent_storage.store(self.get_all_data())

        # Set all the dataframes to 0, and empty all the lists.
        self._reset_frames()

        # Reset counters
        self._game_number = 0
        self.__nr_games = 0
        if increase_epoch:
            self._epoch += 1

    def _add_training_frame(self, frame_info):
        """
            Add a frame to training data

            Parameters
            ----------
            frame_info: GameInterface Player class
                Stores handlers for 'gym', 'counters', 'algorithm_base'.
                all the information from the environment (obs, reward, done, info)
                all the counters, partially from the environment (step, game)
                the algorithm_base of that player (not used here)
            """
        frame_info_converted = self._convert_training(frame_info)
        if frame_info_converted.game_id != self.__game_number:
            self.__nr_games += 1
            self.__game_number = frame_info_converted.game_id

        self.__list_training_step.append(frame_info_converted)
        self.__list_preprocessed_observations.append(frame_info.gym.obs)

        # Data is no longer correctly compiled when a new frame is added.
        if self.__data_is_compiled:
            self._data_is_compiled = False

    def _add_evaluation_frame(self, frame_info):
        """
            Add a frame to evaluation data

            Parameters
            ----------
            frame_info: namedtuple
                all the information from the environment (obs, reward, done, info)
                with the step, game id and time.

            """
        if not self.__store_video:
            frame_info = self._convert_evaluation(frame_info)
        self.__list_evaluation_step.append(frame_info)

        # Data is no longer correctly compiled when a new frame is added.
        if self.__data_is_compiled:
            self.__data_is_compiled = False

    def _compile_data(self):
        """
            Converts all the rapid appending lists to dataframes.

            Modifies
            --------
            self._data_is_compiled = True
        """
        self.__dataframe_evaluation_step = \
            pd.DataFrame(self.__list_evaluation_step, columns=self.__evaluation_step_columns)
        self.__dataframe_training_step = \
            pd.DataFrame(self.__list_training_step, columns=self.__training_step_columns)

        grouped_training = self.__dataframe_training_step.groupby(['game_id'])
        action_training_distributions = []
        for name, group in grouped_training['action']:
            action_training_distributions.append(group.value_counts().to_string().replace('\n', '; '))

        self.__dataframe_training_game = pd.DataFrame(
                    {'game_id': list(grouped_training.groups.keys()),
                     'epoch': [self._epoch]*len(grouped_training),
                     'running_session_id': [self._running_session_id]*len(grouped_training),
                     'reward_sum': grouped_training['reward'].sum(),
                     'step_count': grouped_training['step_id'].count(),
                     'actions': action_training_distributions,
                    })

        grouped_evaluation = self.__dataframe_evaluation_step.groupby(['evaluation_id'])
        action_evaluation_distribution = []
        for name, group in grouped_evaluation['action']:
            action_evaluation_distribution.append(group.value_counts().to_string().replace('\n', '; '))
        self.__dataframe_evaluation_game = pd.DataFrame({
            'evaluation_id': list(grouped_evaluation.groups.keys()),
            'epoch': [self._epoch]*len(grouped_evaluation),
            'running_session_id': [self._running_session_id]*len(grouped_evaluation),
            'reward_sum': grouped_evaluation['reward'].sum(),
            'step_count': grouped_evaluation['step_id'].count(),
            'actions': action_evaluation_distribution
            })

        self.__dataframe_epoch = pd.DataFrame({
            'running_session_id': self._running_session_id,
            'epoch': self._epoch,
            'training_episode_count': len(self.__dataframe_training_game),
            'training_step_count': len(self.__dataframe_training_step),
            'training_time': 0,
            'training_average_reward': self.__dataframe_training_game['reward_sum'].mean(),
            'training_actions': self.__dataframe_training_step['action'].value_counts().to_string().replace('\n', '; '),
            'training_average_steps': self.__dataframe_training_game['step_count'].mean(),
            'evaluation_average_reward': self.__dataframe_evaluation_game['reward_sum'].mean(),
            'evaluation_actions': self.__dataframe_evaluation_step['action'].value_counts().to_string().replace('\n', '; '),
            'evaluation_average_steps': self.__dataframe_evaluation_game['step_count'].mean(),
            'algorithm_field_1_value': 0,
            'algorithm_field_2_value': 0,
            'algorithm_field_3_value': 0,
        }, index=[0])

        self._data_is_compiled = True

    # TODO: REMOVE OR CHANGE
    def _convert_training(self, game_info):
        """"Converts the current game_info tuple to something useful"""

        frame_info = self.__training_step(game_info.counters.step_id,
                                          game_info.counters.game_id,
                                          self._running_session_id,
                                          game_info.gym.reward,
                                          game_info.gym.done,
                                          "-",
                                          game_info.gym.action_old)
        if game_info.gym.info is None:
            frame_info = frame_info._replace("observation", json.dumps(game_info.gym.info))
        return frame_info

    def _convert_evaluation(self, game_info):
        """"Converts the current game_info tuple to something useful"""
        if game_info.info is None:
            frame_info = self.__evaluation_step(game_info.step_id,
                                                game_info.evaluation_id,
                                                self._running_session_id,
                                                "None",
                                                game_info.reward,
                                                game_info.done,
                                                "-",
                                                game_info.action)
        else:
            frame_info = self.__evaluation_step(game_info.step_id,
                                                game_info.evaluation_id,
                                                self._running_session_id,
                                                "None",
                                                game_info.reward,
                                                game_info.done,
                                                json.dumps(game_info.info),
                                                game_info.action)
        return frame_info
