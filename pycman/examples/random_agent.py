

import pycman
from pycman.core.agent.agent import Agent


class RandomAgent(Agent):
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

    agents = [RandomAgent() for _ in range(8)]

    pycman.env.gym("Breakout-v0")
    pycman.agent.add(agents)
    pycman.run(order='sequential')