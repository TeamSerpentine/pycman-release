"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import difflib
import gym
import numpy as np

from collections import namedtuple
from pycman.core.env import Env


class HandlerGym(Env):
    """ Handles the call to gym and stores all the variables.

        Parameters
        ----------
        game_name: str
            The game name of the gym environment (this includes version and correct
            capitalization, for example 'MsPacman-v0'.
    """
    __slots__ = ("_env", "game_name", "input_shape", "output_shape", "total_reward", "total_action_distribution",
                 "action", "action_new")

    def __init__(self, game_name):
        # If the game name is not available in gym, there will be an error
        # and it will return possible alternatives.
        if game_name not in self.get_all_environment_names():
            alternatives = self.find_n_nearest_matches(game_name, 5)
            raise ValueError("Game not found, close matches are:\n {}".
                             format('\n '.join(map(str, alternatives))))

        self._env = gym.make(game_name)

        # Store environment variables
        self.game_name = game_name
        self.input_shape = self._env.reset().shape
        self.output_shape = self._get_action_space(self._env),

        # Set all the default variables
        self.total_reward = 0
        self.total_action_distribution = np.zeros(self.output_shape)

        self.done = False
        self.action = 0
        self.action_new = 0

    def __repr__(self):
        return f"<class 'Handlergym' game {self.game_name}>"

    @staticmethod
    def _get_action_space(env):
        """ Check the action space for different game types.  """
        if hasattr(env.action_space, 'n'):
            return env.action_space.n

        if hasattr(env.action_space, 'shape'):
            return env.action_space.shape

        raise ValueError("Unknown action space, try another game")

    @staticmethod
    def _get_action_meanings(env):
        """ Return the names of the actions that you can provide.  """
        if hasattr(env.unwrapped, 'get_action_meanings'):
            return env.unwrapped.get_action_meanings()
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

    def random_action(self):
        """ Returns a random action, which is an integer between 0 and the action space.  """
        self.action_new = self._env.action_space.sample()
        return self.action_new

    def step(self, action=None):
        """ Make a step in the game, if there is no action provided, it will repeat the last action. """
        if action is not None:
            self.action_new = action
        self.action = self.action_new

        obs, reward, done, info = self._env.step(self.action_new)

        self.total_reward += reward
        if self.done:
            # TODO log rewards
            ...
        return obs, reward, done, info

    def reset(self):
        """ Reset all the game variables and environment to the begin state. """
        self._env.reset()
        self.action = 0
        self.done = False
        return self

    def render(self):
        """ Renders the game to the screen, this has to be called every time again after a new step.  """
        self._env.render()
        return self

    def close(self):
        self._env.close()
        return self

    def info(self):
        """  Get constants that are specific to a game.  """
        info = namedtuple("info", ["action_meanings"])
        return info(action_meanings=self._get_action_meanings(self._env))
