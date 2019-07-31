import pycman


class RandomAgent(pycman.AgentBase):
    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

        self.loss = None
        self.reward = None
        self.games_played = 0

    def run(self, env):

        # play 3 games
        for _ in range(3):
            env.reset()
            done = False
            while not done:
                obs, reward, done, info = env.step(env.random_action())
            self.games_played += 1
        print('finished')


if __name__ == "__main__":

    # Creating a list with 8 RandomAgent instances
    agents = [RandomAgent()]

    # Start with a particular environment
    pycman.env.gym("Breakout-v0")

    # Adding the agents to pycman!
    pycman.agent.add(agents)
    pycman.run()

