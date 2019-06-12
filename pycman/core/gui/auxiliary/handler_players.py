"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


from itertools import cycle

from pycman.core.gui.auxiliary import constants
from pycman.core.gui.auxiliary.handler_config import HandlerConfig


class HandlerPlayers:
    def __init__(self):
        self.human = dict()
        self.ai = dict()
        self.game = dict()

        self.player_actions = dict()
        self._player_iterable = cycle(self.get_players())

        # Add the game settings to the dictionary.
        self.add_player(constants.PLAYER_GAME)

    def __len__(self):
        return len(self.get_players())

    def add_player(self, player_type):
        """ Add an extra player to the right dictionary.  """
        name = self._get_player_name(player_type)
        if player_type == constants.PLAYER_AI:
            getattr(self, player_type.lower())[name] = HandlerConfig(name)

        if player_type == constants.PLAYER_GAME:
            getattr(self, player_type.lower())[name] = HandlerConfig(name)

        if player_type == constants.PLAYER_HUMAN:
            config = self._get_player_settings_human(name)
            getattr(self, player_type.lower())[name] = config

        # Update the next player cycle
        self._player_iterable = cycle(self.get_players())
        return name

    def del_player(self, name):
        """ Deletes a player based on the name.  """
        if constants.PLAYER_HUMAN in name:
            if name in self.human:
                del self.human[name]

        if constants.PLAYER_AI in name:
            if name in self.ai:
                del self.ai[name]

        # Update the next player cycle
        self._player_iterable = cycle(self.get_players())
        return self

    def get_players(self):
        """ Returns all the human.rst and AI players.  """
        return dict(**self.human, **self.ai)

    def get_players_all(self):
        """ Returns all the human.rst, AI and game players.  """
        return dict(**self.human, **self.ai, **self.game)

    def get_player_next(self):
        """ Returns the next player that is available.  """
        if self.get_players():
            return next(self._player_iterable)
        return None

    def get_player_config(self, player_name, per_section=False):
        if not self.get_players_all().get(player_name, None):
            raise ValueError(f"Player '{player_name}', does not seem to exist")

        if per_section:
            return self.get_players_all()[player_name].get_config_values_per_section()
        return self.get_players_all()[player_name].get_config_values()

    def _get_player_name(self, player_type):
        """ Goes through all the possible names and stops if the name is not used.

        Parameters
        ----------
        player_type: string
            Should be either human.rst, ai or game
        """
        # If it the game, return the name
        if player_type == constants.PLAYER_GAME:
            return constants.PLAYER_GAME

        limit_player_type = getattr(constants, f"LIMIT_PLAYER_{player_type}")
        names_used_player_type = getattr(self, player_type.lower())
        for num in range(1, limit_player_type+1):
            if f"{player_type}_{num}" not in names_used_player_type:
                return f"{player_type}_{num}"
        raise ValueError("Cannot get add another name, limit has been reached?")

    @staticmethod
    def _get_player_settings_human(name):
        config = HandlerConfig(name)
        config.reset_config_values()
        config.change_config_value(name, "player", "HUMAN")
        config.change_config_value(name, "keys", f"KEYS_{name}")
        config.change_config_value(name, "save_highscores", "False")
        return config

    def change_config_values(self, player_name, section, key, value):
        """ Change a config value, if it was changed in the gui.  """
        player = self.get_players_all()[player_name]
        player.change_config_value(section, key, value)
        return self

    def check_save_path(self):
        return self.get_players_all()[constants.PLAYER_GAME].check_save_path()

    def save_players(self, path):
        """ Store the settings to disk.  """

        # If there are only human.rst players store the game data
        if not len(self.ai):
            self.get_players_all()[constants.PLAYER_GAME].save_file(path)
            return self

        # Store all of the AI's that you have
        for player_name, settings in self.ai.items():
            settings.save_file(path)

    def save_game_config_in_players(self):
        section_dict = self.game[constants.PLAYER_GAME].get_config_values_per_section()
        for key, value in section_dict[constants.PLAYER_GAME].items():
            for config in self.get_players().values():
                config.change_config_value(constants.PLAYER_GAME, key, str(value))
        return self

    def load_config_from_ai(self, player_name, open_loc):
        """ Get the controller settings from an ai.  """

        # Load the settings from the ai
        self.ai[player_name].load_file(open_loc)

        # Pass all the settings to the controller
        game_config = self.game[constants.PLAYER_GAME].reset_config_values()
        value_dict = self.ai[player_name].get_config_values_section(constants.PLAYER_GAME)
        for key, value in value_dict.items():
            _, section, key = key.split(';')
            game_config.change_config_value(section, key, str(value))
        return self

    def get_export_code(self):
        export_dict = dict()
        player_dict = dict()
        for player_name, config in self.get_players_all().items():
            if player_name == constants.PLAYER_GAME:
                for key, value in config.create_export_code().items():
                    export_dict[key] = value
            else:
                player_dict[player_name] = config.create_export_code()
        export_dict["players"] = player_dict
        return export_dict


if __name__ == "__main__":
    test = HandlerPlayers()
