"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


from pycman.core.gui.auxiliary import constants
from PIL import  Image, ImageTk


class GameGUI:
    def __init__(self, app, players, unique_id=1):
        self._app = app
        self._players = players
        self._players_actions = self.fill_players_actions(players)
        self._unique_id = unique_id
        self._render_game_setup_flag = False
        self._pause_game_flag = False

        # TODO implement pause option for AI only as well
        self._app.addButtons(constants.BUTTONS_RUNNING_GAME, self._running_game_options, colspan=constants.CENTERED)
        if not self._players.human:
            self._app.disableButton("PAUSE GAME")

        # Activate the keys
        self._app.bindKeys(constants.KEYS_HUMAN_1, self._pressed_keys_human)
        self._app.bindKeys(constants.KEYS_HUMAN_2, self._pressed_keys_human)

        # Retrieve the render settings
        game_settings = self._players.get_player_config(constants.PLAYER_GAME)
        render_settings = game_settings[f"{constants.PLAYER_GAME};{constants.PLAYER_GAME};render"]

        # If there are no render settings give this message instead.
        if not render_settings:
            self._app.addLabel("The render option is set to False, no visualization. "
                               "Game is playing in the background. \n"
                               "You can increase speed by running from main_load_ini instead")

    def fill_players_actions(self, players):
        player_action = dict()
        for player in players.human:
            player_action[player] = 0
        return player_action

    def render_game_setup(self, observation):
        if self._render_game_setup_flag:
            return self

        image = self._convert_observation_to_image(observation)
        row, column = self._app.getRow(), 0
        for num, player in enumerate(self._players.get_players()):
            if num % constants.LIMIT_PLAYER_PER_ROW == 0:
                row += 1
                column = 0

            with self._app.frame(f"{player} {self._unique_id} plot", row=row, column=column):
                self._app.addImageData(f"{player} {self._unique_id}", image, fmt="PhotoImage")
                # self._app.setImageSize(player, 420, 320)
                column += 1
        self._render_game_setup_flag = True
        return self

    def render_game(self, player, observation):
        image = self._convert_observation_to_image(observation)
        self._app.reloadImageData(f"{player} {self._unique_id}", image, fmt="PhotoImage")
        return self

    @staticmethod
    def _convert_observation_to_image(observation):
        pil_image = Image.fromarray(observation, 'RGB')
        pil_image = ImageTk.PhotoImage(pil_image)
        return pil_image

    def return_player_action(self, player):
        return self._players_actions.get(player, 0)

    def _pressed_keys_human(self, btn):
        for player, handlers in self._players.human.items():
            if constants.PLAYER_HUMAN in player:
                keys = self._players.get_player_config(player)[f"{player};{player};keys"]
                if btn in getattr(constants, keys):
                    self._players_actions[player] = getattr(constants, keys).index(btn)
                    return self
        return self

    def _running_game_options(self, btn):
        if btn == "TERMINATE GAME AND GUI":
            self._running_game_options_terminate_game()
            return self

        if btn == "PAUSE GAME":
            self._running_game_options_pause_game()
            return self
        return self

    def _running_game_options_terminate_game(self):
        # If there are no Human players, just stop the app to cancel

        # Just terminate, there is a bug if you try to
        # run a game after one is terminated,
        # has to do with pyglet.app net being reloaded
        # in the Atari gym environment
        exit()

        if not self._players_actions:
            self._app.stop()

        for player in self._players_actions:
            self._players_actions[player] = -1
        return self

    def _running_game_options_pause_game(self):
        for player, action in self._players_actions.items():
            # If the game is already paused, continue, otherwise pause it
            if action < 0:
                self._players_actions[player] = 0
            else:
                self._players_actions[player] = -2
