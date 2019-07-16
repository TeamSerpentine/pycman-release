
from copy import deepcopy
from multiprocessing import Pool
from pycman.core.utils.decorators import timer
import pycman


class Run:
    def __init__(self, agents, env):
        self.agents = agents
        self.env = env

    @timer
    def run(self, order='sequential'):
        if order == 'sequential':
            self.run_sequential()
        else:
            self.run_parallel()

    def run_sequential(self):
        envs = [deepcopy(self.env.get()) for _ in self.agents]

        for agent, env in zip(self.agents, envs):
            agent.run(env)
            env.close()

    def run_parallel(self):
        envs = [deepcopy(self.env.get()) for _ in self.agents]

        args = []
        for agent, env in zip(self.agents, envs):
            args.append((agent, env))
            # FIXME: create test case -> print(str(agent) + "##############")

        with Pool(len(self.agents)) as p:
            result = p.map(self.start_worker, args)

        print(self.agents)
        for idx, a in enumerate(result):
            self.agents[idx] = a
        return

    @staticmethod
    def start_worker(info):
        info[0].run(info[1])
        return info[0]
