
import pycman.env.env_gym as env_gym


class Collecter:
    def __init__(self):
        self.store = []

    def add(self, item):
        if not hasattr(item, "__iter__"):
            item = [item]
        self.store.extend(item)

    def __repr__(self):
        return str(self.store)

    def __iter__(self):
        return iter(self.store)


class Env(Collecter):
    gym = env_gym.HandlerGym
