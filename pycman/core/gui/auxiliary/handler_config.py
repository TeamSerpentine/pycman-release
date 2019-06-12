"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import configparser
import os
import json

from pycman.core.gui.auxiliary import constants


class HandlerConfig:
    """
        Handles all calls to the configparser, updates the values and
        stores all the data to the disk. Restores values from string to booleans
        and integers. """
    def __init__(self, player_name):
        self._player_name = player_name

        self._save_path = ""
        self._default_path = self._set_default_path()

        self._config = configparser.ConfigParser()
        self.load_file_default()

    def _set_default_path(self):
        """ Returns the path to the config file (OS independent).  """
        file_path = os.path.realpath(__file__)
        path = self.create_closest_path_to_project(file_path, "core")
        path =  os.path.join(path, 'default_config.ini')
        if not os.path.exists(path):
            file_folder = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(file_folder, 'config.ini')
        return path

    def load_file(self, open_loc):
        """ Load a file from a new path.  """
        if not open_loc.endswith('.ini'):
            raise ValueError("Error path is not a '.ini' extension")

        self._config = configparser.ConfigParser()
        self._config.read(open_loc)

        if open_loc is not self._default_path:
            self._save_path = open_loc
        return self

    def load_file_default(self):
        """ Get the default config.ini file.  """
        self.load_file(self._default_path)
        return self

    def save_file(self, save_folder=""):
        if save_folder:
            self.change_config_value(constants.PLAYER_GAME, "save_folder", save_folder)
            self._save_path = os.path.join(save_folder, f"{self._player_name}.ini")

        self.check_save_path()
        with open(self._save_path, "w") as configfile:
            self._config.write(configfile)

        return self

    def get_config_value(self, section, key, data_type):
        """ Get a value from a specific section, and data type.  """
        if data_type == constants.STRING:
            return self._config.get(section, key)

        if data_type == constants.BOOLEAN:
            return self._config.getboolean(section, key,)

        if data_type is constants.INT:
            return self._config.getint(section, key)

        if data_type is constants.FIXED:
            return self._config.get(section, key)

        raise ValueError(f"Unknown data type: '{data_type}'")

    def get_config_values(self):
        """ Returns all the values as a dict, with ';' separators.  """
        info = dict()
        for section in self._check_get_section_to_return():
            for key, value in sorted(self._config.items(section)):
                key, value = self._check_special_type(section, key, value)

                # Skip empty entries
                if key == constants.EMPTY_SECTION:
                    continue

                info[f"{self._player_name};{section};{key}"] = value
        return info

    def get_config_values_section(self, section):
        """ Returns all the values as a dict, with ';' separators.  """
        info = dict()
        for key, value in sorted(self._config.items(section)):
            key, value = self._check_special_type(section, key, value)

            # Skip empty entries
            if key == constants.EMPTY_SECTION:
                continue

            info[f"{self._player_name};{section};{key}"] = value
        return info

    def get_config_values_per_section(self, return_all=False):
        """ Return the config values per section as dict values, with ';' separators.  """
        section_dict = dict()
        for section in self._check_get_section_to_return(return_all):
            # Create the section
            section_dict[section] = dict()

            # Add the key and values to the section
            for key, value in sorted(self._config.items(section)):
                key, value = self._check_special_type(section, key, value)
                section_dict[section][key] = value

            # If the section is empty, add an empty warning section
            if not section_dict[section]:
                section_dict[section][constants.EMPTY_SECTION] = "ADD VALUES IN CONFIG?"
        return section_dict

    def change_config_value(self, section, key, value):
        """ Changes the value in a specific section.  """

        # If the section, doesn't exists create it
        if section not in self._config.sections():
            self._config.add_section(section)

        # If the value is empty, it won't be changed
        if value:
            self._config.set(section, key, value)
        return self

    def reset_config_values(self):
        """ Clear all old values.  """
        self._config = configparser.ConfigParser()
        return self

    def _check_get_section_to_return(self, return_all=False):
        """ Return the correct sections depending on the player name.  """

        if return_all:
            return self._config.sections()

        if self._player_name == constants.PLAYER_GAME:
            # Only return the game settings
            section = [constants.PLAYER_GAME]

        else:
            section = self._config.sections()
            # Return everything but the game section
            if constants.PLAYER_GAME in section:
                del section[section.index(constants.PLAYER_GAME)]
        return section

    def _check_special_type(self, section, key, value):
        """ Checks if it has to return a booleans and integers instead of string.  """

        # All config settings are saved as string, here we can convert it back
        # to integers or booleans.
        if key in constants.SPECIAL_TYPES:
            value = self.get_config_value(section, key, constants.SPECIAL_TYPES[key])

        if key == "save_folder":
            _, path = self.check_save_path()
            value = path

        return key, value

    def check_save_path(self):
        """ Checks if the save path is well set.  """
        flag, save_folder = self.get_full_save_path()

        # This is the first time for saving, always ask where to save
        if not flag:
            return False, save_folder

        # If the path is not there, try to make it, otherwise give an alternative and ask
        if not os.path.exists(save_folder):
            try:
                os.makedirs(save_folder, exist_ok=True)
                return True, save_folder
            except OSError:
                save_folder_alternative = self.create_closest_path_to_project()
                return False, save_folder_alternative

        return True, save_folder

    @staticmethod
    def create_closest_path_to_project(path="", name="pycman"):
        """ Alternative path at the top of the base folder. """
        if not path:
            path = __file__

        tail, head = "", path
        if name in head:
            while not tail == name:
                head, tail = os.path.split(head)
        return head

    def get_full_save_path(self):
        """ Replaces all placeholders by real values and join all paths.  """

        # Get the section default values
        section = constants.PLAYER_GAME
        game_name = self.get_config_value(section, "game_name", constants.STRING)
        session_name = self.get_config_value(section, "session_name", constants.STRING)
        save_folder = self.get_config_value(section, "save_folder", constants.STRING)

        # If you are saving for the first time, ask where to store, but give default save path
        if save_folder == "data":
            save_folder = os.path.join(save_folder, "Serpentine", game_name, session_name)
            return False, save_folder

        # Create an os path and replace the place holder with the actual game name
        if "Serpentine" in save_folder:
            save_folder = self.create_closest_path_to_project(save_folder, "Serpentine")
        save_folder = os.path.join(save_folder, "Serpentine", game_name, session_name)
        return True, save_folder

    def create_export_code(self):
        """ Returns importable code for the controller.  """

        # Store all the values per section as dict
        section_dict = self.get_config_values_per_section(return_all=True)

        # For general purposes in Human and AI players
        game_name = section_dict[constants.PLAYER_GAME]['game_name']
        save_folder = section_dict[constants.PLAYER_GAME]['save_folder']

        # Returns all the game settings that are necessary for the controller
        if self._player_name == constants.PLAYER_GAME:
            value_dicts = section_dict[constants.PLAYER_GAME]
            return value_dicts

        # Returns the initialization of a human.rst player
        if constants.PLAYER_HUMAN in self._player_name:
            save_highscores = section_dict[self._player_name]['save_highscores']
            return{"HumanAlgorithm": dict(game_name=game_name,
                                          save_folder=save_folder,
                                          save_highscores=save_highscores,
                                          player=self._player_name,
                                          gui=None)}

        if constants.PLAYER_AI in self._player_name:

            # Take the algorithm name out of the section and delete it from the dict
            algorithm_name = section_dict['Algorithm']['algorithm_name']
            del section_dict['Algorithm']['algorithm_name']

            algorithm = section_dict['Algorithm']

            # Put all preprocessor.rst settings from the config in a dictionary
            preprocessor_settings = {}
            for key, value in section_dict['PreprocessorSettings'].items():
                if key != constants.EMPTY_SECTION:
                    preprocessor_settings[key] = value

            # Put all algorithm settings from the config in a dictionary
            algorithm_settings = {}
            for key, value in section_dict['AlgorithmSettings'].items():
                if key != constants.EMPTY_SECTION:
                    algorithm_settings[key] = value

            # The settings for the algorithm base class.
            # These are all the constructor parameters wrapped up.
            training_condition = dict(nr_steps=float(algorithm['condition_nr_steps']),
                                      nr_games=int(algorithm['condition_nr_games']),
                                      ram_used=int(algorithm['condition_ram_used']))

            algorithm_base_settings = dict(game_name=game_name,
                                           save_folder=save_folder,
                                           preprocessor=algorithm['preprocessor'],
                                           preprocessor_settings=preprocessor_settings,
                                           session_name=section_dict['GAME']['session_name'],
                                           algorithm=algorithm_name,
                                           algorithm_settings=algorithm_settings,
                                           compressor=section_dict['GAME']['compressor'],
                                           can_train=algorithm['can_train'],
                                           session_restore=algorithm['session_restore'],
                                           nr_evaluations=int(algorithm['nr_evaluations']),
                                           training_condition=training_condition,
                                           store_data=section_dict['GAME']['store_data'],
                                           checkpoint_interval=int(section_dict['GAME']['checkpoint_interval']),
                                           player=self._player_name,
                                           gui=None,
                                           store_video=section_dict['GAME']['store_video'])

            return {algorithm_name: dict(settings=algorithm_base_settings,
                                         **algorithm_settings,
                                         )}


if __name__ == "__main__":
    pass
