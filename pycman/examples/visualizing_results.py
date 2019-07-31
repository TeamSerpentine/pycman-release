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

    def run(self, env):

        # Sets the header of the log
        pycman.log.set_header(self, 'games_played', 'rewards', 'loss')

        # Play 3 sets of 10 games
        for _ in range(3):
            self.play_a_set_of_10_games(env)

            # Visualize after 10 games are done.
            pycman.stat.plot('games_played', ['rewards', 'loss'], title='Loss and performance vs games played')
            print('RandomAgent finished', self.games_played, 'games!')

    def play_a_set_of_10_games(self, env):

        # Play 10 games
        for _ in range(10):
            rewards = []
            env.reset()
            done = False

            while not done:
                # env.render()
                obs, reward, done, info = env.step(env.random_action())
                rewards.append(reward * self.dummy_growth ** self.games_played)

            self.games_played += 1

            # Log the following things after a game is played
            pycman.log.line(self,  # Caller
                            self.games_played,  # Number of played games
                            sum(rewards),  # Sum of rewards (amplified)
                            500 * (random() + 0.5) * self.dummy_loss ** self.games_played
                            # Decreasing fake loss function
                            )


if __name__ == "__main__":

    # Add a single agent
    agent = [RandomAgent()]

    # Set the environment
    pycman.env.gym("Breakout-v0")

    # Add the agent
    pycman.agent.add(agent)

    # Run!
    pycman.run()
