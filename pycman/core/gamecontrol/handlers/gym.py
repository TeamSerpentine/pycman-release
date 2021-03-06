"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import gym
import difflib


class HandlerGym:
    """ Handles the call to gym and stores all the variables.  """
    def __init__(self, game_name):
        """ Creates a gym environment

        Parameters
        ----------
        game_name: str
            The game name of the gym environment (this includes version and correct
            capitalization, for example 'MsPacman-v0'.
        """

        # If the game name is not available in gym, there will be an error
        # and it will return possible alternatives.
        if game_name not in self.get_all_environment_names():
            alternatives = self.find_n_nearest_matches(game_name, 5)
            raise ValueError("Game not found, close matches are:\n {}".
                             format('\n '.join(map(str, alternatives))))

        self._env = gym.make(game_name)
        self.game_name = game_name

        # Get the number of action that are available, and the meaning of the actions
        self.action_space = self._env.action_space.n
        self.action_meanings = self._get_action_meanings()

        # Set all the default variables
        self.obs = self._env.reset()
        self.reward = 0
        self.done = False
        self.info = dict()
        self.action_old = 0
        self.action_new = 0

    def _get_action_meanings(self):
        """ Return the names of the actions that you can provide.  """
        if hasattr(self._env.unwrapped, 'get_action_meanings'):
            return self._env.unwrapped.get_action_meanings()
        return None

    @staticmethod
    def get_all_environment_names():
        """ Returns a list of all the possible gym games you can make.  """
        all_environments = gym.envs.registry.all()
        all_game_names = [env_spec.id for env_spec in all_environments]
        return all_game_names

    def find_n_nearest_matches(self, game_name, n):
        """ Returns the n closest matches of the game name, against all of the valid gym names. """
        all_game_names = self.get_all_environment_names()
        close_matches = difflib.get_close_matches(game_name.lower(), all_game_names, n=n)
        return close_matches

    def step(self, action=None):
        """ Make a step in the game, if there is no action provided, it will repeat the last action. """
        if action is not None:
            self.action_new = action
        self.obs, self.reward, self.done, self.info = self._env.step(self.action_new)
        self.action_old = self.action_new
        return self

    def set_action(self, action):
        """ Stores the action that will be executed on the next step if no action is provided.  """
        self.action_new = action
        return self

    def random_action(self):
        """ Returns a random action, which is an integer between 0 and the action space.  """
        self.action_new = self._env.action_space.sample()
        return self.action_new

    def reset_game(self):
        """ Reset all the game variables and environment to the begin state. """
        self.obs = self._env.reset()
        self.reward = 0
        self.done = False
        self.info = {}
        self.action_old = 0
        return self

    def render_game(self):
        """ Renders the game to the screen, this has to be called every time again after a new step.  """
        self._env.render()
        return self

    def close(self):
        self._env.close()
        return self


if __name__ == "__main__":
    HandlerGym("MsPacman-v0")
