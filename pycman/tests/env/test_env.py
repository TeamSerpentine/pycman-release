"""
    Date created: 2019/07/03
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import unittest
from pycman.env.env import *
import gym
import pycman

class TestEnv(unittest.TestCase):

    def test_gym_make(self):
        """ Tests the pycman.env.step function. """
        pycman.env.gym('CartPole-v0')
        env = pycman.env.get()
        base = gym.make('CartPole-v0')

        env.reset()
        base.reset()

        obs, rew, done, inf = env.step(0)
        obs1, rew1, done1, inf1 = env.step(0)

        assert obs.size == obs1.size
        assert rew == rew1
        assert done == done1
        assert inf == inf1

        env.close()
        base.close()

    def test_reset(self):
        """ Tests the pycman.env.reset function. """
        pycman.env.gym('CartPole-v0')
        env = pycman.env.get()
        assert env._env._elapsed_steps == 0
        env.step(0)
        env.step(0)
        assert env._env._elapsed_steps == 2
        env.reset()
        assert env._env._elapsed_steps == 0

    def test_info(self):
        """ Tests the pycman.env.test_get_constants function. """
        pycman.env.gym('CartPole-v0')
        env = pycman.env.get()
        info_a = pycman.env.info()
        info_b = env.info()
        assert info_a == info_b

    def test_functions(self):
        """ Tests all the abstract functions whether they cause crashes. """
        pycman.env.gym('CartPole-v0')
        env = pycman.env.get()
        env.reset()
        env.step(0)
        env.info()
        env.render()
        env.close()


if __name__ == "__main__":
    unittest.main()
