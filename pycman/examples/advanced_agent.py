import pycman


class RandomAgent(pycman.AgentBase):
    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

        self.loss = None
        self.reward = None
        self.games_played = 0

    def run(self, env):
        for _ in range(2):
            env.reset()
            done = False
            while not done:
                # env.render()
                obs, reward, done, info = env.step(env.random_action())
            self.games_played += 1


if __name__ == "__main__":

    pycman.env.gym("Breakout-v0")

    agent = [RandomAgent()]
    pycman.agent.add(agent)
    pycman.run(order='parallel')

    pycman.env.gym("Breakout-v0")
    pycman.agent.clear()

    # Test with many
    agents4 = [RandomAgent() for _ in range(4)]
    agents2 = [RandomAgent() for _ in range(2)]

    print(len(pycman.agent))
    pycman.agent.add(agents4)
    print(len(pycman.agent))
    pycman.agent.add(agents2)
    print(len(pycman.agent))
    pycman.run(order='parallel')
    pycman.run(order='sequential')

    # TODO: Raise error if no agents are present.
    # TODO: RAISE error if environment is not set.