""" This file contains the functionality required to add agent to the created environments """


import numpy as np
import pycman

from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def run(self, env, logger, max_thread=1):
        """ Run the agent on the given environment until completion. """
        pass

    def get_environment_info(self, env: pycman.env):
        return env.get_constants()
