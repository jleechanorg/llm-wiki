import os
import re
import unittest
from unittest.mock import patch

import pytest

# ruff: noqa: PT009
from mvp_site import agent_prompts, constants, dice_strategy, logging_util, world_time
from mvp_site.agent_prompts import (
    PromptBuilder,
    _load_instruction_file,
    _loaded_instructions_cache,
)
from mvp_site.agents import (
    StoryModeAgent,
)
from mvp_site.game_state import GameState
from mvp_site.llm_providers.provider_utils import strip_tool_requests_dice_instructions


class TestPromptLoading(unittest.TestCase):
    def setUp(self):
        """Clear the instruction cache before each test to ensure isolation."""
        _loaded_instructions_cache.clear()

    def test_all_prompts_are_loadable_via_service(self):
        """
        Ensures that all referenced prompt files can be loaded successfully
        by calling the actual _load_instruction_file function.
        """
        if logging_util:
            logging_util.info(
                "--- Running Test: test_all_prompts_are_loadable_via_service ---"
            )

        if not agent_prompts or not _load_instruction_file:
            self.skipTest("agent_prompts or _load_instruction_file not available")

        for p_type in agent_prompts.PATH_MAP:
            content = _load_instruction_file(p_type)
            assert isinstance(content, str)
            assert len(content) > 0, f"Prompt file for {p_type} should not be empty."

    def test_loading_unknown_prompt_raises_error(self):
        """
        Ensures that calling _load_instruction_file with an unknown type
        correctly raises a ValueError, following the strict loading policy.
        """
        if not pytest or not _load_instruction_file:
            self.skipTest("pytest or _load_instruction_file not available")

        if logging_util:
            logging_util.info(
                "--- Running Test: test_loading_unknown_prompt_raises_error ---"
            )
        with pytest.raises(ValueError, match="Unknown instruction type requested"):
            _load_instruction_file("this_is_not_a_real_prompt_type")

    def test_all_prompt_files_are_registered_in_service(self):
        """
        Ensures that every .md file in the prompts directory is registered
        in the agent_prompts.path_map, and vice-versa. This prevents
        un-loaded or orphaned prompt files.
        """
        if not agent_prompts:
            self.skipTest("agent_prompts not available")

        if logging_util:
            logging_util.info(
                "--- Running Test: test_all_prompt_files_are_registered_in_service ---"
            )

        prompts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "prompts"
        )

        # 1. Get all .md files from the filesystem (including subdirectories, excluding README files)
        # Also exclude _code_execution.md variants which are loaded dynamically by load_dice_instructions()
        try:
            disk_files = set()
            for _root, _dirs, files in os.walk(prompts_dir):
                for f in files:
                    if not f.endswith(".md"):
                        continue
                    if f.lower() == "readme.md":
                        continue
                    if f.endswith("_code_execution.md"):
                        continue
                    disk_files.add(f)
        except OSError:
            self.fail(f"Prompts directory not found at {prompts_dir}")

        # 2. Get all file basenames from the service's path_map
        # Exclude _code_execution.md variants (same as disk_files filtering)
        service_files = {
            os.path.basename(p)
            for p in agent_prompts.PATH_MAP.values()
            if not os.path.basename(p).endswith("_code_execution.md")
        }

        # 3. Compare the sets
        unregistered_files = disk_files - service_files
        assert len(unregistered_files) == 0, (
            f"Found .md files in prompts/ dir not registered in agent_prompts.path_map: {unregistered_files}"
        )

        missing_files = service_files - disk_files
        assert len(missing_files) == 0, (
            f"Found files in agent_prompts.path_map that do not exist in prompts/: {missing_files}"
        )

    def test_all_registered_prompts_are_actually_used(self):  # noqa: PLR0912, PLR0915
        """
        Ensures that every prompt registered in PATH_MAP is actually used
        somewhere in the codebase. This prevents dead/unused prompts.
        """
        if not agent_prompts or not constants:
            self.skipTest("agent_prompts or constants not available")

        if logging_util:
            logging_util.info(
                "--- Running Test: test_all_registered_prompts_are_actually_used ---"
            )

        # Get all prompt types from PATH_MAP
        prompt_types = set(agent_prompts.PATH_MAP.keys())

        # Create reverse mapping from constant values to constant names
        # by inspecting the constants module
        prompt_to_constant = {}
        for attr_name in dir(constants):
            if attr_name.startswith("PROMPT_TYPE_"):
                attr_value = getattr(constants, attr_name)
                if isinstance(attr_value, str):  # Only include string constants
                    prompt_to_constant[attr_value] = attr_name

        # Search for usage of each prompt type in the codebase
        codebase_dir = os.path.dirname(os.path.dirname(__file__))
        unused_prompts = set()

        for prompt_type in prompt_types:
            # Check if prompt type is used anywhere in Python files
            found_usage = False
            constant_name = prompt_to_constant.get(
                prompt_type, f"PROMPT_TYPE_{prompt_type.upper()}"
            )

            # Search through Python files for usage
            for root, _dirs, files in os.walk(codebase_dir):
                # Skip test directories and __pycache__
                # More specific: only skip if the directory name itself starts with 'test' or is __pycache__
                basename = os.path.basename(root)
                if basename.startswith("test") or basename == "__pycache__":
                    continue

                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, encoding="utf-8") as f:
                                content = f.read()
                                # Look for the prompt type constant being used or the literal value
                                if (
                                    constant_name in content
                                    or f"'{prompt_type}'" in content
                                    or f'"{prompt_type}"' in content
                                ):
                                    found_usage = True
                                    break
                        except (UnicodeDecodeError, PermissionError):
                            continue

                if found_usage:
                    break

            if not found_usage:
                unused_prompts.add(prompt_type)

        # This test should pass now that we're looking for the right patterns
        assert len(unused_prompts) == 0, (
            f"Found prompt types registered in PATH_MAP but not used in codebase: {unused_prompts}"
        )

        # Also verify that prompt types are actually called via _load_instruction_file
        # This is a more specific check for actual loading via constants
        used_in_loading = set()

        # Check if agent_prompts.py path calculation is correct
        agent_prompts_path = os.path.join(codebase_dir, "agent_prompts.py")
        if not os.path.exists(agent_prompts_path) and logging_util:
            logging_util.warning(f"agent_prompts.py not found at {agent_prompts_path}")

        # Search for _load_instruction_file calls with constants
        for root, _dirs, files in os.walk(codebase_dir):
            # Skip test directories and __pycache__
            basename = os.path.basename(root)
            if basename.startswith("test") or basename == "__pycache__":
                continue

            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, encoding="utf-8") as f:
                            content = f.read()
                            # Look for _load_instruction_file calls with constants
                            if (
                                "_load_instruction_file(constants.PROMPT_TYPE_"
                                in content
                            ):
                                # Extract the constant names used in _load_instruction_file calls

                                matches = re.findall(
                                    r"_load_instruction_file\(constants\.(PROMPT_TYPE_\w+)\)",
                                    content,
                                )
                                for match in matches:
                                    # Get the actual constant value
                                    if hasattr(constants, match):
                                        constant_value = getattr(constants, match)
                                        if constant_value in prompt_types:
                                            used_in_loading.add(constant_value)

                            # Also check for dynamic loading in loops
                            # Look for patterns like: for p_type in [...]: _load_instruction_file(p_type)
                            if (
                                "for p_type in" in content
                                and "_load_instruction_file(p_type)" in content
                            ):
                                # This indicates dynamic loading - check the context
                                lines = content.split("\n")
                                for i, line in enumerate(lines):
                                    if "_load_instruction_file(p_type)" in line:
                                        # Look backwards for the loop definition
                                        for j in range(max(0, i - 10), i):
                                            if "for p_type in" in lines[j]:
                                                # Check if it mentions prompt types
                                                if "selected_prompts" in lines[j]:
                                                    # Mark narrative and mechanics as used (they're in selected_prompts)
                                                    used_in_loading.add("narrative")
                                                    used_in_loading.add("mechanics")
                                                elif "prompt_order" in lines[j]:
                                                    # Also check prompt_order list
                                                    used_in_loading.add("narrative")
                                                    used_in_loading.add("mechanics")
                                                break
                    except (UnicodeDecodeError, PermissionError):
                        continue

        # Define prompts that are loaded conditionally (not always loaded)
        conditional_prompts = set()
        if constants:
            conditional_prompts = {
                constants.PROMPT_TYPE_NARRATIVE,  # Only when narrative selected
                constants.PROMPT_TYPE_MECHANICS,  # Only when mechanics selected
                constants.PROMPT_TYPE_CHARACTER_TEMPLATE,  # Only when narrative is selected
                constants.PROMPT_TYPE_RELATIONSHIP,  # Dynamic: loaded on LLM request
                constants.PROMPT_TYPE_REPUTATION,  # Dynamic: loaded on LLM request
                constants.PROMPT_TYPE_GAME_STATE_EXAMPLES,  # Dynamic: loaded on LLM request
                constants.PROMPT_TYPE_DIALOG,  # Only when DialogAgent is used
                constants.PROMPT_TYPE_NARRATIVE_LITE,  # Only when DialogAgent is used
                constants.PROMPT_TYPE_NARRATIVE,  # Only when DialogAgent is used
                constants.PROMPT_TYPE_SPICY_MODE,  # Only when SpicyModeAgent is used
                constants.PROMPT_TYPE_FACTION_MINIGAME,  # Only when faction minigame enabled
                constants.PROMPT_TYPE_DIVINE_ASCENSION,  # Only when divine tier unlocked
                constants.PROMPT_TYPE_DIVINE_SYSTEM,  # Only when divine tier active
                constants.PROMPT_TYPE_SOVEREIGN_ASCENSION,  # Only when multiverse tier unlocked
                constants.PROMPT_TYPE_SOVEREIGN_SYSTEM,  # Only when multiverse tier active
                constants.PROMPT_TYPE_DICE_CODE_EXECUTION,  # Only for code_execution strategy
                constants.PROMPT_TYPE_DEFERRED_REWARDS,  # Only at specific turn intervals
                constants.PROMPT_TYPE_LEVEL_UP,  # Only when LevelUpAgent is used
            }

        # Separate always-loaded vs conditional prompts
        always_loaded_prompts = prompt_types - conditional_prompts
        not_loaded_always = always_loaded_prompts - used_in_loading

        # All always-loaded prompts should be found
        assert len(not_loaded_always) == 0, (
            f"Found always-loaded prompt types that are never loaded: {not_loaded_always}"
        )

        # Conditional prompts should be loaded when conditions are met
        conditional_prompts - used_in_loading

        # Verify conditional prompts are at least referenced in conditional logic
        conditional_referenced = set()
        for root, _dirs, files in os.walk(codebase_dir):
            # Skip test directories and __pycache__
            basename = os.path.basename(root)
            if basename.startswith("test") or basename == "__pycache__":
                continue

            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, encoding="utf-8") as f:
                            content = f.read()
                            # Look for conditional loading patterns
                            for prompt_type in conditional_prompts:
                                constant_name = prompt_to_constant.get(
                                    prompt_type, f"PROMPT_TYPE_{prompt_type.upper()}"
                                )
                                # Check various conditional patterns
                                if (
                                    (
                                        "in selected_prompts" in content
                                        and constant_name in content
                                    )
                                    or (
                                        f"constants.{constant_name} in selected_prompts"
                                        in content
                                    )
                                    or (
                                        f"{constant_name} in selected_prompts"
                                        in content
                                    )
                                ):
                                    conditional_referenced.add(prompt_type)
                                # Also check character_template special case
                                if (
                                    prompt_type == "character_template"
                                    and "PROMPT_TYPE_NARRATIVE in selected_prompts"
                                    in content
                                    and "_load_instruction_file(constants.PROMPT_TYPE_CHARACTER_TEMPLATE)"
                                    in content
                                ):
                                    conditional_referenced.add(prompt_type)
                    except (UnicodeDecodeError, PermissionError):
                        continue

        unreferenced_conditionals = conditional_prompts - conditional_referenced
        assert len(unreferenced_conditionals) == 0, (
            f"Found conditional prompt types that are not referenced in conditional logic: {unreferenced_conditionals}"
        )

        print(
            f"✓ Always-loaded prompts: {len(always_loaded_prompts - not_loaded_always)}/{len(always_loaded_prompts)} verified"
        )
        print(
            f"✓ Conditional prompts: {len(conditional_referenced)}/{len(conditional_prompts)} properly referenced"
        )

    @patch("mvp_site.agent_prompts._build_debug_instructions")
    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_build_rewards_mode_instructions_order(self, mock_load, mock_debug):
        """Rewards mode builder loads prompts in the expected order."""

        def side_effect(prompt_type):
            return f"PROMPT:{prompt_type}"

        mock_load.side_effect = side_effect
        mock_debug.return_value = "DEBUG"

        builder = agent_prompts.PromptBuilder(None)
        parts = builder.build_rewards_mode_instructions()

        expected = [
            f"PROMPT:{constants.PROMPT_TYPE_MASTER_DIRECTIVE}",
            f"PROMPT:{constants.PROMPT_TYPE_GAME_STATE}",
            f"PROMPT:{constants.PROMPT_TYPE_PLANNING_PROTOCOL}",
            f"PROMPT:{constants.PROMPT_TYPE_REWARDS}",
            f"PROMPT:{constants.PROMPT_TYPE_DND_SRD}",
            f"PROMPT:{constants.PROMPT_TYPE_MECHANICS}",
            "DEBUG",
        ]

        assert parts == expected
        assert [call.args[0] for call in mock_load.call_args_list] == [
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
            constants.PROMPT_TYPE_REWARDS,
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
        ]
        mock_debug.assert_called_once()

class TestDuplicateDiceLoading(unittest.TestCase):
    """Test that dice instructions are never loaded twice.

    The SystemInstructionBuilder.build_from_order() method has multiple points
    where dice instructions can be loaded (after MASTER_DIRECTIVE, GAME_STATE,
    MECHANICS, or COMBAT). The dice_loaded flag should prevent duplicate loading.
    """

    @patch("mvp_site.agent_prompts.load_dice_instructions")
    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_code_execution_combat_agent_loads_dice_once(
        self, mock_load_file, mock_load_dice
    ):
        """CombatAgent with code_execution loads dice exactly once via build_from_order.

        For code_execution strategy, build_from_order should still load dice guidance once
        to ensure instructions are present when this builder is used directly in tests or
        contexts that do not apply provider-level injection.
        """
        mock_load_file.side_effect = lambda pt: f"PROMPT:{pt}"
        mock_load_dice.return_value = "DICE_INSTRUCTIONS"

        # CombatAgent's prompt order
        combat_prompt_order = (
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
            constants.PROMPT_TYPE_COMBAT,
            constants.PROMPT_TYPE_NARRATIVE,
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
        )

        builder = agent_prompts.PromptBuilder(None)
        parts = builder.build_from_order(
            prompt_order=combat_prompt_order,
            dice_roll_strategy=dice_strategy.DICE_STRATEGY_CODE_EXECUTION,
            include_debug=False,
        )

        # Dice should be loaded once for deterministic prompt completeness.
        dice_count = sum(1 for p in parts if p == "DICE_INSTRUCTIONS")
        self.assertEqual(
            dice_count,
            1,
            f"build_from_order must add dice guidance exactly once for code_execution. "
            f"Found {dice_count} occurrence(s). Parts: {[i for i, p in enumerate(parts) if 'DICE' in p]}",
        )
        self.assertEqual(mock_load_dice.call_count, 1)

    @patch("mvp_site.agent_prompts.load_dice_instructions")
    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_all_prompt_orders_load_dice_at_most_once(
        self, mock_load_file, mock_load_dice
    ):
        """No prompt order should ever load dice instructions more than once.

        This is a generic test that covers any prompt order configuration.
        """
        mock_load_file.side_effect = lambda pt: f"PROMPT:{pt}"
        mock_load_dice.return_value = "DICE_INSTRUCTIONS"

        # Test various prompt orders that include dice-loading triggers
        prompt_orders = [
            # CombatAgent order
            (
                constants.PROMPT_TYPE_MASTER_DIRECTIVE,
                constants.PROMPT_TYPE_GAME_STATE,
                constants.PROMPT_TYPE_PLANNING_PROTOCOL,
                constants.PROMPT_TYPE_COMBAT,
                constants.PROMPT_TYPE_NARRATIVE,
                constants.PROMPT_TYPE_DND_SRD,
                constants.PROMPT_TYPE_MECHANICS,
            ),
            # StoryAgent order (has game_state and mechanics)
            (
                constants.PROMPT_TYPE_MASTER_DIRECTIVE,
                constants.PROMPT_TYPE_GAME_STATE,
                constants.PROMPT_TYPE_PLANNING_PROTOCOL,
                constants.PROMPT_TYPE_NARRATIVE,
                constants.PROMPT_TYPE_DND_SRD,
                constants.PROMPT_TYPE_MECHANICS,
            ),
        ]

        for prompt_order in prompt_orders:
            mock_load_dice.reset_mock()
            builder = agent_prompts.PromptBuilder(None)
            parts = builder.build_from_order(
                prompt_order=prompt_order,
                dice_roll_strategy=dice_strategy.DICE_STRATEGY_CODE_EXECUTION,
                include_debug=False,
            )

            dice_count = sum(1 for p in parts if p == "DICE_INSTRUCTIONS")
            self.assertLessEqual(
                dice_count,
                1,
                f"Dice instructions loaded {dice_count} times for order {prompt_order}",
            )


class TestDiceInstructionMarkers(unittest.TestCase):
    """DICE-ktu: Validate tool_requests dice instructions have proper markers.

    When code_execution mode is active, strip_tool_requests_dice_instructions()
    removes content between BEGIN_TOOL_REQUESTS_DICE and END_TOOL_REQUESTS_DICE
    markers. Any tool_requests dice guidance NOT wrapped in these markers will
    leak into code_execution prompts, creating conflicting instructions.
    """

    # Patterns that indicate tool_requests dice guidance
    TOOL_REQUESTS_DICE_PATTERNS = [
        r"tool_requests.*roll_attack",
        r"tool_requests.*roll_damage",
        r"tool_requests.*roll_saving",
        r"tool_requests.*roll_skill",
        r"MANDATORY.*tool_requests.*dice",
        r"REQUIRE.*tool_requests.*roll",
        r'"tool":\s*"roll_attack"',
        r'"tool":\s*"roll_saving_throw"',
        r'"tool":\s*"roll_skill_check"',
    ]

    def test_tool_requests_dice_instructions_are_marked(  # noqa: PLR0912
        self,
    ):
        """Ensure all tool_requests dice instructions are wrapped in markers.

        This prevents DICE-ktu: conflicting dice instructions in code_execution mode.
        """
        prompts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "prompts"
        )

        violations = []

        for root, _dirs, files in os.walk(prompts_dir):
            for filename in files:
                if not filename.endswith(".md"):
                    continue
                # Skip code_execution variants - they're for code_execution mode only
                if "_code_execution.md" in filename:
                    continue
                # Skip README files
                if filename.lower() == "readme.md":
                    continue
                # Skip dice_system_instruction.md - it's the SOURCE for tool_requests dice
                # (only loaded for native_two_phase strategy, not code_execution)
                if filename == "dice_system_instruction.md":
                    continue
                # Skip example files - they show JSON format, not instructions
                if "example" in filename.lower():
                    continue

                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, encoding="utf-8") as f:
                        content = f.read()
                except (UnicodeDecodeError, PermissionError):
                    continue

                # Check each pattern
                for pattern in self.TOOL_REQUESTS_DICE_PATTERNS:
                    matches = list(re.finditer(pattern, content, re.IGNORECASE))
                    for match in matches:
                        # Check if this match is inside BEGIN/END markers
                        match_pos = match.start()

                        # Find the last BEGIN marker before this position
                        begin_pattern = r"<!--\s*BEGIN_TOOL_REQUESTS_DICE"
                        end_pattern = r"<!--\s*END_TOOL_REQUESTS_DICE"

                        # Check if we're between BEGIN and END markers
                        begin_matches = list(
                            re.finditer(begin_pattern, content[:match_pos])
                        )
                        end_matches = list(
                            re.finditer(end_pattern, content[:match_pos])
                        )

                        # We're inside markers if there's a BEGIN after the last END
                        # (or if there's a BEGIN and no END before our position)
                        inside_markers = False
                        if begin_matches:
                            last_begin = begin_matches[-1].end()
                            last_end = end_matches[-1].end() if end_matches else 0
                            if last_begin > last_end:
                                inside_markers = True

                        if not inside_markers:
                            # Extract context around the match
                            start = max(0, match.start() - 20)
                            end = min(len(content), match.end() + 20)
                            context = content[start:end].replace("\n", " ")

                            violations.append(
                                {
                                    "file": filename,
                                    "pattern": pattern,
                                    "context": f"...{context}...",
                                }
                            )

        if violations:
            msg = "DICE-ktu: Found tool_requests dice instructions NOT wrapped in markers:\n"
            for v in violations[:5]:  # Limit to first 5
                msg += f"\n  - {v['file']}: {v['context']}"
            msg += "\n\nFix: Wrap these sections with:"
            msg += "\n  <!-- BEGIN_TOOL_REQUESTS_DICE -->"
            msg += "\n  ... dice tool_requests content ..."
            msg += "\n  <!-- END_TOOL_REQUESTS_DICE -->"
            self.fail(msg)

    def test_strip_function_removes_marked_content(self):
        """Verify strip_tool_requests_dice_instructions removes marked content."""
        test_content = """
Some intro text.

<!-- BEGIN_TOOL_REQUESTS_DICE -->
You MUST use tool_requests for roll_attack and roll_damage.
All dice rolls require: "tool_requests": [{"tool": "roll_attack", ...}]
<!-- END_TOOL_REQUESTS_DICE -->

Some other content that should remain.
"""

        result = strip_tool_requests_dice_instructions(test_content)

        # Verify marked content is removed
        assert "roll_attack" not in result
        assert "tool_requests" not in result
        assert "BEGIN_TOOL_REQUESTS_DICE" not in result
        assert "END_TOOL_REQUESTS_DICE" not in result

        # Verify other content remains
        assert "Some intro text." in result
        assert "Some other content that should remain." in result


class TestDeferredRewardsPrompts(unittest.TestCase):
    def setUp(self):
        _loaded_instructions_cache.clear()

    def test_should_include_deferred_rewards_interval(self):
        """Deferred rewards only triggers on configured interval and positive turns."""

        builder = agent_prompts.PromptBuilder(None)

        self.assertFalse(builder.should_include_deferred_rewards(0))
        self.assertFalse(builder.should_include_deferred_rewards(1))
        self.assertTrue(
            builder.should_include_deferred_rewards(
                constants.DEFERRED_REWARDS_SCENE_INTERVAL
            )
        )

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_build_deferred_rewards_instruction_includes_context(self, mock_load):
        """Build instruction returns contextual header and base prompt content."""

        mock_load.return_value = "BASE"
        builder = agent_prompts.PromptBuilder(None)
        turn_number = constants.DEFERRED_REWARDS_SCENE_INTERVAL

        instruction = builder.build_deferred_rewards_instruction(turn_number)

        self.assertIn("DEFERRED REWARDS CHECK", instruction)
        self.assertIn(str(constants.DEFERRED_REWARDS_SCENE_INTERVAL), instruction)
        self.assertIn("BASE", instruction)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_build_deferred_rewards_instruction_force_include(self, mock_load):
        """Force include bypasses interval gating and uses provided reason."""

        mock_load.return_value = "FORCE_BASE"
        builder = agent_prompts.PromptBuilder(None)

        instruction = builder.build_deferred_rewards_instruction(
            turn_number=1, force_include=True, force_reason="Manual audit"
        )

        self.assertIn("Manual audit", instruction)
        self.assertIn("FORCE_BASE", instruction)

class TestPromptBuilderLivingWorldIntegration(unittest.TestCase):
    """Test PromptBuilder integration with GameState living world triggers."""

    def test_build_living_world_instruction_is_turn_driven(self):
        """Living world instruction is emitted for positive turns without trigger delegation."""
        gs = GameState()
        with patch.object(
            gs, "check_living_world_trigger", return_value=(True, "test reason", None)
        ) as mock_check:
            builder = PromptBuilder(game_state=gs)

            with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
                instruction = builder.build_living_world_instruction(3)
                self.assertIn("LIVING WORLD", instruction)
                self.assertIn("LIVING WORLD ADVANCEMENT", instruction)
                mock_check.assert_not_called()

    def test_does_not_update_tracking_on_build(self):
        """Should not update tracking fields during prompt construction."""
        current_time = {"year": 1000, "month": 1, "day": 1}
        gs = GameState()
        # Mock the trigger check to return True and a time
        with patch.object(
            gs, "check_living_world_trigger", return_value=(True, "reason", current_time)
        ) as mock_check:
            builder = PromptBuilder(game_state=gs)
            # Mock loading instruction
            with patch("mvp_site.agent_prompts._load_instruction_file", return_value="INSTRUCTION"):
                builder.build_living_world_instruction(10)
            # Verify state NOT updated
            assert gs.last_living_world_turn == 0
            assert gs.last_living_world_time is None

    def test_does_not_reset_tracking_on_build_without_time(self):
        """Should not reset tracking when prompt builds without current_time."""
        gs = GameState()
        gs.last_living_world_time = {"old": "time"}
        # Mock the trigger check to return True but NO time (e.g. turn-only trigger)
        with patch.object(
            gs, "check_living_world_trigger", return_value=(True, "reason", None)
        ):
            builder = PromptBuilder(game_state=gs)
            # Mock loading instruction
            with patch("mvp_site.agent_prompts._load_instruction_file", return_value="INSTRUCTION"):
                builder.build_living_world_instruction(30)
            # Verify state NOT updated
            assert gs.last_living_world_turn == 0
            assert gs.last_living_world_time == {"old": "time"}


class TestPromptBuilderCoverage(unittest.TestCase):
    def test_social_hp_early_reminder_prepended_for_high_tier_npc(self):
        """Ensure Social HP reminder is prepended when high-tier NPCs exist."""
        gs = GameState()
        gs.npc_data = {"npc_1": {"tier": "god_primordial", "level": 20}}
        builder = PromptBuilder(game_state=gs)

        with patch(
            "mvp_site.agent_prompts._load_instruction_file", return_value="PROMPT"
        ):
            parts = builder.build_from_order(
                (constants.PROMPT_TYPE_MASTER_DIRECTIVE,),
                include_debug=False,
            )

        self.assertEqual(parts[0], agent_prompts.SOCIAL_HP_EARLY_REMINDER)

    def test_social_hp_early_reminder_in_core_instructions(self):
        """Ensure core instruction builder prepends Social HP reminder."""
        gs = GameState()
        gs.npc_data = {"npc_1": {"tier": "king_ancient", "level": 1}}
        builder = PromptBuilder(game_state=gs)

        with patch(
            "mvp_site.agent_prompts._load_instruction_file", return_value="PROMPT"
        ), patch(
            "mvp_site.agent_prompts._build_debug_instructions", return_value="DEBUG"
        ):
            parts = builder.build_core_system_instructions()

        self.assertEqual(parts[0], agent_prompts.SOCIAL_HP_EARLY_REMINDER)

    def test_build_for_agent_missing_methods_raises(self):
        """Non-AgentProtocol without required methods should raise TypeError."""
        builder = PromptBuilder(None)

        class BadAgent:
            pass

        with self.assertRaises(TypeError):
            builder.build_for_agent(BadAgent())

    @patch("mvp_site.agent_prompts.load_dice_instructions")
    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_add_selected_prompts_forces_narrative_when_non_empty(
        self, mock_load_file, mock_load_dice
    ):
        """Narrative is injected when selected prompts are non-empty."""
        mock_load_file.side_effect = lambda pt: f"PROMPT:{pt}"
        mock_load_dice.return_value = "DICE"
        builder = PromptBuilder(None)

        parts: list[str] = []
        builder.add_selected_prompt_instructions(
            parts,
            [constants.PROMPT_TYPE_MECHANICS],
            essentials_only=False,
        )

        self.assertIn(f"PROMPT:{constants.PROMPT_TYPE_NARRATIVE}", parts)
        self.assertIn(f"PROMPT:{constants.PROMPT_TYPE_MECHANICS}", parts)
        self.assertIn("DICE", parts)

    @patch("mvp_site.agent_prompts.load_detailed_sections")
    @patch("mvp_site.agent_prompts.load_dice_instructions")
    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_add_selected_prompts_essentials_loads_requested_sections(
        self, mock_load_file, mock_load_dice, mock_load_sections
    ):
        """Essentials mode loads detailed sections when requested."""
        section_name = next(iter(agent_prompts.SECTION_TO_PROMPT_TYPE.keys()))
        mock_load_file.side_effect = lambda pt: f"PROMPT:{pt}"
        mock_load_dice.return_value = "DICE"
        mock_load_sections.return_value = "DETAILS"
        builder = PromptBuilder(None)

        parts: list[str] = []
        builder.add_selected_prompt_instructions(
            parts,
            [section_name],
            essentials_only=True,
        )

        self.assertIn("DETAILS", parts)
        mock_load_sections.assert_called_once_with([section_name])

    @patch("mvp_site.agent_prompts.load_detailed_sections")
    @patch("mvp_site.agent_prompts.load_dice_instructions")
    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_add_selected_prompts_non_essentials_loads_llm_sections(
        self, mock_load_file, mock_load_dice, mock_load_sections
    ):
        """Non-essentials mode loads only LLM-requested detailed sections."""
        section_name = next(iter(agent_prompts.SECTION_TO_PROMPT_TYPE.keys()))
        mock_load_file.side_effect = lambda pt: f"PROMPT:{pt}"
        mock_load_dice.return_value = "DICE"
        mock_load_sections.return_value = "DETAILS"
        builder = PromptBuilder(None)

        parts: list[str] = []
        builder.add_selected_prompt_instructions(
            parts,
            [constants.PROMPT_TYPE_NARRATIVE],
            llm_requested_sections=[section_name],
            essentials_only=False,
        )

        self.assertIn("DETAILS", parts)
        mock_load_sections.assert_called_once_with([section_name])

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_build_living_world_instruction_stateless_interval(
        self, mock_load_file
    ):
        """Stateless builder includes living-world header and base instructions."""
        mock_load_file.return_value = "LIVING_WORLD"
        builder = PromptBuilder(game_state=None)

        instruction = builder.build_living_world_instruction(
            constants.LIVING_WORLD_TURN_INTERVAL
        )

        self.assertIn("LIVING_WORLD", instruction)
        self.assertIn("LIVING WORLD ADVANCEMENT", instruction)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_build_living_world_instruction_stateless_turn_zero(self, mock_load_file):
        """Stateless builder should not trigger living world on turn 0."""
        mock_load_file.return_value = "LIVING_WORLD"
        builder = PromptBuilder(game_state=None)

        instruction = builder.build_living_world_instruction(0)

        self.assertEqual(instruction, "")

class TestDetailedPromptLoading(unittest.TestCase):
    """Verify relationship and reputation files exist and load correctly."""

    def test_relationship_file_exists_and_loads(self):
        """Verify relationship_instruction.md exists and loads without error."""
        content = agent_prompts._load_instruction_file(
            constants.PROMPT_TYPE_RELATIONSHIP
        )

        self.assertIsInstance(content, str)
        self.assertGreater(
            len(content), 100, "Relationship file should have substantial content"
        )
        self.assertIn("Relationship", content)
        self.assertIn("trust_level", content)
        self.assertIn("npc_data", content)

    def test_reputation_file_exists_and_loads(self):
        """Verify reputation_instruction.md exists and loads without error."""
        content = agent_prompts._load_instruction_file(constants.PROMPT_TYPE_REPUTATION)

        self.assertIsInstance(content, str)
        self.assertGreater(
            len(content), 100, "Reputation file should have substantial content"
        )
        self.assertIn("Reputation", content)
        self.assertIn("public", content)
        self.assertIn("private", content)

    def test_load_detailed_sections_relationships(self):
        """Test load_detailed_sections with relationships section."""
        result = agent_prompts.load_detailed_sections(["relationships"])

        self.assertIn("--- RELATIONSHIPS MECHANICS ---", result)
        self.assertIn("trust_level", result)

    def test_load_detailed_sections_reputation(self):
        """Test load_detailed_sections with reputation section."""
        result = agent_prompts.load_detailed_sections(["reputation"])

        self.assertIn("--- REPUTATION MECHANICS ---", result)
        self.assertIn("notoriety_level", result)

    def test_load_detailed_sections_both(self):
        """Test load_detailed_sections with both sections."""
        result = agent_prompts.load_detailed_sections(["relationships", "reputation"])

        self.assertIn("--- RELATIONSHIPS MECHANICS ---", result)
        self.assertIn("--- REPUTATION MECHANICS ---", result)
        self.assertIn("trust_level", result)
        self.assertIn("notoriety_level", result)

    def test_load_detailed_sections_empty_list(self):
        """Test load_detailed_sections with empty list returns empty string."""
        result = agent_prompts.load_detailed_sections([])
        self.assertEqual(result, "")

    def test_load_detailed_sections_unknown_section(self):
        """Test load_detailed_sections gracefully ignores unknown sections."""
        result = agent_prompts.load_detailed_sections(["unknown_section"])
        self.assertEqual(result, "")

    def test_load_detailed_sections_mixed_valid_invalid(self):
        """Test load_detailed_sections with mix of valid and invalid sections."""
        result = agent_prompts.load_detailed_sections(
            ["relationships", "invalid", "reputation"]
        )

        self.assertIn("--- RELATIONSHIPS MECHANICS ---", result)
        self.assertIn("--- REPUTATION MECHANICS ---", result)
        self.assertNotIn("invalid", result.lower().split("---")[0])


class TestExtractLLMInstructionHints(unittest.TestCase):
    """Test extraction of instruction hints from LLM responses."""

    def test_extract_hints_valid_response(self):
        llm_response = {
            "narrative": "The story continues...",
            "debug_info": {"meta": {"needs_detailed_instructions": ["relationships"]}},
        }

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, ["relationships"])

    def test_extract_hints_multiple_sections(self):
        llm_response = {
            "narrative": "The story continues...",
            "debug_info": {
                "meta": {"needs_detailed_instructions": ["relationships", "reputation"]}
            },
        }

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(set(hints), {"relationships", "reputation"})

    def test_extract_hints_no_debug_info(self):
        llm_response = {"narrative": "The story continues..."}

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, [])

    def test_extract_hints_no_meta(self):
        llm_response = {"narrative": "The story continues...", "debug_info": {}}

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, [])

    def test_extract_hints_no_needs_detailed(self):
        llm_response = {
            "narrative": "The story continues...",
            "debug_info": {"meta": {}},
        }

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, [])

    def test_extract_hints_invalid_hint_type(self):
        llm_response = {
            "narrative": "The story continues...",
            "debug_info": {
                "meta": {"needs_detailed_instructions": ["relationships", 123, None]}
            },
        }

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, ["relationships"])

    def test_extract_hints_invalid_section_name(self):
        llm_response = {
            "narrative": "The story continues...",
            "debug_info": {
                "meta": {
                    "needs_detailed_instructions": ["relationships", "invalid_section"]
                }
            },
        }

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, ["relationships"])

    def test_extract_hints_not_a_dict(self):
        hints = agent_prompts.extract_llm_instruction_hints("not a dict")
        self.assertEqual(hints, [])

        hints = agent_prompts.extract_llm_instruction_hints(None)
        self.assertEqual(hints, [])

    def test_extract_hints_debug_info_not_dict(self):
        llm_response = {
            "narrative": "The story continues...",
            "debug_info": "not a dict",
        }

        hints = agent_prompts.extract_llm_instruction_hints(llm_response)
        self.assertEqual(hints, [])


class TestPromptBuilderIntegration(unittest.TestCase):
    """Integration tests for PromptBuilder with detailed sections loading."""

    def setUp(self):
        self.game_state = GameState(
            player_character_data={"name": "TestHero"},
        )

    def test_add_selected_prompt_instructions_loads_relationships(self):
        """Test that llm_requested_sections loads relationship mechanics."""
        builder = PromptBuilder(self.game_state)

        prompt_parts = ["Base prompt"]
        # Section names go in llm_requested_sections, not selected_prompts
        builder.add_selected_prompt_instructions(
            prompt_parts, [], llm_requested_sections=["relationships"]
        )

        combined = "\n".join(prompt_parts)
        self.assertIn("--- RELATIONSHIPS MECHANICS ---", combined)
        self.assertIn("trust_level", combined)

    def test_add_selected_prompt_instructions_loads_multiple_sections(self):
        """Test that multiple sections can be loaded via llm_requested_sections."""
        builder = PromptBuilder(self.game_state)

        prompt_parts = ["Base prompt"]
        # Section names go in llm_requested_sections, not selected_prompts
        builder.add_selected_prompt_instructions(
            prompt_parts, [], llm_requested_sections=["relationships", "reputation"]
        )

        combined = "\n".join(prompt_parts)
        self.assertIn("--- RELATIONSHIPS MECHANICS ---", combined)
        self.assertIn("--- REPUTATION MECHANICS ---", combined)
        self.assertIn("trust_level", combined)
        self.assertIn("notoriety_level", combined)

    def test_add_selected_prompt_instructions_handles_empty(self):
        """Test that empty llm_requested_sections doesn't add detailed sections."""
        builder = PromptBuilder(self.game_state)

        prompt_parts = ["Base prompt"]
        # With empty selected_prompts and no llm_requested_sections,
        # the method still adds narrative and dice instructions (always required)
        builder.add_selected_prompt_instructions(
            prompt_parts, [], llm_requested_sections=[]
        )

        combined = "\n".join(prompt_parts)
        # Should have narrative + dice, but NOT detailed sections
        self.assertIn("Base prompt", combined)
        self.assertNotIn("--- RELATIONSHIPS MECHANICS ---", combined)
        self.assertNotIn("--- REPUTATION MECHANICS ---", combined)


class TestSectionToPromptTypeMapping(unittest.TestCase):
    """Test mapping from detailed section names to prompt types."""

    def test_section_to_prompt_type_mapping(self):
        mapping = agent_prompts.SECTION_TO_PROMPT_TYPE

        self.assertEqual(
            mapping["relationships"],
            constants.PROMPT_TYPE_RELATIONSHIP,
        )
        self.assertEqual(
            mapping["reputation"],
            constants.PROMPT_TYPE_REPUTATION,
        )

    def test_mapping_only_contains_valid_sections(self):
        for section in agent_prompts.SECTION_TO_PROMPT_TYPE:
            self.assertIn(section, agent_prompts.DETAILED_INSTRUCTION_SECTIONS)


class TestTokenSavings(unittest.TestCase):
    """Test that token savings are achieved when sections not loaded."""

    def test_no_sections_vs_all_sections_size_difference(self):
        no_sections = agent_prompts.load_detailed_sections([])
        all_sections = agent_prompts.load_detailed_sections(
            ["relationships", "reputation"]
        )

        self.assertEqual(len(no_sections), 0)
        self.assertGreater(
            len(all_sections),
            10000,
            "Combined sections should be >10KB (saves ~3400 tokens when not loaded)",
        )


class TestPendingInstructionHintsWiring(unittest.TestCase):
    """Test the full wiring: GameState.pending_instruction_hints → Agent → PromptBuilder."""

    def test_needs_relationship_hint_loads_relationship_instructions(self):
        game_state = GameState(
            player_character_data={"name": "TestHero"},
            pending_instruction_hints=["relationships"],
        )

        agent = StoryModeAgent(game_state)

        system_instructions = agent.build_system_instructions(
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE],
            llm_requested_sections=game_state.pending_instruction_hints,
        )

        self.assertIn(
            "--- RELATIONSHIPS MECHANICS ---",
            system_instructions,
            "relationship_instruction.md content should be loaded",
        )


class TestLivingWorldTurnTriggers(unittest.TestCase):
    """Test living-world instruction inclusion behavior by turn."""

    def test_turn_based_trigger_at_turn_3(self):
        """Living world event should trigger at turn 3 when last event was turn 0."""
        game_state = GameState(
            last_living_world_turn=0,
            last_living_world_time=None,
            player_turn=3,
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Turn 3 should trigger (3 - 0 = 3 turns elapsed)
        # We check build_living_world_instruction instead of should_include_living_world
        # because should_include_living_world is now always True for cache consistency.
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(3) != ""

    def test_turn_based_trigger_at_turn_20(self):
        """Living world event should trigger at turn 6 when last event was turn 3."""
        game_state = GameState(
            last_living_world_turn=3,
            last_living_world_time=None,
            player_turn=6,
        )
        prompt_builder = PromptBuilder(game_state=game_state)
        # Turn 6 should trigger (6 - 3 = 3 turns elapsed)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(6) != ""

    def test_fallback_when_game_state_none(self):
        """Instruction should be included for positive turns even without GameState."""
        builder = PromptBuilder(game_state=None)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="INSTRUCTION"):
            assert "INSTRUCTION" in builder.build_living_world_instruction(9)
            assert builder.build_living_world_instruction(9) != ""

        game_state = GameState(
            last_living_world_turn=10,
            last_living_world_time=None,
            player_turn=11,
        )
        prompt_builder = PromptBuilder(game_state=game_state)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="INSTRUCTION"):
            assert "INSTRUCTION" in prompt_builder.build_living_world_instruction(11)

    def test_trigger_exactly_at_interval(self):
        """Living world event should trigger exactly when interval is reached."""
        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=None,
            player_turn=9,
        )
        prompt_builder = PromptBuilder(game_state=game_state)
        # Turn 9 should trigger (9 % 3 == 0 and 9 > 5)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(9) != ""

    def test_no_trigger_at_turn_0(self):
        """Living world event should not trigger at turn 0."""
        game_state = GameState(
            last_living_world_turn=0,
            last_living_world_time=None,
            player_turn=0,
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should be empty for turn 0
        assert prompt_builder.build_living_world_instruction(0) == ""


class TestLivingWorldTimeTriggers(unittest.TestCase):
    """Test time-state compatibility while instruction inclusion remains turn-driven."""

    def test_time_based_trigger_after_24_hours(self):
        """Living world event should trigger after 24 hours of game time."""
        last_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        current_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=6,  # Only 1 turn elapsed (not enough for turn trigger)
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should trigger due to time (24 hours elapsed)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(6) != ""

    def test_no_trigger_before_24_hours(self):
        """Instruction remains included before 24 hours for schema consistency."""
        last_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        current_time = {"year": 1492, "month": 6, "day": 16, "hour": 9, "minute": 59}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=7,  # 7 % 3 != 0, so no turn trigger
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(7) != ""

    def test_time_trigger_after_48_hours(self):
        """Living world event should trigger after 48+ hours (multiple intervals)."""
        last_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        current_time = {"year": 1492, "month": 6, "day": 17, "hour": 11, "minute": 0}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=6,
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should trigger (49 hours elapsed, well over 24h threshold)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(6) != ""

    def test_time_trigger_with_month_boundary(self):
        """Living world event should trigger across month boundaries."""
        last_time = {"year": 1492, "month": 6, "day": 30, "hour": 23, "minute": 0}
        current_time = {"year": 1492, "month": 7, "day": 1, "hour": 23, "minute": 0}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=6,
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should trigger (24 hours elapsed across month boundary)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(6) != ""

    def test_no_trigger_without_world_time(self):
        """Instruction remains included even when world_time is unavailable."""
        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=None,
            world_data={},  # No world_time
            player_turn=7,  # 2 turns elapsed (not enough for turn trigger)
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(7) != ""


class TestLivingWorldDualTriggers(unittest.TestCase):
    """Test that either trigger (turn OR time) will fire the event."""

    def test_turn_trigger_overrides_insufficient_time(self):
        """Turn trigger should fire even if time hasn't reached threshold."""
        last_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        current_time = {"year": 1492, "month": 6, "day": 15, "hour": 15, "minute": 0}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=15,  # 10 turns elapsed (enough for turn trigger)
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should trigger due to turns (only 5 hours elapsed, but 10 turns elapsed)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(15) != ""

    def test_time_trigger_overrides_insufficient_turns(self):
        """Time trigger should fire even if turns haven't reached threshold."""
        last_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        current_time = {"year": 1492, "month": 6, "day": 16, "hour": 11, "minute": 0}

        game_state = GameState(
            last_living_world_turn=10,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=11,  # 11 % 3 != 0, so no turn trigger
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should trigger due to time (25 hours elapsed; 11 % 3 != 0 so no turn trigger)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(11) != ""

    def test_both_triggers_fire_together(self):
        """Event should fire when both turn AND time thresholds are met."""
        last_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        current_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time=last_time,
            world_data={"world_time": current_time},
            player_turn=15,  # 10 turns AND 24 hours elapsed
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Should trigger (both conditions met)
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            assert prompt_builder.build_living_world_instruction(15) != ""


class TestLivingWorldTrackingUpdate(unittest.TestCase):
    """Test that tracking fields are updated when events fire."""

    def test_tracking_fields_updated_on_trigger(self):
        """Tracking fields should not update during prompt construction."""
        current_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        game_state = GameState(
            last_living_world_turn=0,
            last_living_world_time=None,
            world_data={"world_time": current_time},
            player_turn=9,  # 9 % 3 == 0, triggers
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        # Build instruction (should trigger, but not update tracking during prompt build)
        # We need to mock _load_instruction_file since it reads from disk
        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            instruction = prompt_builder.build_living_world_instruction(9)

        # Verify instruction was generated
        assert instruction != ""
        assert "LIVING WORLD" in instruction

        # Verify tracking fields were NOT updated during prompt build
        assert game_state.last_living_world_turn == 0
        # last_living_world_time is seeded from world_data in GameState.__init__
        for key in ("year", "month", "day", "hour", "minute"):
            assert game_state.last_living_world_time.get(key) == current_time[key]

    def test_tracking_not_updated_when_no_trigger(self):
        """Tracking fields should not update during prompt construction."""
        current_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        game_state = GameState(
            last_living_world_turn=5,
            last_living_world_time={"year": 1492, "month": 6, "day": 16, "hour": 9, "minute": 0},
            world_data={"world_time": current_time},
            player_turn=7,  # 7 % 3 != 0, and only 1 hour elapsed
        )
        prompt_builder = PromptBuilder(game_state=game_state)

        with patch("mvp_site.agent_prompts._load_instruction_file", return_value="LIVING WORLD"):
            instruction = prompt_builder.build_living_world_instruction(7)
        assert instruction != ""

        # Verify tracking fields were NOT changed
        assert game_state.last_living_world_turn == 5
        assert game_state.last_living_world_time == {"year": 1492, "month": 6, "day": 16, "hour": 9, "minute": 0}


class TestWorldTimeCalculations(unittest.TestCase):
    """Test the calculate_hours_elapsed helper function."""

    def test_calculate_hours_elapsed_24_hours(self):
        """Should correctly calculate 24 hours elapsed."""
        old_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours == 24.0

    def test_calculate_hours_elapsed_with_minutes(self):
        """Should correctly calculate hours with fractional minutes."""
        old_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 30}
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 11, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours == 24.5

    def test_calculate_hours_elapsed_returns_none_for_incomplete_time(self):
        """Should return None when time data is incomplete."""
        old_time = {"hour": 10, "minute": 0}  # Missing year, month, day
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours is None

    def test_calculate_hours_elapsed_returns_none_for_none_input(self):
        """Should return None when input is None."""
        old_time = None
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours is None


class TestStripPromptComments(unittest.TestCase):
    """Test the _strip_prompt_comments function."""

    def test_strip_empty_comment(self):
        """Should strip comments that contain only whitespace."""
        content = "Some content<!--   -->more content"
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!--   -->" not in result
        assert "Some contentmore content" in result

    def test_strip_whitespace_only_comment(self):
        """Should strip comments with only whitespace characters."""
        content = "Before<!-- \t\n\r -->After"
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!--" not in result
        assert "BeforeAfter" in result

    def test_preserve_comment_with_content(self):
        """Should preserve comments that have actual content."""
        content = "Before<!-- This is a comment -->After"
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!-- This is a comment -->" in result
        assert "Before" in result
        assert "After" in result

    def test_strip_essentials_block(self):
        """Should strip ESSENTIALS comment blocks — they are dev docs, not LLM instructions."""
        content = """Some content
<!-- ESSENTIALS (token-constrained mode)
- Important content here
/ESSENTIALS -->
More content"""
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!-- ESSENTIALS" not in result
        assert "/ESSENTIALS -->" not in result
        assert "Some content" in result
        assert "More content" in result

    def test_strip_multiple_empty_comments(self):
        """Should strip multiple empty comments."""
        content = "A<!-- -->B<!--   -->C"
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!--" not in result
        assert "ABC" in result

    def test_strip_nested_essentials_block(self):
        """Should strip ESSENTIALS block even when it contains inner comments."""
        content = """<!-- ESSENTIALS
- Outer block
<!-- inner comment -->
/ESSENTIALS -->"""
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!-- ESSENTIALS" not in result
        assert "/ESSENTIALS -->" not in result

    def test_strip_auto_generated_markers(self):
        """Should strip AUTO-GENERATED comment markers."""
        content = "Before\n<!-- AUTO-GENERATED from schema -->\nContent\n<!-- /AUTO-GENERATED -->\nAfter"
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!-- AUTO-GENERATED" not in result
        assert "<!-- /AUTO-GENERATED -->" not in result
        assert "Content" in result
        assert "Before" in result
        assert "After" in result

    def test_no_comments_unchanged(self):
        """Should return content unchanged if no comments present."""
        content = "No comments here, just content"
        result = agent_prompts._strip_prompt_comments(content)
        assert result == content

    def test_malformed_comment_preserved(self):
        """Should preserve malformed/unclosed comments as-is."""
        content = "Before<!-- unclosed comment After"
        result = agent_prompts._strip_prompt_comments(content)
        assert "<!-- unclosed comment" in result

    def test_clean_up_double_newlines(self):
        """Should clean up resulting double newlines from removed comments."""
        content = "Line 1\n\n<!--   -->\n\nLine 2"
        result = agent_prompts._strip_prompt_comments(content)
        # Should not have triple+ newlines
        assert "\n\n\n" not in result


class TestCommentStrippingFeatureFlag(unittest.TestCase):
    """Test the feature flag for comment stripping."""

    def test_default_enabled(self):
        """Should be enabled by default."""
        # Reset the cached value
        agent_prompts._ENABLE_PROMPT_COMMENT_STRIPPING = None
        result = agent_prompts._is_comment_stripping_enabled()
        assert result is True

    def test_can_be_disabled(self):
        """Should respect ENABLE_PROMPT_COMMENT_STRIPPING=false."""
        with patch.dict(os.environ, {"ENABLE_PROMPT_COMMENT_STRIPPING": "false"}):
            # Reset the cached value
            agent_prompts._ENABLE_PROMPT_COMMENT_STRIPPING = None
            result = agent_prompts._is_comment_stripping_enabled()
            assert result is False

    def test_explicit_true_enabled(self):
        """Should be enabled when explicitly set to true."""
        with patch.dict(os.environ, {"ENABLE_PROMPT_COMMENT_STRIPPING": "true"}):
            # Reset the cached value
            agent_prompts._ENABLE_PROMPT_COMMENT_STRIPPING = None
            result = agent_prompts._is_comment_stripping_enabled()
            assert result is True


if __name__ == '__main__':
    unittest.main()
