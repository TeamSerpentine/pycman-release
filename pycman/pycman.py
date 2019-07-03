""" This file contains links to every public function available in the Pycman package. """

import pycman.env.env_gym as env_gym

from pycman.stat.logger import Logger
from pycman.utils.helper import Collecter


class Env(Collecter):
    gym = env_gym.HandlerGym

env = Env()
agent = Collecter()
logger = Logger()