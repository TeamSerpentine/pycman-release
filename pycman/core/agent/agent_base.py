""" This file contains the functionality required to add agent to the created environments """

import pycman

from abc import ABC, abstractmethod


class AgentBase(ABC):

    part_of_parallel_pool = False
    agent_id = float('nan')

    @abstractmethod
    def run(self, env):
        """ Run the agent on the given environment until completion. """
        pass
