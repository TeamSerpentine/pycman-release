
import pycman.core.env.env_gym as env_gym

from  pycman.core.stat.logging.logger import Logger


class EnvSelector:
    environment = None
    game_name = None

    def gym(self, name):
        self.environment = env_gym.HandlerGym(name)
        self.game_name = name
        Logger.setup_logging(name)

    def get(self):
        return self.environment

    def info(self):
        return self.environment.info