
"""
    Date created: 2019/07/03
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import unittest
from pycman.utils.helper import Collecter


class TestCollector(unittest.TestCase):

    def setUp(self):
        self.collector = Collecter()

    def test_add_item(self):
        for i in range(3):
            self.collector.add(i)
        self.assertEqual([i for i in range(3)], self.collector.store, msg="Not appending correctly")

    def test_extend_items(self):
        self.collector.add([i for i in range(3)])
        self.assertEqual([i for i in range(3)], self.collector.store, msg="Not appending multiple items correctly")

    def test_representation(self):
        self.collector.add([i for i in range(3)])
        self.assertEqual("[0, 1, 2]", repr(self.collector))

    def test_iterable(self):
        self.collector.add([i for i in range(3)])
        for i in self.collector:
            ...


if __name__ == "__main__":
    unittest.main()
