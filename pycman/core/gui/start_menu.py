"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import glob
import importlib.util
import os
import sys

from appJar import gui

from pycman.core.controller.controller import Controller
from pycman.core.gui.auxiliary import constants, os_specific
from pycman.core.gui.auxiliary.handler_players import HandlerPlayers
from pycman.core.gui.auxiliary.handler_game_gui import GameGUI


class Layout:
    def __init__(self):
        self._os_name = sys.platform
        self._os_class = None
        self._players = HandlerPlayers()
        self._player_selected = None

        self._active_tooltips = []
        self._remove_tooltips = False

    def __enter__(self):
        with gui(constants.GUI_NAME, constants.SCREEN_SIZE) as self._app:

            # Global settings in the app
            self.create_global_app_features()

            # Create the layout
            self.create_layout_begin()
            self.create_layout_ending()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _find_operating_system(self):
        """ Returns a class which contains OS specific functions.  """
        platform = self._os_name
        if platform == 'win32' or platform == 'cygwin':
            return os_specific.Windows()
        if platform == 'linux':
            return os_specific.Linux()
        if platform == 'darwin':
            return os_specific.Darwin()
        return self

    def _find_path_pictures(self):
        path_pycman = os.path.dirname(os.path.dirname(__file__))
        path_images = os.path.join(path_pycman, "images", self._os_class.__class__.__name__.lower())
        return os.path.join(path_images, "logos")

    def _find_list_of_algorithms_preprocessor(self, folder):
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
            filter = getattr(constants, f"FILTER_{folder.upper()}", [])
            classes = self._load_all_classes_in_a_module(loaded_module, filter)
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

    def _print_msg_box(self, msg):
        self._app.infoBox("Info", msg)

    def create_global_app_features(self):
        self._app.setPadding(constants.PADDING)  # padding outside the widget
        self._app.setInPadding(constants.INPADDING)  # padding inside the widget
        self._os_class = self._find_operating_system()  # OS dependent functions

        self._app.addMenuList("File", constants.MENU_FILE, self._menu_files_options)
        return self

    def create_layout_begin(self):
        """ Create the start screen layout.  """
        self._app.addButtons(constants.BUTTONS_HOME_MENU, self._buttons_home_menu, colspan=constants.CENTERED)
        self._add_tooltips_buttons("HOME_MENU")
        path_icon, path_logo = self._os_class.set_logos(self._find_path_pictures())

        if path_icon:
            self._app.setIcon(path_icon)

        if path_logo:
            self._app.addImage("Logo", str(path_logo), colspan=constants.CENTERED)

        return self

    def create_layout_ending(self):
        row = self._app.getRow()
        self._app.addWebLink("www.serpentineai.nl", "http://serpentineai.nl", row=row, column=0)
        self._app.addLabel("team-pycman@serpentineai.nl", row=row, column=1)
        self._app.addLabel("© Copyright 2019, Serpentine", colspan=constants.CENTERED)
        return self

    def create_layout_game(self):
        """ Creates the layout for the game information.  """
        self._create_layout_frame(ids=constants.PLAYER_GAME,
                                  section=constants.PLAYER_GAME,
                                  config=self._players[constants.PLAYER_GAME].get_config_values())
        return self

    def _create_layout_frame(self, ids, section, config):
        # Creates a container per section
        with self._app.frame(f"{ids};{section}", colspan=constants.CENTERED):
            self._app.addLabel(title=f"{section}", text=section, colspan=constants.CENTERED)
            with self._app.frame(f"{section} LEFT", row=1, column=0, bg="Black", fg="White", stretch='ROW'):
                for key, value in sorted(config.items()):
                    self._app.addLabel(title=f"{ids};{section};{key}", text=key)
                    self._app.setLabelAlign(f"{ids};{section};{key}", "left")
                    self._add_tooltips(f"{ids};{section};{key}")

            with self._app.frame(f"{section} RIGHT", row=1, column=1, colspan=2):
                for key, value in sorted(config.items()):
                    self._create_layout_entries(ids, section, key, value)
        return self

    def _create_layout_entries(self, ids, section, key, value):
        if constants.SPECIAL_TYPES.get(key, None):
            if constants.SPECIAL_TYPES[key] == constants.BOOLEAN:
                self._app.addOptionBox(f"{ids};{section};{key}", constants.BUTTONS_BOOLEAN)
                self._app.setOptionBox(f"{ids};{section};{key}", str(value))
                return self

            if constants.SPECIAL_TYPES[key] == constants.FIXED:
                if key == "keys":
                    key_names = getattr(constants, value)
                    value = key_names

                self._app.addLabel(title=f"{ids};{section};{value}", text=value)
                self._add_tooltips(f"{ids};{section};{value}")
                return self

        if key == "algorithm_name" or key == "preprocessor":
            folder = "algorithms" if key == "algorithm_name" else "preprocessors"
            algorithms_dict = self._find_list_of_algorithms_preprocessor(folder=folder)
            if value in algorithms_dict:
                # Create the drop down menu
                self._create_layout_option_box_algorithm_name(ids, section, key, list(algorithms_dict), value)
                return self
            else:
                # Notify that the algorithm cannot be found
                self._app.addValidationEntry(title=f"{ids};{section};{key}")
                self._app.setEntryDefault(f"{ids};{section};{key}", value)
                self._app.setEntryInvalid(f"{ids};{section};{key}")
                return self

        self._app.addEntry(title=f"{ids};{section};{key}")
        self._app.setEntryDefault(f"{ids};{section};{key}", value)
        return self

    def _create_layout_option_box_algorithm_name(self, ids, section, key, algorithms_list, value):
        self._app.addOptionBox(f"{ids};{section};{key}", algorithms_list)
        self._app.setOptionBox(f"{ids};{section};{key}", index=algorithms_list.index(value))
        return self

    def _create_layout_player_settings(self, player_name):
        self.clear_layout()
        self._app.addButtons(constants.BUTTONS_PLAYER, self._buttons_players, colspan=constants.CENTERED)
        self._add_tooltips_buttons("PLAYER")
        self._app.addLabel(title=f" {player_name} ", colspan=constants.CENTERED)

        section_dict = self._players.get_player_config(player_name, per_section=True)
        for section, config in section_dict.items():
            self._create_layout_frame(player_name, section, config)

        self.create_layout_ending()
        self._player_selected = player_name
        return self

    def clear_layout(self):
        """ Remove all the fields and then add the begin layout with buttons.  """
        self._app.removeAllWidgets()
        self._active_tooltips = []
        self.create_layout_begin()
        return self

    def bind_unbind_keys(self, player, bind=True):
        mapping = dict(HUMAN_1=constants.KEYS_HUMAN_1,
                       HUMAN_2=constants.KEYS_HUMAN_2)
        if bind:
            self._app.bindKeys(mapping[player], self._buttons_players)
            return self

        self._app.unbindKeys(mapping[player])
        return self

    def _buttons_home_menu(self, btn):
        mapping = {
            "ADD AI": (self._button_home_menu_add_player, dict(player_type="AI")),
            "ADD HUMAN": (self._button_home_menu_add_player, dict(player_type="HUMAN")),
            "SAVE": (self._buttons_home_menu_save, dict()),
            "LOAD AI": (self._button_home_menu_load_ai, dict()),
            "RESET": (self._button_home_menu_reset, dict())
        }
        function, kwargs = mapping.get(btn, (None, None))
        function(**kwargs)
        return self

    def _button_home_menu_add_player(self, player_type):
        """ Add a player, depending on the type.  """

        # If the maximum players have been reached give a message
        number_of_players = len(self._players)
        if number_of_players >= constants.LIMIT_PLAYER_TOTAL:
            self._print_msg_box(f"Reached player limit of {constants.LIMIT_PLAYER_TOTAL}")
            return self

        # If the maximum of the player type has been reached give an error
        number_of_player_type = len(getattr(self._players, player_type.lower()))
        limit_player_type = getattr(constants, f"LIMIT_PLAYER_{player_type}")
        if number_of_player_type >= limit_player_type:
            self._print_msg_box(f"Reached maximum number of {player_type} players")
            return self

        # Create the new player and print it to the screen
        new_player_name = self._players.add_player(player_type)
        self._player_selected = new_player_name
        self.refresh()
        return self

    def _buttons_home_menu_save(self):
        """ Save the current ai and the settings to the disk.  """
        # Ignore if there are no players
        if not self._players.get_players():
            self._print_msg_box("Unable to save, no players found")
            return False

        if not self._save_player_settings():
            self._print_msg_box("Unable to save, cancelled action")
            return False

        return self

    def _button_home_menu_load_ai(self):
        """ Load an AI from an existing .ini file.  """
        open_loc = self._app.openBox()
        if open_loc and open_loc.endswith(".ini"):
            self._button_home_menu_add_player("AI")
            self._players.load_config_from_ai(self._player_selected, open_loc)
            self.refresh()
        return self

    def _button_home_menu_reset(self):
        self.clear_layout()
        self.create_layout_ending()
        self._players = HandlerPlayers()
        return self

    def _buttons_players(self, btn):
        mapping = {
            "DELETE PLAYER": self._buttons_players_delete_player,
            "GAME SETTINGS": self._buttons_players_controller_settings,
            "RUN GAME": self._buttons_players_run_game,
            "SWITCH/SHOW PLAYER": self._button_players_switch_show_player,
            "ADD PARAMETER": self._button_players_add_parameter,
        }
        return mapping.get(btn, None)()

    def _buttons_players_delete_player(self):
        """ Delete a player and updates the screen.  """

        # Delete the player and select the next player
        self._players.del_player(self._player_selected)
        self._player_selected = self._players.get_player_next()

        # Restore the layout to the home menu
        self.clear_layout()
        self.create_layout_ending()

        # If there is a new player to select, print his settings to the screen
        if self._player_selected is not None:
            self.refresh()
        return self

    def _buttons_players_controller_settings(self):
        """ Show the game settings.  """

        # Before switching store all values in case of changed parameters
        self._update_player_settings()

        # Change the player selected
        self._player_selected = constants.PLAYER_GAME
        self.refresh()
        return self

    def _buttons_players_run_game(self):

        # If you cancelled the saving, abort
        if not self._buttons_home_menu_save():
            return False

        # Retrieve the render settings
        game_settings = self._players.get_player_config(constants.PLAYER_GAME)
        render_settings = game_settings[f"{constants.PLAYER_GAME};{constants.PLAYER_GAME};render"]

        # If there is a Human and rendering is False, set it to True
        if self._players.human and not render_settings:
            self._players.change_config_values(constants.PLAYER_GAME, constants.PLAYER_GAME, 'render', "True")
            self._print_msg_box("Render is set to True, since a Human player was detected.")

        kwargs = self._players.get_export_code()
        self._app.removeAllWidgets()
        self._app.threadCallback(Controller, self.refresh, **kwargs, gui=GameGUI(self._app, self._players))
        return self

    def _button_players_switch_show_player(self):
        """ Switches to the next player, and stores the settings of the current one.  """

        # Before switching store all values in case of changed parameters
        self._update_player_settings()

        # Get the new player and show it on the screen
        self._player_selected = self._players.get_player_next()
        self.refresh()
        return self

    def _button_players_add_parameter(self):
        if self._player_selected is constants.PLAYER_GAME:
            self._print_msg_box("Please do not add a GAME parameter.")
            return self

        result = self._retrieve_new_parameter()
        if not result:
            return self

        if len(result.split(';')) is 3:
            self._add_new_parameter(*result.split(';'))
            return self

        self._print_msg_box(f"Couldn't split correctly '{result}' , try again or cancel")
        return self._button_players_add_parameter()

    def _retrieve_new_parameter(self):
        msg = "Please enter the section, parameter and default value, by using ';' as seperator and no spaces. \n" \
              "Section has to be shorted by: '1 = AlgorithmSettings, 2 = PreprocessorSettings'\n" \
              "Example: 1;param1;True\n\n" \
              "Please note that the value will always be returned as a string in the algorithm and preprocessor.rst."
        result = self._app.stringBox("Section;Parameter;Value", msg)
        return result

    def _add_new_parameter(self, section, parameter, value):
        if section not in ["1", "2"]:
            self._print_msg_box("The section is not correct, please try again")
            return self

        section = "AlgorithmSettings" if section == "1" else "PreprocessorSettings"
        player = self._players.get_players()[self._player_selected]
        player.change_config_value(section, parameter.strip(), value.strip())
        self.refresh()
        return self

    def _update_player_settings(self):
        """ Store all the changes to the config handler of the player.  """

        # Update all the values from the Entry boxes in the selected players config file
        input_types = [self._app.getAllEntries, self._app.getAllOptionBoxes]
        for inputs in input_types:
            for key, value in inputs().items():
                player_name, section, key = key.split(";")
                self._players.change_config_values(player_name, section, key, value)

        # Update all the ai with the controller settings
        self._players.save_game_config_in_players()

        return self

    def _save_player_settings(self):
        """ Store all the player settings to disk.  """

        # First update the player settings, in case it has been changes
        self._update_player_settings()

        # Check if the save folder is correct
        flag, path = self._players.check_save_path()
        while not flag:
            # Make sure that the new save folder, is also the folder that you want
            path = self._app.directoryBox("save path", dirName=path)
            if not path:
                # If you cancel the saving, abort
                return False

            # Save the new path to the controller settings
            player = constants.PLAYER_GAME
            self._players.change_config_values(player_name=player, section=player, key="save_folder", value=path)
            flag, path = self._players.check_save_path()

        # Actually save the players
        self._players.save_players(path)

        # Update the screen
        self.refresh()

        # Give a note that it is completed
        self._print_msg_box(f"Save successful\n{path}")
        return self

    def _add_tooltips(self, wdg_name):
        """ Adds a tooltip at hoovering over the letters of the widget.  """

        # Remove player specific information, maintain section and key
        clean_wdg_name = ";".join(wdg_name.split(";")[1:])

        # In case it is HUMAN, remove the endings for the tooltips
        clean_wdg_name = clean_wdg_name.replace("_1", "").replace("_2", "")

        # If the tooltip is in the tooltip dictionary and we want to show tooltips
        # Add them, too the active tooltips.
        if constants.TOOLTIPS.get(clean_wdg_name, None) and not self._remove_tooltips:
            self._app.setLabelTooltip(wdg_name, constants.TOOLTIPS[clean_wdg_name])
            self._active_tooltips.append(f"setLabelTooltip;{wdg_name}")
        return self

    def _add_tooltips_buttons(self, menu):
        """ Add tooltips to the buttons.  """
        buttons = []
        if menu == "HOME_MENU":
            buttons = constants.BUTTONS_HOME_MENU

        if menu == "PLAYER":
            buttons = constants.BUTTONS_PLAYER

        if menu == "RUNNING_GAME":
            buttons = constants.BUTTONS_RUNNING_GAME

        for button in buttons:
            if constants.TOOLTIPS.get(button, None) and not self._remove_tooltips:
                self._app.setButtonTooltip(button, constants.TOOLTIPS[button])
                self._active_tooltips.append(f"setButtonTooltip;{button}")
        return self

    # TODO make it a proper fix, if it gets called back from the controller
    # it gets an extra variable, that it doesn't need nor uses.
    def refresh(self, callback=None):
        self.clear_layout()
        if self._player_selected:
            self._create_layout_player_settings(self._player_selected)
            return self
        self.create_layout_ending()
        return self

    def _change_tooltip_value(self, value):
        self._remove_tooltips = value
        msg = "Added tooltips hover over items to see them." if not value else "Removed tooltips"
        self._print_msg_box(msg)
        self.refresh()
        return self

    def _menu_files_options(self, btn):
        mapping = {
            "Open": (self._button_home_menu_load_ai, dict()),
            "Save": (self._buttons_home_menu_save, dict()),
            "Show help": (self._change_tooltip_value, dict(value=False)),
            "Disable help": (self._change_tooltip_value, dict(value=True)),
            "License": (self._menu_files_options_license, dict()),
            "Close": (self._app.stop, dict())
        }

        if mapping.get(btn, None):
            function, args = mapping[btn]
            function(**args)
        return self

    def _menu_files_options_license(self):
        self._app.addWebLink()
        return self
