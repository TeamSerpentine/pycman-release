

import pycman
from pycman.core.agent.agent import Agent


class MockAgent(Agent):
    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

        self.loss = None
        self.reward = None
        self.games_played = 0

    def run(self, env, max_threads=1):
        for _ in range(3):
            env.reset()
            done = False
            while not done:
                # env.render()
                obs, reward, done, info = env.step(env.random_action())
            self.games_played += 1
        print('finished')


if __name__ == "__main__":

    agents = [MockAgent() for _ in range(2)]

    pycman.env.gym("Breakout-v0")
    # pycman.agent.add(MockAgent())
    # pycman.agent.add(MockAgent())
    # pycman.agent.add(agents)
    # pycman.agent.set(agents)
    pycman.agent.add(agents)

    # for a in pycman.agent:
    #     print(a)
    #
    # for a in agents:
    #     print(a)

    # pycman.run()
    pycman.run(order='sequential')
    # pycman.run(order='parallel')

    # for agent in pycman.agent:
    #     print(agent)
    #     print(agent.games_played)
    #
    # for agent in agents:
    #     print(agent)
    #     print(agent.games_played)
    #
    # print("Env:  ", pycman.env)
    # print("Agent:", pycman.agent)
    # # print(f"Loggers:\n{pycman.logger}")
