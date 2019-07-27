""" This file contains the functionality required to add agent to the created environments """

import pycman

from abc import ABC, abstractmethod


class AgentBase(ABC):

    @abstractmethod
    def run(self, env):
        """ Run the agent on the given environment until completion. """
        pass
