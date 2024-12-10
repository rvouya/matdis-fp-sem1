import unittest
from unittest.mock import patch
import pandas as pd
import itertools
import time
from io import StringIO

# Import functions from function.py file
from function import load_data, get_allowed_ranks, filter_players_by_rank, calculate_team_score, backtrack_matchmaking, display_matches

class TestMatchmaking(unittest.TestCase):

    @patch("builtins.open", new_callable=lambda: StringIO("username,mmr,region,latency,rank\nwpynner0,1314,CN,53,Iron\n"))
    def test_load_data(self, mock_file):
        # Simulate loading a dataset
        data = load_data("dummy.csv")
        
        # Check if the data is loaded correctly
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["username"], "wpynner0")
        self.assertEqual(data[0]["mmr"], 1314)
        self.assertEqual(data[0]["rank_numeric"], 1)  # Iron => 1
        self.assertEqual(data[0]["region"], "CN")

    def test_get_allowed_ranks(self):
        # Test if rank mapping returns correct allowed ranks
        self.assertEqual(get_allowed_ranks(1), [1, 2])  # Iron
        self.assertEqual(get_allowed_ranks(2), [1, 2, 3])  # Silver
        self.assertEqual(get_allowed_ranks(3), [2, 3, 4])  # Gold
        self.assertEqual(get_allowed_ranks(4), [3, 4])  # Platinum
        self.assertEqual(get_allowed_ranks(5), [])  # No such rank

    def test_filter_players_by_rank(self):
        # Test filtering players by rank
        players = [
            {"username": "player1", "rank_numeric": 1},
            {"username": "player2", "rank_numeric": 2},
            {"username": "player3", "rank_numeric": 3},
            {"username": "player4", "rank_numeric": 4}
        ]
        filtered = filter_players_by_rank(players, 2)  # Silver rank should include Iron and Silver
        self.assertEqual(len(filtered), 2)  # Only player1 and player2
        self.assertIn({"username": "player1", "rank_numeric": 1}, filtered)
        self.assertIn({"username": "player2", "rank_numeric": 2}, filtered)

    def test_calculate_team_score(self):
        # Test if team score calculation works correctly
        team = [
            {"username": "player1", "mmr": 1000},
            {"username": "player2", "mmr": 1200}
        ]
        score = calculate_team_score(team)
        self.assertEqual(score, 2200)

    @patch("itertools.combinations", return_value=[("player1", "player2"), ("player3", "player4")])
    def test_backtrack_matchmaking(self, mock_combinations):
        # Mocking combinations to return a predefined result
        players = [
            {"username": "player1", "rank_numeric": 1, "mmr": 1000},
            {"username": "player2", "rank_numeric": 2, "mmr": 1200},
            {"username": "player3", "rank_numeric": 1, "mmr": 1300},
            {"username": "player4", "rank_numeric": 2, "mmr": 1400}
        ]
        matches = backtrack_matchmaking(players, 1, 2, 2)
        
        self.assertEqual(len(matches), 2)  # 2 matches should be returned
        self.assertEqual(matches[0][2], 200)  # Skill difference between match 1
        self.assertEqual(matches[1][2], 100)  # Skill difference between match 2

    def test_display_matches(self):
        # We will test if the match details are displayed properly
        matches = [
            ([
                {"username": "player1", "mmr": 1000, "region": "CN", "rank": "Iron"},
                {"username": "player2", "mmr": 1200, "region": "KR", "rank": "Silver"}
            ], [
                {"username": "player3", "mmr": 1300, "region": "CN", "rank": "Gold"},
                {"username": "player4", "mmr": 1400, "region": "EU", "rank": "Platinum"}
            ], 100)
        ]
        with patch("builtins.print") as mocked_print:
            display_matches(matches)
            mocked_print.assert_called()

if __name__ == "__main__":
    unittest.main()
