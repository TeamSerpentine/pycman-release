"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import time

from pycman.core.gamecontrol.handlers.gym import HandlerGym
from pycman.core.gamecontrol.handlers.counters import HandlerCounters


class GameInterface(object):
    """ Creates an interface for the Atari game to run in for humans and ais.

        It is an integration of the counters, gym environment and the base.

    """

    def __init__(self, game_name, player_details):
        """ Constructor

            Parameters
            ----------
            game_name: str
                name of the atari game

            player_details: dict
                Dictionary with the player name and initialized base
                it uses.
        """

        self._players = {}

        if not player_details:
            raise ValueError("Unable to initialize players, check the input")

        for player_name, algorithm in player_details.items():
            self._players[player_name] = self._create_player(game_name, algorithm)

    def _create_player(self, game_name, algorithm):
        """ Gives every player a Gym, Counter and an base.  """

        class Player:
            """ Makes an object ouf of the other classes.  """
            def __init__(self, game_name, algorithm_class):
                self.gym = HandlerGym(game_name)
                self.counters = HandlerCounters()
                self.algorithm = algorithm_class

        return Player(game_name, algorithm)

    def _game_step(self, player, action=None):
        """
             Takes a step in the game, and if no action is specified
             it will take a random step.

             Parameters
             ----------
             player: Player
                class containing a HandlerGameCounter and HandelGym class

             action: int
                 an action within the available action space, if no valid
                 action is passed it will choose a random action to execute.

         """

        # If the game is over reset everything for next game
        if player.gym.done:
            player.gym.reset_game()
            player.counters.new_game()
            return player

        # take a step and update the appropriate counters
        player.gym.step(action)
        player.counters.new_step()

        return self

    def play_game(self, render=False, frames_per_seconds=0, gui=None):
        """ Optimizes the game loop for the given parameters.

        render: bool
            Show the game on the screen if true

        frames_per_seconds: int
            Number of frames to show every seconds

        gui: gui
            If you want to render the game in the gui itself
        """

        # If the game is not pixel data, use the gym renderer instead
        player = self._players[next(iter(self._players))]
        observation = player.gym.obs
        if observation.shape != (210, 160, 3):
            gui = None

        # Run the game interfaced with a gui.
        if render and gui:
            self._render_gui_game_setup(gui)
            while True:
                if False in [self._play_game_render_true_appJar(items) for items in self._players.values()]:
                    [items.gym.close() for items in self._players.values()]
                    break

                if frames_per_seconds:
                    time.sleep(1 / frames_per_seconds)

        # Run the game and render using a gym environment
        if render and not gui:
            while True:
                if False in [self._play_game_render_true_gym(items) for items in self._players.values()]:
                    [items.gym.close() for items in self._players.values()]
                    break

                if frames_per_seconds:
                    time.sleep(1 / frames_per_seconds)

        # Run the game, without interface
        if not render:
            while True:
                if False in [self._play_game_render_false(items) for items in self._players.values()]:
                    [items.gym.close() for items in self._players.values()]
                    break

    def get_players(self):
        """ Return all the players in the game.  """
        return self._players

    def _play_game_render_false(self, player_items):
        """ Only runs the game, no rendering possible.  """

        # Let the base pick the next action
        action = player_items.algorithm.store_and_pick_action(player_items)

        # Check for the pause or terminating the game
        if not self._check_action_meaning(action):
            return self._check_action_meaning(action)

        # Make the step and update all the counters
        self._game_step(player_items, action)

        return self

    def _play_game_render_true_gym(self, player_items):
        """ Run the game, and renders using Atari Gym env.  """

        # Render the game
        player_items.gym.render_game()

        # Let the base pick the next action
        action = player_items.algorithm.store_and_pick_action(player_items)

        # Check for the pause or terminating the game
        if not self._check_action_meaning(action):
            return self._check_action_meaning(action)

        # Make the step and update all the counters
        self._game_step(player_items, action)

        return self

    def _play_game_render_true_appJar(self, player_items):
        """ Run the game, and show it in the gui.  """

        # Call for the special rendering in the gui
        player_items.algorithm.render_game_in_app(player_items.gym.obs)

        # Let the base pick the next action
        action = player_items.algorithm.store_and_pick_action(player_items)

        # Check for the pause or terminating the game
        if not self._check_action_meaning(action):
            return self._check_action_meaning(action)

        # Make the step and update all the counters
        self._game_step(player_items, action)

        return self

    def _render_gui_game_setup(self, gui):
        """ Setup for the rendering in the appJar gui.  """

        # Select the first player
        player = self._players[next(iter(self._players))]

        # Get the observation from the player (this is just after env.reset())
        observation = player.gym.obs

        # Let the gui change the interface, and set the observation
        # as a basic template, it will be refresh every step
        gui.render_game_setup(observation)

    @staticmethod
    def _check_action_meaning(action):
        if action < 0:

            # Terminate the game
            if action == -1:
                return False

            # Pause the game, by inserting NOOP
            if action == -2:
                return None
        return True
