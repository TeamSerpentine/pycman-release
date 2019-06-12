"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import gym


class HumanAlgorithm:
    """Algorithm that takes Human inputs.  """

    def __init__(self, game_name, save_folder, save_highscores, player, gui):
        """ Constructor

        game_name: string
            Name of the game

        save_folder: string
            Save location for the highscores

        save_highscores: bool
            If true it will save the best scores

        app: appJar gui interface
            Is used to render the game to the screen
        """

        if not gui:
            raise ValueError("Needs an interface in order to work")

        self._player = player
        self._gui = gui

    def store_and_pick_action(self, _):
        """ Asks for an action from the gui.  """
        return self._gui.return_player_action(self._player)

    def render_game_in_app(self, observation):
        """ Renders the game in the gui.  """
        self._gui.render_game(self._player, observation)
        return self._gui.return_player_action(player=self._player)
