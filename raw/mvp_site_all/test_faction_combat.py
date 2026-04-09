"""
Unit tests for faction combat power calculations.

Tests verify the faction power calculation formula and edge cases.
"""

import os
import sys
import unittest

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from mvp_site.faction.combat import calculate_faction_power


class TestFactionPowerCalculation(unittest.TestCase):
    """Test cases for calculate_faction_power function."""

    def test_calculate_faction_power_territory_multiplier(self):
        """Verify territory FP = territory * 5 (not * 10)."""
        # Test with territory only (no units)
        fp = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=0,
            territory=100,
            fortifications=0,
        )

        # Should be 100 * 5 = 500
        self.assertEqual(fp, 500)

    def test_calculate_faction_power_soldiers(self):
        """Verify soldiers contribute 1x FP each."""
        fp = calculate_faction_power(
            soldiers=100,
            spies=0,
            elites=0,
            territory=0,
            fortifications=0,
        )

        # Should be 100 * 1.0 = 100
        self.assertEqual(fp, 100)

    def test_calculate_faction_power_spies(self):
        """Verify spies contribute 0.5x FP each."""
        fp = calculate_faction_power(
            soldiers=0,
            spies=100,
            elites=0,
            territory=0,
            fortifications=0,
        )

        # Should be 100 * 0.5 = 50
        self.assertEqual(fp, 50)

    def test_calculate_faction_power_elites(self):
        """Verify elites contribute 3x FP each (at level 6)."""
        fp = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=10,
            elite_avg_level=6,
            territory=0,
            fortifications=0,
        )

        # Should be 10 * 3.0 = 30
        self.assertEqual(fp, 30)

    def test_calculate_faction_power_elites_level_bonus(self):
        """Verify elites get level bonus above level 6."""
        fp_level_6 = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=10,
            elite_avg_level=6,
            territory=0,
            fortifications=0,
        )

        fp_level_10 = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=10,
            elite_avg_level=10,
            territory=0,
            fortifications=0,
        )

        # Level 10 should have higher FP than level 6
        self.assertGreater(fp_level_10, fp_level_6)
        # Level 10 bonus: 1.0 + (10-6)*0.1 = 1.4
        # Expected: 10 * 3.0 * 1.4 = 42
        self.assertEqual(fp_level_10, 42)

    def test_calculate_faction_power_total_calculation(self):
        """Verify total FP calculation is correct."""
        fp = calculate_faction_power(
            soldiers=100,
            spies=50,
            elites=10,
            elite_avg_level=6,
            territory=200,
            fortifications=2,
        )

        # Soldiers: 100 * 1.0 = 100
        # Spies: 50 * 0.5 = 25
        # Elites: 10 * 3.0 = 30
        # Territory: 200 * 5 = 1000
        # Fortifications: 2 * 1000 = 2000
        # Total: 100 + 25 + 30 + 1000 + 2000 = 3155
        self.assertEqual(fp, 3155)

    def test_calculate_faction_power_handles_missing_units(self):
        """Verify handles missing unit types gracefully."""
        # Test with only soldiers
        fp_soldiers = calculate_faction_power(
            soldiers=100,
            spies=0,
            elites=0,
            territory=0,
            fortifications=0,
        )
        self.assertEqual(fp_soldiers, 100)

        # Test with only spies
        fp_spies = calculate_faction_power(
            soldiers=0,
            spies=100,
            elites=0,
            territory=0,
            fortifications=0,
        )
        self.assertEqual(fp_spies, 50)

        # Test with only elites
        fp_elites = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=10,
            territory=0,
            fortifications=0,
        )
        self.assertEqual(fp_elites, 30)

    def test_calculate_faction_power_handles_zero_values(self):
        """Verify handles zero territory/units correctly."""
        fp = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=0,
            territory=0,
            fortifications=0,
        )

        self.assertEqual(fp, 0)

    def test_calculate_faction_power_base_stats_multiplier(self):
        """Verify base_stats attack/defense multipliers work correctly."""
        fp_default = calculate_faction_power(
            soldiers=100,
            spies=0,
            elites=0,
            territory=0,
            fortifications=0,
        )

        fp_with_stats = calculate_faction_power(
            soldiers=100,
            spies=0,
            elites=0,
            territory=0,
            fortifications=0,
            base_stats={"attack": 1.5, "defense": 1.2},
        )

        # With attack=1.5 and defense=1.2, multiplier = 1.5 * 1.2 = 1.8
        # Expected: 100 * 1.0 * 1.8 = 180
        self.assertEqual(fp_with_stats, 180)
        self.assertGreater(fp_with_stats, fp_default)

    def test_calculate_faction_power_fortifications(self):
        """Verify fortifications contribute 1000 FP each."""
        fp = calculate_faction_power(
            soldiers=0,
            spies=0,
            elites=0,
            territory=0,
            fortifications=3,
        )

        # Should be 3 * 1000 = 3000
        self.assertEqual(fp, 3000)


if __name__ == "__main__":
    unittest.main()
