import pycman
from random import random


class RandomAgent(pycman.AgentBase):

    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

        self.loss = None
        self.reward = None
        self.games_played = 0
        self.dummy_growth = 1.2
        self.dummy_loss = 0.7
        pycman.log.set_header(self, 'games_played', 'rewards', 'loss')

    def run(self, env):

        for _ in range(3):
            for _ in range(10):
                rewards = []
                env.reset()
                done = False

                while not done:
                    # env.render()
                    obs, reward, done, info = env.step(env.random_action())
                    rewards.append(reward*self.dummy_growth**self.games_played)

                self.games_played += 1
                pycman.log.line(self,                                                   # Caller
                                self.games_played,                                      # Number of played games
                                sum(rewards),                                           # Sum of rewards (amplified)
                                500*(random()+0.5)*self.dummy_loss**self.games_played   # Decreasing fake loss function
                                )

            pycman.stat.plot('games_played', ['rewards', 'loss'], title='Loss and performance vs games played')
            print('RandomAgent finished', self.games_played, 'games!')


if __name__ == "__main__":

    agent = [RandomAgent()]
    pycman.env.gym("Breakout-v0")
    pycman.agent.add(agent)
    pycman.run(order='sequential')
