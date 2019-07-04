from copy import deepcopy
import multiprocessing


class Run:
    def __init__(self, agents, env):
        self.agents = agents
        self.env = env

    def run(self):
        envs = [deepcopy(self.env.get()) for _ in self.agents]

        for agent, env in zip(self.agents, envs):
            print(f"{str(agent).ljust(20)}, {env}")
            agent.run(env)
            env.close()
