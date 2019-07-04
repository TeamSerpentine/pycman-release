

import multiprocessing


class Run:
    def __init__(self, agents, environments):
        self.agents = agents
        self.environments = environments

    def run(self):
        for agent in self.agents:
            for environment in self.environments:
                print(f"{str(agent).ljust(20)}, {environment}")
