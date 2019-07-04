""" This file contains the functionality required to log results to a file """

import logging

from pycman.utils.helper import Collector


class Logger:
    def __init__(self):
        self.console = Collector()
        self.game = Collector()
        self.step = Collector()
        self.general = Collector()

    def __repr__(self):
        return f" Console: {self.console}\n" \
               f" Game:    {self.game}\n" \
               f" Step:    {self.step}\n" \
               f" General: {self.general}\n"
