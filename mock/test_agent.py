

from pycman import pycman


class MockAgent:
    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

        self.loss = None
        self.reward = None

    def run(self, model, env, logger, max_threads=1):
        done = False
        while not done:
            obs, reward, done, info = env.step(env.random_action())

        return 0

    def create_model(self, *args, **kwargs): ...


if __name__ == "__main__":
    env = pycman.env.gym("MsPacman-v0")

    pycman.env.add(env)
    pycman.agent.add([MockAgent, MockAgent])
    pycman.logger.game.add(["reward", "loss"])
    pycman.logger.console.add(["error"])

    print("Env:  ", pycman.env)
    print("Agent:", pycman.agent)
    print(f"Loggers:\n{pycman.logger}")
