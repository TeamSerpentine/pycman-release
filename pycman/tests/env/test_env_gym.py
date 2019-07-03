"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

from pycman.env.env_gym import HandlerGym

import unittest


class TestHandlerGym(unittest.TestCase):

    def setUp(self):
        """ Set up a correct environment.  """
        self.game_name = "MsPacman-v0"
        self._gym = HandlerGym(self.game_name)

    def test_failed_setup(self):
        """ Check for an empty input.  """
        with self.assertRaises(ValueError):
            HandlerGym("")

    def test_failed_setup_2(self):
        """ Check if you get correct alternatives"""
        try:
            HandlerGym("MsPacman")
        except ValueError as err:
            # Note need extra space in front of the game names
            expected_alternatives = [" MsPacman-v4", " MsPacman-v0"]
            found_alternatives = str(err).split("\n")[1:]
            self.assertEqual(expected_alternatives, found_alternatives, msg="Alternatives are not properly projected")

    def test_pacman_game_id(self):
        """ Check if the game name is stored properly.  """
        self.assertEqual(self.game_name, self._gym.game_name,
                         msg="Wrong game ID loaded")

    def test_get_constants(self):
        # Count the number of allowed actions.
        self.assertEqual(9, self._gym.get_constants().output_shape)

        # See if all the actions are mapped correctly.
        correct = ['NOOP', 'UP', 'RIGHT', 'LEFT', 'DOWN', 'UPRIGHT', 'UPLEFT', 'DOWNRIGHT', 'DOWNLEFT']
        self.assertEqual(correct, self._gym.get_constants().action_meanings)

        # input shape
        self.assertEqual((210, 160, 3), self._gym.get_constants().input_shape)


    def test_pacman_step(self):
        """ Evaluate a single step. """
        obs, reward, done, info = self._gym.step(5)
        self.assertEqual((210, 160, 3), obs.shape, msg="Obs after step wrong dimensions")
        self.assertEqual(0, reward, msg="Rewards after step correctly")
        self.assertEqual(False, done, msg="Done after step correctly")
        self.assertEqual({'ale.lives': 3}, info, msg="Info after step correctly")
        self.assertEqual(5, self._gym.action, msg="Action after step correctly")

    def test_pycman_random_step_bounds(self):
        for _ in range(500):
            if not 0 <= self._gym.random_action() <= 9:
                raise ValueError("random action is not bounded correctly")

    def test_pacman_random_step(self):
        """ Evaluate if a random step is stored correctly.  """
        for _ in range(50):
            action = self._gym.random_action()
            self._gym.step(action)
            self.assertEqual(self._gym.action, action, msg="Action after step correctly")

    def test_reset_game(self):
        """ Evaluate if random values are restored to begin state.  """
        self._gym.action = 5
        self._gym.reset()
        self.assertEqual(self._gym.action, 0, msg="Action not init correctly")

    def test_set_action_empty_step(self):
        """ Evaluate that if the game is not receiving an input it well return action 0.  """
        for action in range(9):
            self._gym.step(action)
            self.assertEqual(action, self._gym.action_new, msg="Empty step not taken properly")


if __name__ == "__main__":
    unittest.main()
