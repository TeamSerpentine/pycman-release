
import pycman.core.env.env_gym as env_gym

from pycman.core.stat.logging.logger import Logger


class GlobalEnv:
    """ Wrapper for all the different environment wrappers. Global access point for the currently
        selected environment in Pycman.
    """

    environment = None
    game_name = None

    def gym(self, name):
        self.environment = env_gym.GymWrapper(name)
        self.game_name = name
        Logger.setup_logging(name)

    def get(self):
        return self.environment

    def info(self):
        return self.environment.info