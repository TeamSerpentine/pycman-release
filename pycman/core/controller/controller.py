"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import os
import sys

from importlib import import_module
from pycman.core.gamecontrol.game_controller import GameInterface

# The algorithm_base Names that you can use, to initiate an algorithm_base
# Don't forget to add your own algorithm_base here and in the algorithm_base folder
from pycman.algorithms.algorithm_human import HumanAlgorithm
from pycman.algorithms.algorithm_random import RandomAlgorithm

from pycman.preprocessors.preprocessor_hackaday import PreProcessor


class Controller(object):
    """
    An integration between the Game Interface, Algorithm, Temporal Memory and Persistent Storage.

    It can play games and store all data in a database, and continue from a previous point.
    """

    def __init__(self, game_name, save_folder, render, fps, players, gui=None, **kwargs):
        """
            Constructor

            Parameters
            ----------
            game_name: string
                Tha atari game that you want to play

            save_folder: string
                Saving folder for all the data

            render: bool
                If True will render the game

            fps: int
                Controls the frames per seconds that are rendered

            players: dict(dict())
                Gives a player with an algorithm_base and all the variables neccesarry
                to initialize the algorithm_base, only the variables 'player' and 'gui'
                will be filled in later by this class

            gui: class gui
                If passed the game will be rendered inside the gui

            **kwargs:
                To handle extra parameters added to controller
        """

        # Check if the folder exists, and otherwise try to create it
        self._check_save_path(save_folder)
        print("Storing data at:", save_folder)

        # Initializing the players algorithm_base, the algorithm_base have to be imported in this file
        player_details = self._get_players_algorithm(players, gui)

        # Create the GameInterface, every player gets its own
        # 'gym' handler, 'counters' handler and 'algorithm_base' handler
        self._game = GameInterface(game_name, player_details)

        # Start the game loop
        self._game.play_game(render, fps, gui)

    @staticmethod
    def _check_save_path(save_path):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        return save_path

    def _get_players_algorithm(self, players, gui=None):
        player_details = dict()
        for player, algorithm in players.items():
            algorithm_init = None
            for algorithm_name, algorithm_kwargs in algorithm.items():

                # Replace the gui with the real gui interface
                if algorithm_kwargs.get("gui", False) is not False:
                    algorithm_kwargs['gui'] = gui
                elif algorithm_kwargs.get("settings", False) is not False:
                    algorithm_kwargs['settings']['gui'] = gui
                else:
                    algorithm_kwargs['gui'] = None
                    algorithm_kwargs['player'] = player

                algorithm_instance = self._find_algorithm_in_this_module(algorithm_name)
                algorithm_init = algorithm_instance(**algorithm_kwargs)
            player_details[player] = algorithm_init

        return player_details

    def _find_algorithm_in_this_module(self, algorithm_name):
        for each in sys.modules:
            if "pycman.algorithms" in each:
                module = import_module(each)
                if getattr(module, algorithm_name, None):
                    return getattr(module, algorithm_name)
        raise ValueError("The algorithm_base couldn't be found, please make sure that it is located in the algorithm_base folder \n"
                         "and imported in this file, otherwise it cannot be detected automatically.")
