

from pycman import pycman
from pycman.agent.agent import Agent


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

    agents = [MockAgent() for _ in range(8)]

    pycman.env.gym("Breakout-v0")
    pycman.agent.add(agents)

    pycman.run()

    #pycman.run(order='parallel')
    for a in agents:
        print(a.games_played)
    #print(agents[0].games_played)

    print("Env:  ", pycman.env)
    print("Agent:", pycman.agent)
    print(f"Loggers:\n{pycman.logger}")
