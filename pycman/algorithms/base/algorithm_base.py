"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import gym
import json
import os
import sys
from collections import namedtuple, defaultdict

from abc import abstractmethod
from pycman.algorithms.base.replay_memory import ReplayMemory
from pycman.core.gamecontrol.handlers.gym import HandlerGym
import pickle
import numpy as np


class AlgorithmBase(ReplayMemory):
    """Models an algorithm_base that would play the game by choosing an action based on the observation and prior data"""

    def __init__(self, game_name, save_folder, preprocessor, preprocessor_settings, session_name, algorithm,
                 algorithm_settings, compressor, can_train, session_restore, nr_evaluations, store_data, store_video,
                 # The constructor parameters above this line are also passed to ReplayMemory
                 training_condition, checkpoint_interval, player, gui):
        """
        Initializes the algorithm_base

        Parameters
        ----------
         game_name: string
            The name of the OpenAI gym environment.
         save_folder:
            The path where the database and the checkpoints will be saved.
         preprocessor: class
            The instance of the used preprocessor.
         preprocessor_settings: dict
            A dictionary containing all construction parameters for the preprocessor.rst.
         session_restore: bool
            A boolean describing whether the previous session should be restored.
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
         nr_evaluations: int
            The number of evaluation games between each epoch.
         training_condition: dict
            A dict containing nr_games, nr_steps, ram_used. When one is reached training will start.

        """

        # For rendering in the app
        if gui and player:
            self.__player = player
            self.__gui = gui

        # Checkpoint related
        self.__save_folder = save_folder
        self.__last_checkpoint_epoch = None
        self.__checkpoint_interval = checkpoint_interval

        # Restore previous session and checkpoint
        previous_session, restored = self._restore_session(save_folder, session_restore)

        # Initializes the ReplayMemory
        super().__init__(game_name, save_folder, preprocessor, preprocessor_settings, previous_session, session_name, algorithm,
                 algorithm_settings, compressor, store_data, store_video)

        # Settings required for the evaluations
        self.__nr_evaluations = nr_evaluations
        self.__evaluation_step_columns = ['step_id', 'evaluation_id', 'running_session_id', 'observation', 'reward',
                                          'done', 'info', 'action']
        self.__evaluation_step = namedtuple("evaluation_info", self.__evaluation_step_columns)
        self.__game_name = game_name
        self.__evaluation_game_id = 0

        # Settings for training
        self.__training_conditions = training_condition
        self.__can_train = can_train
        self.__store_data = store_data

        # These are now publicly available for usage
        # The size of an observation and the number of actions allowed
        self.state_size, self.action_space = self._get_gym_constants(game_name)

        # Restore the previous session
        if session_restore and restored:
            checkpoint_path = self.__save_folder + '\\Epoch_' + str(self._epoch)
            try:
                self._load_checkpoint(checkpoint_path)
                print("Successfully loaded checkpoint at epoch", self._epoch, "from:", checkpoint_path)
                self._epoch += 1
            except:
                raise("Error: Can not load checkpoint from path:", checkpoint_path)

        # Create an instance of the preprocessor.rst
        if preprocessor:
            if preprocessor_settings is None:
                self.__preprocessor = preprocessor()
            else:
                self.__preprocessor = preprocessor(**preprocessor_settings)
        else:
            print("Using preprocessor:", None)
            self.__preprocessor = type('', (), dict(preprocess=lambda x: x,
                                                   get_output_size=lambda: self.state_size))

        # Game reward counters for showing information in the console
        self.__game_rewards = []
        self.__game_reward = 0
        self.__action_distribution = defaultdict(int)

    def store_and_pick_action(self, game_info):
        """
            Performs all the underlying step based work. Also calls its implementation for _pick_action.

            Parameters
            ----------
            game_info: GameInfo
                Class containing information about the current state of the game

            Returns
            -------
            action: int
                The number of the picked action.

        """
        # This will make sure that the frame data is always stored before deciding on a new step.
        if self.__preprocessor is not None:
            game_info.gym.obs = self.__preprocessor.preprocess(game_info.gym.obs)

        self._add_training_frame(game_info)
        self.__game_reward += game_info.gym.reward
        if game_info.gym.done:
            self.__game_rewards.append(self.__game_reward)
            self.__game_reward = 0
            self._start_training_and_evaluation()
        action = self._pick_action(game_info.gym.obs)
        self.__action_distribution[action] += 1
        return action

    def switch_can_train(self):
        """
            Changes the state of the trainings flag

            Modifies
            --------
            can_train: bool
                A boolean describing whether this algorithm can be trained.

        """
        self.__can_train = not self.__can_train

    def get_can_train(self):
        """
            Gets the state of the trainings flag

            Returns
            -------
            can_train: bool
                A boolean describing whether this algorithm can be trained.

        """
        return self.__can_train

    def render_game_in_app(self, observation):
        """ Renders the game in the gui.  """
        self.__gui.render_game(self.__player, observation)

    def _evaluate(self):
        """ Evaluates the algorithm. Also prints the results to the console and SQL. """
        sys.stdout.write('\nEvaluating...')
        sys.stdout.flush()
        game_rewards = []
        env = gym.make(self.__game_name)
        actions = defaultdict(int)

        # Run each evaluation game
        for game_nr in range(self.__nr_evaluations):

            # (Re)set game parameters
            evaluation_step_id = 0
            game_reward = 0
            self.__evaluation_game_id += 1
            observation = env.reset()
            done = False

            # Run a game
            while not done:
                evaluation_step_id += 1
                if self.__preprocessor is not None:
                    processed_observation = self.__preprocessor.preprocess(observation)
                else:
                    processed_observation = observation
                action = self._pick_eval_action(processed_observation)
                observation, reward, done, info = env.step(action)
                actions[action] += 1
                game_reward += reward
                if info is None:
                    frame_info = self.__evaluation_step(evaluation_step_id,
                                                        self.__evaluation_game_id,
                                                        self._running_session_id,
                                                        observation,
                                                        reward,
                                                        done,
                                                        "-",
                                                        action)
                else:
                    frame_info = self.__evaluation_step(evaluation_step_id,
                                                        self.__evaluation_game_id,
                                                        self._running_session_id,
                                                        observation,
                                                        reward,
                                                        done,
                                                        json.dumps(info),
                                                        action)
                self._add_evaluation_frame(frame_info)

            # End of game. Add game reward for average and print results.
            game_rewards.append(game_reward)
            output = f"\r Evaluating..." \
                f" games: {game_nr + 1}/{self.__nr_evaluations} " \
                f" avg: {sum(game_rewards) // len(game_rewards)}"
            sys.stdout.write(output)
            sys.stdout.flush()

        # Make the display of the action distribution a bit nicer
        action_distribution = ", ".join([f"{k}: {v}" for k, v in sorted(actions.items())])

        # Add additional info about the action distribution
        output = f"\r Evaluation: " \
                 f" games: {game_nr + 1}/{self.__nr_evaluations} " \
                 f"\tavg: {round(sum(game_rewards) // len(game_rewards), 1)}" \
                 f"\tmin: {round(min(game_rewards), 1)} \tmax: {round(max(game_rewards), 1)}" \
                 f"\tstd: {round(np.std(game_rewards), 1)}" \
                 f"\taction distribution: {action_distribution}\n\n"
        sys.stdout.write(output)
        sys.stdout.flush()

    def _training_condition(self):
        """ Checks whether the algorithm is ready to train or to evaluate. Returns true if so. """
        info = self.get_info()
        output = f"\r Gathering training data... epoch: {info['epoch']}, " \
                 f" steps: {info['nr_steps']+1}/{self.__training_conditions['nr_steps']} " \
                 f" games: {info['nr_games']+1}/{self.__training_conditions['nr_games']} " \
                 f" ram: {info['ram_used']}% / {self.__training_conditions['ram_used']}%" \
                 f" avg: {sum(self.__game_rewards) // len(self.__game_rewards)}"

        sys.stdout.write(output)
        sys.stdout.flush()

        start_training = (info['nr_steps']+1 >= self.__training_conditions['nr_steps']) or \
               (info['nr_games'] + 1 >= self.__training_conditions['nr_games']) or \
               (info['ram_used'] >= self.__training_conditions['ram_used'])

        if start_training:
            # Make the display of the action distribution a bit nicer
            action_distribution = ", ".join([f"{k}: {v}" for k, v in sorted(self.__action_distribution.items())])
            output = f"\r Training:    epoch: {info['epoch']}, " \
                     f"\tavg: {round(sum(self.__game_rewards) // len(self.__game_rewards), 1)}" \
                     f"\tmin: {round(min(self.__game_rewards), 1)} \tmax: {round(max(self.__game_rewards), 1)}" \
                     f"\tstd: {round(np.std(self.__game_rewards), 1)}"\
                     f"\taction distribution: {action_distribution}"
            self.__action_distribution = defaultdict(int)
            sys.stdout.write(output)
            sys.stdout.flush()

        return start_training

    def _start_training_and_evaluation(self):
        """"" Starts the training and evaluation procedure if the algorithm is ready for it. """
        if self._training_condition():
            # Step 1: Training
            if self.__can_train:
                self._train(**self.get_training_data())

            # Step 2: Evaluation
            self._evaluate()

            # Step 3: Store results and checkpoint
            if self.__store_data:

                # Create checkpoint, flushing and resetting memory
                if self._epoch % self.__checkpoint_interval == 0:
                    checkpoint_path = self.__save_folder + '\\Epoch_' + str(self._epoch)
                    try:
                        os.mkdir(checkpoint_path)
                    except:
                        print('Warning: Path already exists: ', checkpoint_path)
                    self._store_checkpoint(checkpoint_path)
                    self.__last_checkpoint_epoch = self._epoch
                    print("New checkpoint created!")

                self._store_session()

            self._flush(increase_epoch=True)
            self.__game_rewards = []

    def _get_gym_constants(self, game_name):
        """"Receives info about the game environment """
        # Get some basic data from the game

        gym_env = HandlerGym(game_name)
        state_size = gym_env.obs.size
        action_space = gym_env.action_space
        return state_size, action_space

    def _store_session(self):
        with open(self.__save_folder + '/session.pycman', "wb") as handle:
            pickle.dump({'running_session_id': self._running_session_id,
                         'epoch': self._epoch,
                         'last_checkpoint_epoch': self.__last_checkpoint_epoch}, handle)

    def _restore_session(self, save_folder, session_restore):
        if os.path.isfile(save_folder+'/session.pycman') and session_restore:
            info = {}
            try:
                with open(save_folder+'/session.pycman', "rb") as handle:
                    info = pickle.load(handle)
            except:
                raise("Error reading session: " + save_folder + '/session.pycman')
            previous_session = info['running_session_id']
            try:
                self.__last_checkpoint_epoch = int(info['last_checkpoint_epoch'])
                self._epoch = self.__last_checkpoint_epoch
            except:
                return "None", False
            checkpoint_path = self.__save_folder + '\\Epoch_' + str(self._epoch)
            try:
                self._load_checkpoint(checkpoint_path)
            except:
                raise("Error loading algorithm checkpoint at: " + checkpoint_path)
            restored = True
        else:
            previous_session = "None"
            self.__last_checkpoint_epoch = None
            restored = False
        return previous_session, restored

    """ -------------------------------------------------------------------------------------------- """
    """ ---- All abstract methods are listed below. These should be overridden by the subclass. ---- """
    """ -------------------------------------------------------------------------------------------- """

    @abstractmethod
    def _store_checkpoint(self, save_folder):
        """ Store a checkpoint """
        pass

    @abstractmethod
    def _load_checkpoint(self, save_folder):
        """ Load an old checkpoint to continue training or retrieving a trained model"""
        pass

    @abstractmethod
    def _pick_action(self, observation):
        r"""
        Chooses an action based on observation

        Parameters
        ----------
        observation: ndarray
            Observation of the current game environment

        Returns
        -------
        action: int
            Number corresponding to the action that can be taken in the current game state (0 <= \result < n_actions)
        """

        pass

    @abstractmethod
    def _train(self, observations, metadata):
        """
        Make it possible for the algorithm_base to train

        Parameters
        ----------
        observations: list
            all the preprocessed observations in one list
        metadata: panda dataframe
            all the available trainings data, observations, reward, done, info and action taken.

        """
        pass

    @abstractmethod
    def _pick_eval_action(self, observation):
        r"""
        Chooses an action based on observation for the evaluation

        Parameters
        ----------
        observation: ndarray
            Observation of the current game environment

        Returns
        -------
        action: int
            Number corresponding to the action that can be taken in the current game state (0 <= \result < n_actions)
        """
        pass
