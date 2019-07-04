

from pycman import pycman
from pycman.agent.agent import Agent

class MockAgent(Agent):
    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

        self.loss = None
        self.reward = None
        self.games_played = 0
        print(self.get_environment_info())

    def run(self, env, logger, max_threads=1):
        for _ in range(2):
            env.reset()
            done = False
            while not done:
                obs, reward, done, info = env.step(env.random_action())
                logger.step.add(reward)
                return 0
            self.games_played += 1
            logger.game.add(self.games_played)



if __name__ == "__main__":

    env_pacman = pycman.env.gym("MsPacman-v0")
    env_breakout = pycman.env.gym("Breakout-v0")

    pycman.env.add([env_pacman, env_breakout])
    pycman.agent.add([MockAgent, MockAgent])

    pycman.run()
    print('')

    print("Env:  ", pycman.env)
    print("Agent:", pycman.agent)
    print(f"Loggers:\n{pycman.logger}")
