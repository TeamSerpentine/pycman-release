"""
    Date created: 2019/07/03
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import unittest
from pycman.core.session.session import _AgentSet


class TestAgentSet(unittest.TestCase):

    def setUp(self):
        self.set = _AgentSet()

    def test_add_item(self):
        for i in range(3):
            self.set.add([i])

        for x, y in zip(self.set, range(3)):
            self.assertEqual([x], [y], msg="Not appending correctly")

    def test_extend_items(self):
        self.set.add([0, 1, 2])
        self.assertEqual([[0, 1, 2]], self.set._nested_store, msg="Not appending multiple items correctly")

    def test_str(self):
        self.set.add([i for i in range(3)])
        self.assertEqual("[[0, 1, 2]]", str(self.set))

    def test_iterable(self):
        self.set.add([i for i in range(3)])
        for _ in self.set:
            pass


if __name__ == "__main__":
    unittest.main()
