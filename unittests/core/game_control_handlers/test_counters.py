"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

from pycman.core.gamecontrol.handlers.counters import HandlerCounters

import time
import unittest


class TestHandlerCounters(unittest.TestCase):

    def setUp(self):
        self._counter = HandlerCounters()
        self._counter_random = HandlerCounters(step_id=50, game_id=20, time_past=15.67,
                                               total_steps=1000)

    def test_init(self):
        self.assertEqual(self._counter.step_id, 0, msg="Init step id not correct")
        self.assertEqual(self._counter.game_id, 0, msg="Init game id not correct")
        self.assertEqual(self._counter.time_past, 0.0, msg="Init step id not correct")
        self.assertEqual(self._counter.total_steps, 0, msg="Init step id not correct")
        self.assertAlmostEqual(self._counter.timer_start_time, time.time(),
                               msg="Init timer start time not correct", places=3)

    def test_init_with_variables(self):
        self.assertEqual(self._counter_random.step_id, 50, msg="Random init step id not correct")
        self.assertEqual(self._counter_random.game_id, 20, msg="Random init game id not correct")
        self.assertEqual(self._counter_random.time_past, 15.67, msg="Random init time past not correct")
        self.assertEqual(self._counter_random.total_steps, 1000, msg="Random init total steps id not correct")
        self.assertAlmostEqual(self._counter_random.timer_start_time, time.time(),
                               msg="Random init timer start time not correct", places=3)

    def test_new_steps(self):
        self._counter.timer_start()
        for steps in range(1, 100):
            self._counter.new_step()
            self.assertEqual(self._counter.step_id, steps, msg="New step id not correct")
            self.assertEqual(self._counter.game_id, 0, msg="New game id not correct")

    def test_new_game(self):
        self._counter_random.new_game()
        self.assertEqual(self._counter_random.step_id, 0, msg="New game, step id not correct")
        self.assertEqual(self._counter_random.game_id, 21, msg="New game, game id not correct")
