"""
    Date created: 2019/07/03
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import unittest
from pycman.core.logger.simple_logger import Log
import inspect
import os


class TestLogger(unittest.TestCase):

    def test_constructor(self):
        Log(None, inspect.stack()[0][3])

    def test_close(self):
        log = Log(None, inspect.stack()[0][3])
        log.close()

    def test_writing_lines(self):
        a = type('AgentBase', (), {})()
        a.part_of_parallel_pool = False
        a.agent_id = 0

        file_name = inspect.stack()[0][3]
        if os.path.exists(file_name + '.csv'):
            os.remove(file_name + '.csv')

        log = Log(None, file_name)
        log.line(a, 1, 2, 3, 4, 'Hello')
        log.line(a, 1, 2, 4, 'Hello')
        log.close()

        file = open(file_name + '.csv')
        lines = [line for line in file]
        file.close()

        self.assertTrue(lines == ['0;1;2;3;4;Hello\n', '0;1;2;4;Hello\n'])

        if os.path.exists(file_name + '.csv'):
            os.remove(file_name + '.csv')


if __name__ == "__main__":
    unittest.main()
