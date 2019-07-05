
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

    def start_worker(self, info):
        info[0].run(info[1])
        return info[0]

    def run_parallel(self):

        envs = [deepcopy(self.env.get()) for _ in self.agents]

        args = []
        for agent, env in zip(self.agents, envs):
            args.append((agent, env))
            print(str(agent) + "##############")

        with Pool(len(self.agents)) as p:
            result = p.map(self.start_worker, args)

        # print(result)
        for idx, a in enumerate(result):
            self.agents.store[idx] = a
        # for a in agents:
        #     print("parallel:", a.games_played)
        return


    # def run_parallel(self):
    #     envs = [deepcopy(self.env.get()) for _ in self.agents]
    #
    #     processes = []
    #     for agent, env in zip(self.agents, envs):
    #         p = Process(target=agent.run, args=(env,))
    #         processes.append(p)
    #
    #     # Start the processes
    #     for p in processes:
    #         print(f"{str(agent).ljust(20)}, {env}")
    #         p.start()
    #
    #     # Ensure all processes have finished execution
    #     for p in processes:
    #         p.join()

        return
