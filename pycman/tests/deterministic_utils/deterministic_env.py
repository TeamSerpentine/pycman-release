
import pycman
import numpy as np


class DeterministicGame(pycman.EnvBase):
    game_name = 'DeterministicGame'
    input_shape = (4,)
    output_shape = (4, 4)
    _reward_flag = True
    steps = 0
    closed = False

    def step(self, *args):
        """ Make a step in the game, if there is no action provided, it will repeat the last action. """

        if self._reward_flag:
            self._reward_flag = False
            reward = 0
        else:
            self._reward_flag = True
            reward = 1

        self.steps = self.steps + 1
        if self.steps > 100:
            done = True
        else:
            done = False
        return np.zeros((4, 4)), reward, done, {}

    def reset(self):
        """ Reset all the game variables and environment to the begin state. """
        self.steps = 0
        return

    def render(self):
        """ Renders the game to the screen, this has to be called every time again after a new step.  """
        return

    def close(self):
        self.closed = True
        return

    def info(self):
        """  Get constants that are specific to a game.  """
        return {}
