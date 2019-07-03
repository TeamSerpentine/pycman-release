""" This file contains the functionality required to add agent to the created environments """


import numpy as np
import pycman

from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """ Creates an environment from one of the supported standard environments (Gym). """
        pass

    @abstractmethod
    def step(self, obs: np.array, reward: int, done: bool, info: dict) -> int:
        """ Perform one step in the environment with the provided arguments. """
        pass

    @abstractmethod
    def create_model(self, env: pycman.env, *args, **kwargs):
        """ Return name, input and output shape of the environment.  """
        pass
