""" This file contains the functionality required to log results to a file """

import os
import json
import logging.config
import logging.handlers
import subprocess
import yaml

from pycman.core.utils.helper import DataLogger


class LogFilter(logging.Filter):
    def __init__(self, type):
        super(LogFilter, self).__init__()
        self.type = type

    def filter(self, rec):
        return rec.name == self.type


class TTSHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        # Speak slowly in a female English voice
        cmd = ["C:\Program Files (x86)\eSpeak\command_line\espeak.exe", '-s150', '-veng+f3', msg]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # wait for the program to finish
        p.communicate()


class Logger:
    path = os.path.join(os.path.dirname(__file__), "logging.yaml")

    def __init__(self, game_name, loc=path):
        self.console = DataLogger("console")
        self.game = DataLogger("game")
        self.general = DataLogger("general")

        if not os.path.exists("log"):
            os.mkdir("log")

        self.setupLogging(loc, game_name)
        for handler in self.game.log.parent.handlers:
            if hasattr(handler, "doRollover"):
                handler.doRollover()

    def __repr__(self):
        return "<class 'Logger'>"

    def setupLogging(self, loc, game_name):
        # Load yaml settings
        with open(loc, 'rt') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

        # Add game name to logger
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.game_name = game_name
            return record

        old_factory = logging.getLogRecordFactory()
        logging.setLogRecordFactory(record_factory)


if __name__ == "__main__":
    log = Logger("Space invaders")

    for type in ["console", "general", "game"]:
        for level in ["debug", "info", "warning", "error", "critical"]:
            input = dict(reward=5, loss=10, actions={0: 5, 1: 10, 2: 40})
            getattr(getattr(log, type), level)(json.dumps(input))
        print("")
