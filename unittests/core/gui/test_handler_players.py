"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


import unittest
from pycman.core.gui.auxiliary.handler_players import HandlerPlayers


class TestHandlerPlayers(unittest.TestCase):
    def setUp(self):
        self.players = HandlerPlayers()

    def test_init(self):
        self.assertEqual(0, len(self.players), msg="Incorrect initialing")

    def test_get_player_name(self):
        self.players.human = dict()
        self.players.ai = dict()

        self.assertEqual("HUMAN_1", self.players._get_player_name("HUMAN"))
        self.assertEqual("AI_1", self.players._get_player_name("AI"))

        self.players.human = dict(HUMAN_1=None)
        self.assertEqual("HUMAN_2", self.players._get_player_name("HUMAN"))

        self.players.human = dict(HUMAN_2=None)
        self.assertEqual("HUMAN_1", self.players._get_player_name("HUMAN"))

        self.players.human = dict(HUMAN_1=None, HUMAN_2=None)

        with self.assertRaises(ValueError):
            self.players._get_player_name("HUMAN")

    def test_add_players_human_ai(self):
        self.players.add_player("HUMAN")
        self.players.add_player("AI")

        self.assertEqual(2, len(self.players), msg="Incorrect length")
        self.assertEqual("HUMAN_1",next(iter(self.players.human.keys())))
        self.assertEqual("AI_1", next(iter(self.players.ai.keys())))

        player = self.players.human["HUMAN_1"].get_config_value("HUMAN_1", "player", 0)
        keys = self.players.human["HUMAN_1"].get_config_value("HUMAN_1", "keys", 0)

        self.assertEqual("HUMAN", player, "Wrong initialization of HUMAN variables")
        self.assertEqual("KEYS_HUMAN_1", keys, "Wrong initialization of HUMAN variables")

        self.assertEqual("dict_keys(['HUMAN_1', 'AI_1'])", str(self.players.get_players().keys()),
                         msg="Get players not returning correctly")

        self.players.human = dict()
        self.players.ai = dict()

    def test_del_players_human_ai(self):
        self.players.human = dict(HUMAN_1=None, HUMAN_2=None)
        self.players.ai = dict(AI_1=None, AI_2=None)

        self.players.del_player("HUMAN_1")
        self.assertEqual("HUMAN_2", next(iter(self.players.human)),
                         msg="Incorrectly deletion of HUMAN")

        self.players.del_player("AI_1")
        self.assertEqual("AI_2", next(iter(self.players.ai)),
                         msg="Incorrectly deletion of AI")

        self.players.human = dict()
        self.players.ai = dict()

    def test_next_players(self):
        self.players.human = dict(HUMAN_1=None)
        self.players.ai = dict(AI_1=None)

        self.players.add_player("HUMAN")

        for answer in ["HUMAN_1", "HUMAN_2", "AI_1", "HUMAN_1"]:
            self.assertEqual(answer, self.players.get_player_next(), msg="Generator not working properly")


        self.players.del_player("HUMAN_1")
        for answer in ["HUMAN_2", "AI_1", "HUMAN_2", "AI_1"]:
            self.assertEqual(answer, self.players.get_player_next(), msg="Generator not working properly")

        self.players.human = dict()
        self.players.ai = dict()
