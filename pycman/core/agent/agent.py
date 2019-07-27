""" This file contains the functionality required to add agent to the created environments """

import pycman

from abc import ABC, abstractmethod


class Agent(ABC):

    @abstractmethod
    def run(self, env, max_thread=1):
        """ Run the agent on the given environment until completion. """
        pass
