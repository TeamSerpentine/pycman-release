import pycman


class AdvancedAgent(pycman.AgentBase):
    def __init__(self, number):
        self.number = number
        self.games_played = 0

    def run(self, env):
        for _ in range(2):
            env.reset()
            done = False
            rewards = []
            while not done:
                # env.render()
                obs, reward, done, info = env.step(env.random_action())
                rewards.append(reward)
            self.games_played += 1
            pycman.log.line(self, self.number, self.games_played, sum(rewards))


if __name__ == "__main__":

    #pycman.log.line("First Line!")
    pycman.env.gym("Breakout-v0")
    # agent = [AdvancedAgent(0)]
    # pycman.agent.add(agent)
    # pycman.run(order='parallel')
    # pycman.agent.clear()

    # Test with many
    agents4 = [AdvancedAgent(i+1) for i in range(4)]
    agents2 = [AdvancedAgent(i+5) for i in range(2)]

    print(len(pycman.agent))
    pycman.agent.add(agents4)
    print(len(pycman.agent))
    pycman.agent.add(agents2)
    print(len(pycman.agent))
    #pycman.run(order='parallel')
    pycman.run(order='sequential')

    #pycman.run(order='parallel')

    # TODO: Raise error if no agents are present.
    # TODO: RAISE error if environment is not set.
