""" This file contains the functionality required to create, step and reset environments """

import numpy as np

from collections import namedtuple
from abc import ABC, abstractmethod


class Env(ABC):
    game_name = None
    input_shape = (None,)
    output_shape = (None,)

    @abstractmethod
    def step(self, action: int) -> [np.array, int, bool, dict]:
        """ Perform one step in the environment with the provided arguments. """
        pass

    @abstractmethod
    def reset(*args, **kwargs):
        """ Resets the environment.  """
        pass
