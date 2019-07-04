
import pycman.env.env_gym as env_gym


class Collector:
    def __init__(self):
        self.store = []

    def add(self, item):
        if not hasattr(item, "__iter__"):
            item = [item]
        self.store.extend(item)

    def __str__(self):
        return str(self.store)

    def __repr__(self):
        return f"<class '{self.__name__}'>"

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class Env():

    environment = None

    def gym(self, name):
        self.environment = env_gym.HandlerGym(name)

    def get(self):
        return self.environment
