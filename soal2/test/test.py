import unittest
import pandas as pd
from matchmaking import load_data, get_allowed_ranks, filter_players_by_rank, calculate_team_score, backtrack_matchmaking

class TestMatchmaking(unittest.TestCase):
    def setUp(self):
        # Load data langsung dari file CSV
        self.data = load_data("soal-2_dataset.csv")
    
    def test_load_data(self):
        self.assertTrue(len(self.data) > 0)  # Data tidak boleh kosong
        self.assertIn("mmr", self.data[0])  # Kolom 'mmr' harus ada
        self.assertIn("rank_numeric", self.data[0])  # Kolom 'rank_numeric' harus ada
    
    def test_get_allowed_ranks(self):
        self.assertEqual(get_allowed_ranks(1), [1, 2])
        self.assertEqual(get_allowed_ranks(2), [1, 2, 3])
        self.assertEqual(get_allowed_ranks(3), [2, 3, 4])
        self.assertEqual(get_allowed_ranks(4), [3, 4])
        self.assertEqual(get_allowed_ranks(5), [])  # Rank tidak valid
    
    def test_filter_players_by_rank(self):
        base_rank = 3  # Gold
        filtered_players = filter_players_by_rank(self.data, base_rank)
        allowed_ranks = get_allowed_ranks(base_rank)
        for player in filtered_players:
            self.assertIn(player["rank_numeric"], allowed_ranks)
    
    def test_calculate_team_score(self):
        team = [
            {"username": "player1", "mmr": 1500},
            {"username": "player2", "mmr": 1400},
            {"username": "player3", "mmr": 1600},
        ]
        self.assertEqual(calculate_team_score(team), 4500)
    
    def test_backtrack_matchmaking(self):
        base_rank = 3  # Gold
        team_size = 2
        match_count = 1
        matches = backtrack_matchmaking(self.data, base_rank, team_size, match_count)
        self.assertTrue(len(matches) > 0)
        for team1, team2, skill_diff in matches:
            self.assertEqual(len(team1), team_size)
            self.assertEqual(len(team2), team_size)

if __name__ == "__main__":
    unittest.main()
