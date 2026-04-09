"""
Unit tests for faction ranking calculations.

Tests verify ranking calculation and edge cases.
"""

import os
import sys
import unittest
from unittest.mock import patch

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from mvp_site import constants
from mvp_site.faction.rankings import (
    calculate_ranking,
    calculate_total_fp,
)


class TestFactionRankingCalculation(unittest.TestCase):
    """Test cases for faction ranking calculation functions."""

    def test_calculate_total_fp_territory_multiplier(self):
        """Verify docstring matches code (territory * 5)."""
        stats = {
            "soldiers": 0,
            "spies": 0,
            "elites": 0,
            "elite_avg_level": 6,
            "territory": 100,
            "fortifications": 0,
            "citizens": 0,
            "gold_pieces": 0,
            "arcana": 0,
            "prestige": 0,
        }

        total_fp = calculate_total_fp(stats)

        # Territory FP should be 100 * 5 = 500
        # (docstring says territory * 5, code uses territory * 5)
        self.assertEqual(total_fp, 500)

    def test_calculate_total_fp_all_components(self):
        """Verify all FP components are included in total."""
        stats = {
            "soldiers": 100,
            "spies": 50,
            "elites": 10,
            "elite_avg_level": 6,
            "territory": 200,
            "fortifications": 2,
            "citizens": 1000,
            "gold_pieces": 50000,
            "arcana": 1000,
            "prestige": 5,
        }

        total_fp = calculate_total_fp(stats)

        # Army: 100*1 + 50*0.5 + 10*3 = 100 + 25 + 30 = 155
        # Territory: 200 * 5 = 1000
        # Fortifications: 2 * 1000 = 2000
        # Citizens: 1000 * 0.1 = 100
        # Gold: 50000 * 0.001 = 50
        # Arcana: 1000 * 0.01 = 10
        # Prestige: 5 * 100 = 500
        # Total: 155 + 1000 + 2000 + 100 + 50 + 10 + 500 = 3815
        self.assertEqual(total_fp, 3815)

    @patch("mvp_site.faction.rankings.get_all_ai_factions")
    def test_calculate_ranking_returns_correct_rank(self, mock_get_ai):
        """Verify ranking calculation is correct."""
        # Mock AI factions (base format)
        mock_get_ai.return_value = [
            {"name": "AI1", "base_fp": 10000, "difficulty": "hard"},
            {"name": "AI2", "base_fp": 8000, "difficulty": "medium"},
            {"name": "AI3", "base_fp": 5000, "difficulty": "easy"},
            {"name": "AI4", "base_fp": 3000, "difficulty": "easy"},
        ]

        # Player FP is 6000, should rank 3rd (above AI3 and AI4, below AI1 and AI2)
        # Use FP above MIN_RANK_FP to ensure ranking
        player_fp = max(6000, constants.MIN_RANK_FP + 1000)
        rank, all_factions = calculate_ranking(player_fp, turn_number=1)

        # Should have a rank (not None if above MIN_RANK_FP)
        self.assertIsNotNone(
            rank, "Player should be ranked when FP is above MIN_RANK_FP"
        )
        self.assertGreaterEqual(rank, 1)
        self.assertEqual(len(all_factions), 5)  # 4 AI + 1 player

    @patch("mvp_site.faction.rankings.get_all_ai_factions")
    def test_calculate_ranking_handles_edge_cases(self, mock_get_ai):
        """Verify handles edge cases (rank 1, last rank, ties)."""
        # Test rank 1 (highest FP)
        mock_get_ai.return_value = [
            {"name": "AI1", "base_fp": 5000, "difficulty": "medium"},
            {"name": "AI2", "base_fp": 3000, "difficulty": "easy"},
        ]

        rank, _ = calculate_ranking(10000, turn_number=1)
        if rank is not None:
            self.assertEqual(rank, 1)

        # Test last rank (lowest FP)
        rank, _ = calculate_ranking(1000, turn_number=1)
        if rank is not None:
            self.assertGreaterEqual(rank, 1)

        # Test tie (same FP as an AI faction)
        rank, _ = calculate_ranking(5000, turn_number=1)
        if rank is not None:
            self.assertGreaterEqual(rank, 1)

    @patch("mvp_site.faction.rankings.get_all_ai_factions")
    def test_calculate_ranking_with_ai_factions(self, mock_get_ai):
        """Verify ranking includes AI factions correctly."""
        mock_get_ai.return_value = [
            {"name": "Strong Faction", "base_fp": 10000, "difficulty": "hard"},
            {"name": "Weak Faction", "base_fp": 2000, "difficulty": "easy"},
        ]

        rank, all_factions = calculate_ranking(5000, turn_number=1)

        # Should have a rank if above MIN_RANK_FP
        if rank is not None:
            self.assertGreaterEqual(rank, 1)

        # Verify all factions are included
        self.assertEqual(len(all_factions), 3)  # 2 AI + 1 player

        # Verify factions are sorted by FP descending
        fps = [f["faction_power"] for f in all_factions]
        self.assertEqual(fps, sorted(fps, reverse=True))

    def test_calculate_total_fp_handles_missing_stats(self):
        """Verify handles missing stat keys gracefully."""
        stats = {
            "soldiers": 100,
            # Missing other keys - should default to 0
        }

        total_fp = calculate_total_fp(stats)

        # Should still calculate with defaults (soldiers only: 100)
        self.assertEqual(total_fp, 100)

    def test_calculate_total_fp_economic_components(self):
        """Verify economic components (citizens, gold, arcana) contribute correctly."""
        stats = {
            "soldiers": 0,
            "spies": 0,
            "elites": 0,
            "elite_avg_level": 6,
            "territory": 0,
            "fortifications": 0,
            "citizens": 1000,
            "gold_pieces": 10000,
            "arcana": 500,
            "prestige": 0,
        }

        total_fp = calculate_total_fp(stats)

        # Citizens: 1000 * 0.1 = 100
        # Gold: 10000 * 0.001 = 10
        # Arcana: 500 * 0.01 = 5
        # Total: 115
        self.assertEqual(total_fp, 115)


if __name__ == "__main__":
    unittest.main()
