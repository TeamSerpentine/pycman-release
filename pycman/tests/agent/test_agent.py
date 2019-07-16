"""
    Date created: 2019/07/03
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import unittest
import pycman
from pycman.core.agent.agent import Agent
from pycman.core.agent.global_agents import GlobalAgentSet


class EmptyAgent(Agent):

    def __init__(self):
        self.games_played = 0
        self.finished = False

    def run(self, env, max_threads=1):
        for _ in range(3):
            env.reset()
            done = False
            while not done:
                obs, reward, done, info = env.step(env.random_action())
            self.games_played += 1
        self.finished = True


def reset():
    pycman.env = pycman.core.env.global_env.GlobalEnv()
    pycman.agent = pycman.core.agent.global_agents.GlobalAgentSet()
    pycman.run = pycman.core.run.run.Run(pycman.agent, pycman.env).run


class TestAgent(unittest.TestCase):

    def test_add(self):
        """ Tests the pycman.agent.add function. """
        reset()
        pycman.agent.add([EmptyAgent()])
        assert (len(pycman.agent) == 1)

    def test_add_multiple(self):
        """" Tests the pycman.agent.add function for multiple agents. """
        reset()
        pycman.agent.add([EmptyAgent()] * 10)
        assert (len(pycman.agent) == 10)

    def test_play_game(self):
        """" Run a game and see if it actually finishes. """
        reset()

        agents = [EmptyAgent()]
        pycman.env.gym("Breakout-v0")
        pycman.agent.add(agents)
        pycman.run()

        assert pycman.agent[0].finished
        assert pycman.agent[0].games_played == 3

    def test_play_game_multi(self):
        """" Run a game and see if it actually finishes. """
        reset()

        agents = [EmptyAgent() for _ in range(4)]
        pycman.env.gym("Breakout-v0")
        pycman.agent.add(agents)
        pycman.run(order='parallel')

        result_agents = pycman.agent
        for a in result_agents:
            assert a.finished
            assert a.games_played == 3

        for a in agents:
            assert a.finished
            assert a.games_played == 3

    def test_play_game_sequential(self):
        """" Run a game and see if it actually finishes. """
        reset()

        agents = [EmptyAgent() for _ in range(4)]
        pycman.env.gym("Breakout-v0")
        pycman.agent.add(agents)
        pycman.run(order='sequential')

        for a in pycman.agent:
            assert a.finished
            assert a.games_played == 3

    def test_agent_references_sequential(self):
        """" Run a game and see if it actually finishes. """
        reset()

        agents = [EmptyAgent() for _ in range(4)]
        pycman.env.gym("Breakout-v0")
        pycman.agent.add(agents)
        pycman.run(order='sequential')

        for a, b in zip(pycman.agent, agents):
            assert a is b

    def test_agent_references_multi(self):
        """" Run a game and see if it actually finishes. """
        reset()

        agents = [EmptyAgent() for _ in range(4)]
        pycman.env.gym("Breakout-v0")
        pycman.agent.add(agents)
        pycman.run(order='parallel')

        for a, b in zip(pycman.agent, agents):
            assert a is b


if __name__ == "__main__":
    unittest.main()
