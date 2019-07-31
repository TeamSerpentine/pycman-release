import pycman


class AdvancedAgent(pycman.AgentBase):

    def __init__(self, number):
        self.number = number
        self.games_played = 0

    def run(self, env):

        # Set the header for the pycman log file
        pycman.log.set_header(self, 'number', 'games_played', 'rewards')

        # Start running 3 games
        for _ in range(3):
            env.reset()
            done = False
            rewards = []
            while not done:
                # env.render()
                obs, reward, done, info = env.step(env.random_action())
                rewards.append(reward)
            self.games_played += 1

            # Log any given number of arguments
            pycman.log.line(self, self.number, self.games_played, sum(rewards))

        # Plot games_played against rewards. Group per agent. (This uses the header previously set)
        pycman.stat.plot('games_played', 'rewards', group_on_agent=True)

        # Close the log file
        pycman.log.close()


if __name__ == "__main__":

    # Test with a few agents ====================================
    # Set the environment
    pycman.env.gym("Breakout-v0")

    # Initialize 2 agents in a list
    pycman.agent.add([AdvancedAgent(i) for i in range(2)])

    # Different running methods: order = 'sequential or parallel'
    pycman.run(order='sequential')

    # Test with many agents instead =============================
    # Remove all agents first
    pycman.agent.clear()

    agents4 = [AdvancedAgent(i+1) for i in range(4)]
    agents2 = [AdvancedAgent(i+5) for i in range(2)]

    # Adding both agents sets, ending up with 6 agents
    pycman.agent.add(agents4)
    pycman.agent.add(agents2)

    # First do a sequential run
    pycman.run(order='sequential')

    # Then do a run in parallel!
    pycman.run(order='parallel')

    # TODO: Raise error if no agents are present.
    # TODO: RAISE error if environment is not set.
    # TODO: Check agent set length
