

from pycman import pycman

class MockAgent:
    def __init__(self):
        self.output_shape = ...
        self.input_shape = ...

    def step(self, *args, **kwargs): return 0

    def create_model(self, *args, **kwargs): ...


if __name__ == "__main__":
    env = pycman.env.gym("MsPacman-v0")

    pycman.env.add(env)
    pycman.agents.add(MockAgent)