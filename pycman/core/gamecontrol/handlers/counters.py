"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import time


class HandlerCounters:
    def __init__(self, step_id=0, game_id=0, time_past=0.0, total_steps=0):
        """ Controls all game counters.  """
        self.step_id = step_id
        self.game_id = game_id
        self.time_past = time_past
        self.total_steps = total_steps
        self.timer_start_time = time.time()

    def timer_start(self):
        """ Start the timer.  """
        self.timer_start_time = time.time()
        return self

    def timer_diff(self):
        """ Keep track of the time between steps.  """
        timer_diff = round(time.time() - self.timer_start_time, 2)
        self.timer_start()
        return timer_diff

    def new_step(self):
        """ Update all the counters for a single step.  """
        self.step_id += 1
        self.total_steps += 1
        self.time_past = self.timer_diff()
        return self

    def new_game(self):
        """ Update all the counters when the game is over.  """
        self.step_id = 0
        self.game_id += 1
        self.total_steps += 1
        self.time_past = 0
        self.timer_start()
