import pycman


class AdvancedAgent(pycman.AgentBase):

    def __init__(self, number):
        self.number = number
        self.games_played = 0

    def run(self, env):
        pycman.log.set_header(self, 'number', 'games_played', 'rewards')
        for _ in range(3):
            env.reset()
            done = False
            rewards = []
            while not done:
                # env.render()
                obs, reward, done, info = env.step(env.random_action())
                rewards.append(reward)
            self.games_played += 1
            pycman.log.line(self, self.number, self.games_played, sum(rewards))

        pycman.stat.plot('games_played', 'rewards', group_on_agent=True)
        pycman.log.close()


if __name__ == "__main__":

    pycman.env.gym("Breakout-v0")

    # Test with many
    agents4 = [AdvancedAgent(i+1) for i in range(4)]
    agents2 = [AdvancedAgent(i+5) for i in range(2)]

    pycman.agent.add(agents4)
    pycman.agent.add(agents2)

    pycman.run(order='sequential')
    #pycman.run(order='parallel')

    # TODO: Raise error if no agents are present.
    # TODO: RAISE error if environment is not set.
    # TODO: Check agent set length
