"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import glob
import os
import importlib

from pycman.core.gamecontrol.game_controller import GameInterface


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

            # Get the (only) item from the dictionary and split it in name and arguments
            algorithm_name = next(iter(algorithm))
            algorithm_kwargs = algorithm[algorithm_name]

            # Settings the gui
            algorithm_kwargs = self._set_gui_in_settings(algorithm_kwargs, player, gui)

            # Give along the instance of the preprocessor
            algorithm_kwargs = self._set_preprocessor_in_settings(algorithm_kwargs)

            # Initialize the algorithm
            algorithm_instance = self._find_algorithm_instance(algorithm_name)
            algorithm_init = algorithm_instance(**algorithm_kwargs)

            player_details[player] = algorithm_init

        return player_details

    def _set_gui_in_settings(self, algorithm_kwargs, player, gui):
        """ Replace the gui with the real gui interface.  """
        if algorithm_kwargs.get("gui", False) is not False:
            algorithm_kwargs['gui'] = gui
        elif algorithm_kwargs.get("settings", False) is not False:
            algorithm_kwargs['settings']['gui'] = gui
        else:
            algorithm_kwargs['gui'] = None
            algorithm_kwargs['player'] = player
        return algorithm_kwargs

    def _set_preprocessor_in_settings(self, algorithm_kwargs):
        """ Returns a preprocessor instance from the preprocessors folder.  """
        if algorithm_kwargs.get("settings", False) is not False:
            preprocessor_name = algorithm_kwargs['settings']['preprocessor']
            preprocessor_instance = self._find_preprocessor_instance(preprocessor_name)
            algorithm_kwargs['settings']['preprocessor'] = preprocessor_instance
        return algorithm_kwargs

    def _find_algorithm_instance(self, algorithm_name):
        """ Returns an algorithm instance from the algorithm folder.  """
        algorithms_dict = self._find_list_of_algorithms_preprocessor("algorithms", [])
        if algorithms_dict.get(algorithm_name, None):
            return algorithms_dict[algorithm_name]

        algorithms_found = "\n ".join(algorithms_dict)
        raise ValueError("Unable to find your algorithm, here is a list"
                         f"of the algorithms we could find: \n {algorithms_found}")

    def _find_preprocessor_instance(self, preprocessor_name):
        """ Returns a preprocessor instance from the preprocessors folder.  """
        preprocessor_dict = self._find_list_of_algorithms_preprocessor("preprocessors", [])
        if preprocessor_dict.get(preprocessor_name, False) is not False:
            return preprocessor_dict[preprocessor_name]

        preprocessor_found = "\n ".join(preprocessor_dict)
        raise ValueError("Unable to find your preprocessor, here is a list"
                         f"of the preprocessors we could find: \n {preprocessor_found}")

    def _find_list_of_algorithms_preprocessor(self, folder, filter_list):
        algorithm_dict = dict()

        # Find the full path to the (lowest) pycman folder
        tail, head = "", os.path.abspath(__file__)
        while not tail == "core":
            head, tail = os.path.split(head)

        # Go into algorithms and select everything not starting with '__'
        # and has the extension '.py'
        python_files = glob.glob(f"{head}/{folder}/[!__]*.py")

        # Load the module from the full path name
        for path in python_files:
            loaded_module = self._load_module_from_full_path_string(path)
            classes = self._load_all_classes_in_a_module(loaded_module, filter_list)
            if classes:
                algorithm_dict = dict(**algorithm_dict, **classes)

        return algorithm_dict

    def _load_module_from_full_path_string(self, full_path):
        """ Get a module from a full path name to the module.  """
        spec = importlib.util.spec_from_file_location("module.name", full_path)
        loaded_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded_module)
        return loaded_module

    def _load_all_classes_in_a_module(self, module, filters_list):
        """ Returns all the classes and ignores import statements.  """
        classes = dict()
        for name, object in module.__dict__.items():
            # Check for classes
            if isinstance(object, type):
                # Ignore imported classes, so check for module name
                if object.__module__ == module.__name__:
                    # Ignore the base class algorithms
                    if name not in filters_list:
                        classes[name] = object
        return classes