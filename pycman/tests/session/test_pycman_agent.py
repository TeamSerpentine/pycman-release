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
        agents = []
        for _ in range(3):
            a = type('AgentBase', (), {})()
            a.part_of_parallel_pool = False
            a.agent_id = 0
            agents.append(a)

        for i in agents:
            self.set.add([i])

        for x, y in zip(self.set, agents):
            self.assertEqual([x], [y], msg="Not appending correctly")

    def test_extend_items(self):
        agents = []
        for _ in range(3):
            a = type('AgentBase', (), {})()
            a.part_of_parallel_pool = False
            a.agent_id = 0
            agents.append(a)

        self.set.add(agents)
        self.assertEqual([agents], self.set._nested_store, msg="Not appending multiple items correctly")

    def test_str(self):

        a = type('AgentBase', (), {})()
        a.part_of_parallel_pool = False
        a.agent_id = 0

        self.set.add([a for _ in range(3)])
        str(self.set)

    def test_iterable(self):
        agents = []
        for _ in range(3):
            a = type('AgentBase', (), {})()
            a.part_of_parallel_pool = False
            a.agent_id = 0
            agents.append(a)

        self.set.add(agents)
        for _ in self.set:
            pass


if __name__ == "__main__":
    unittest.main()
