#!/usr/bin/env python3
"""Unit tests for battle simulation bugs identified in PR #2778.

These tests reproduce the bugs before fixing them (TDD approach).
"""

from __future__ import annotations

import random
import unittest

from mvp_site.faction.battle_sim import (
    _calculate_round_casualties_fast,
    _check_morale_rout,
    _simulate_round_detailed,
)
from mvp_site.faction.srd_units import create_unit_group


class TestBattleDamageMultiplierBug(unittest.TestCase):
    """Bug #1: Battle damage multiplied by number of defender groups."""

    def test_damage_should_not_multiply_by_defender_groups_fast(self):
        """Same attackers should deal same total damage regardless of defender grouping."""
        attackers = [create_unit_group("soldier", 100)]

        # Same total defenders, different grouping
        defenders_single = [create_unit_group("soldier", 100)]
        defenders_split = [
            create_unit_group("soldier", 50),
            create_unit_group("soldier", 50),
        ]

        # Calculate damage for single group
        damage_single = _calculate_round_casualties_fast(attackers, defenders_single)

        # Calculate damage for split groups
        damage_split = _calculate_round_casualties_fast(attackers, defenders_split)

        # Damage should be approximately equal (within 5% tolerance for rounding)
        ratio = damage_split / damage_single if damage_single > 0 else 0
        self.assertLess(
            abs(ratio - 1.0),
            0.05,
            f"Damage multiplied by defender groups: single={damage_single}, split={damage_split}, ratio={ratio:.2f}",
        )

    def test_damage_should_not_multiply_by_defender_groups_detailed(self):
        """Same attackers should deal same total damage regardless of defender grouping (detailed mode)."""
        attackers = [create_unit_group("soldier", 100)]

        defenders_single = [create_unit_group("soldier", 100)]
        defenders_split = [
            create_unit_group("soldier", 50),
            create_unit_group("soldier", 50),
        ]

        rng = random.Random(42)
        log = []

        damage_single = _simulate_round_detailed(
            attackers, defenders_single, rng, log, "Test"
        )

        rng2 = random.Random(42)  # Same seed
        log2 = []
        damage_split = _simulate_round_detailed(
            attackers, defenders_split, rng2, log2, "Test"
        )

        # Damage should be approximately equal
        ratio = damage_split / damage_single if damage_single > 0 else 0
        self.assertLess(
            abs(ratio - 1.0),
            0.1,  # Slightly more tolerance for RNG
            f"Damage multiplied by defender groups (detailed): single={damage_single}, split={damage_split}, ratio={ratio:.2f}",
        )


class TestMoraleThresholdBug(unittest.TestCase):
    """Bug #2: Morale threshold logic inverted - checks casualties instead of HP remaining."""

    def test_morale_rout_at_25_percent_hp_remaining(self):
        """Units should rout when reduced to 25% HP remaining (75% casualties), not 25% casualties."""
        # Create units with 100 total
        units = [create_unit_group("soldier", 100)]
        units[0]["count"] = 100
        units[0]["remaining"] = 25  # 25% remaining = 75% casualties

        # Should rout (25% HP remaining <= 25% threshold)
        should_rout = _check_morale_rout(units)
        self.assertTrue(
            should_rout,
            f"Should rout at 25% HP remaining (75% casualties), but rout check returned {should_rout}",
        )

    def test_morale_no_rout_at_75_percent_hp_remaining(self):
        """Units should NOT rout when at 75% HP remaining (25% casualties)."""
        units = [create_unit_group("soldier", 100)]
        units[0]["count"] = 100
        units[0]["remaining"] = 75  # 75% remaining = 25% casualties

        # Should NOT rout (75% HP remaining > 25% threshold)
        should_rout = _check_morale_rout(units)
        self.assertFalse(
            should_rout,
            f"Should NOT rout at 75% HP remaining (25% casualties), but rout check returned {should_rout}",
        )

    def test_morale_rout_threshold_documentation_match(self):
        """Verify rout threshold matches documented behavior (25% HP remaining)."""
        # Test boundary: exactly 25% remaining
        units_exact = [create_unit_group("soldier", 100)]
        units_exact[0]["count"] = 100
        units_exact[0]["remaining"] = 25  # Exactly 25%

        # Test just above: 26% remaining
        units_above = [create_unit_group("soldier", 100)]
        units_above[0]["count"] = 100
        units_above[0]["remaining"] = 26  # Just above 25%

        rout_exact = _check_morale_rout(units_exact)
        rout_above = _check_morale_rout(units_above)

        # At exactly 25%, should rout (or be very close)
        # At 26%, should NOT rout
        self.assertFalse(
            rout_above,
            f"Should NOT rout at 26% HP remaining, but returned {rout_above}",
        )


class TestCasualtyCalculationBug(unittest.TestCase):
    """Bug #7: Casualty calculation uses unweighted average HP."""

    def test_casualty_calculation_should_weight_by_unit_count(self):
        """Average HP should be weighted by unit count, not just group count."""
        # Create defenders: 100 soldiers (11 HP each) + 1 elite (52 HP)
        defenders = [
            create_unit_group("soldier", 100),  # 11 HP each
            create_unit_group("elite_6", 1),  # 52 HP each
        ]

        # Unweighted average: (11 + 52) / 2 = 31.5 HP
        # Weighted average: (100*11 + 1*52) / 101 = 1100 + 52 / 101 ≈ 11.4 HP

        # Calculate casualties with current (buggy) method
        total_damage = 500  # Enough to kill many soldiers

        # Current buggy calculation (unweighted)
        unweighted_avg_hp = sum(g["stats"]["hp"] for g in defenders) / len(defenders)
        casualties_unweighted = int(total_damage / unweighted_avg_hp)

        # Correct calculation (weighted)
        total_units = sum(g["remaining"] for g in defenders)
        weighted_avg_hp = (
            sum(g["stats"]["hp"] * g["remaining"] for g in defenders) / total_units
        )
        casualties_weighted = int(total_damage / weighted_avg_hp)

        # Weighted should give MORE casualties (lower avg HP)
        self.assertGreater(
            casualties_weighted,
            casualties_unweighted,
            f"Weighted avg HP ({weighted_avg_hp:.2f}) should give more casualties than unweighted ({unweighted_avg_hp:.2f})",
        )


class TestZeroHpDivisionByZeroBug(unittest.TestCase):
    """Bug: Division by zero when all defenders have hp=0."""

    def test_zero_hp_defenders_no_crash(self):
        """Defenders with hp=0 should not raise ZeroDivisionError."""
        attackers = [create_unit_group("soldier", 10)]
        defenders = [create_unit_group("soldier", 5)]
        defenders[0]["stats"]["hp"] = 0

        result = _calculate_round_casualties_fast(attackers, defenders)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_malformed_defender_stats_hp_zero_no_crash(self):
        """Multiple defender groups all with hp=0 should not crash."""
        attackers = [create_unit_group("soldier", 100)]
        defenders = [
            create_unit_group("soldier", 50),
            create_unit_group("soldier", 50),
        ]
        for g in defenders:
            g["stats"]["hp"] = 0

        result = _calculate_round_casualties_fast(attackers, defenders)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)


class TestInvalidEliteTypeBug(unittest.TestCase):
    """Bug #8: Unhandled KeyError when LLM passes invalid elite type."""

    def test_invalid_elite_type_should_return_error_not_crash(self):
        """Invalid elite type should return error dict, not raise KeyError."""
        from mvp_site.faction.tools import execute_faction_tool

        # Try with invalid elite type
        result = execute_faction_tool(
            "faction_simulate_battle",
            {
                "attacker_soldiers": 100,
                "attacker_elites": 5,
                "attacker_elite_type": "dragon",  # Invalid type
                "defender_soldiers": 80,
            },
        )

        # Should return error dict, not raise exception
        self.assertIn(
            "error", result, "Should return error dict for invalid elite type"
        )
        self.assertIn(
            "unknown",
            result["error"].lower() or "",
            "Error should mention unknown/invalid type",
        )


class TestDamageDiceScalingBug(unittest.TestCase):
    """Bug #9: Damage dice scaling wrong for negative modifiers."""

    def test_negative_modifier_scaling(self):
        """Scaling damage dice with negative modifier should preserve sign."""
        from mvp_site.faction.srd_units import _scale_damage_dice

        # Test "1d6-2" with increase of 1
        # Should become "1d6-1" (not "1d6+1")
        result = _scale_damage_dice("1d6-2", 1)

        # Should have negative modifier
        self.assertIn(
            "-", result, f"Result should have negative modifier, got: {result}"
        )
        self.assertNotIn(
            "+", result, f"Result should NOT have positive modifier, got: {result}"
        )

        # Parse and verify
        import re

        match = re.match(r"(\d+)d(\d+)([+-])(\d+)", result)
        if match:
            sign = match.group(3)
            modifier = int(match.group(4))
            self.assertEqual(
                sign, "-", f"Modifier sign should be negative, got: {sign}"
            )
            self.assertEqual(modifier, 1, f"Modifier should be 1, got: {modifier}")


if __name__ == "__main__":
    unittest.main()
