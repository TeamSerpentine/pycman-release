""" This file contains the functionality required to log results to a file """

import logging

from pycman.utils.helper import Collecter


class Logger:
    def __init__(self):
        self.console = Collecter()
        self.game = Collecter()
        self.step = Collecter()
        self.general = Collecter()

    def __repr__(self):
        return f" Console: {self.console}\n" \
               f" Game:    {self.game}\n" \
               f" Step:    {self.step}\n" \
               f" General: {self.general}\n"
