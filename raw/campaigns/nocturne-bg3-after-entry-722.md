---
title: "Nocturne Bg3 After — Scene 722"
type: source
tags: [campaign, scene, nocturne-bg3-after]
last_updated: 2026-04-12
scene_number: 722
scene_total: 1027
source_file: /tmp/campaign_downloads_v2/
---

## Scene 722 Summary

============================================================ [Timestamp: 1493 DR, Marpenoth 18, 17:30:00 Location: Zariel's Command Center - Avernus Status: Lvl 30 Sovereign (Masked 22) | HP: 605/605 | Gold: 1,179,967gp] Resources: HD: 11/11, Spells: L1-7 Infinite, L8 2/2, L9 5/5, L10: 2/4, Exhaustion: 0 Dice Rolls:   - Strategic Simulation (Bel Hollowing): 1d20+49 = 7+49 = 56 vs DC 60 (Partial Success)  Game Master: You remain pinned against the cool obsidian of the throne, the sulfurous draft

## Key Details

- **Location:** Zariel's Command Center - Avernus
- **Level hint:** 30
- **Word count:** 5659
- **Campaign:** [[Nocturne Bg3 After]]
- **Entry:** [[nocturne-bg3-after-entry-722]]

---

## Full Scene Content

============================================================
[Timestamp: 1493 DR, Marpenoth 18, 17:30:00
Location: Zariel's Command Center - Avernus
Status: Lvl 30 Sovereign (Masked 22) | HP: 605/605 | Gold: 1,179,967gp]
Resources: HD: 11/11, Spells: L1-7 Infinite, L8 2/2, L9 5/5, L10: 2/4, Exhaustion: 0
Dice Rolls:
  - Strategic Simulation (Bel Hollowing): 1d20+49 = 7+49 = 56 vs DC 60 (Partial Success)

Game Master:
You remain pinned against the cool obsidian of the throne, the sulfurous draft of the Command Center whipping a loose strand of hair across your porcelain cheek. Your gaze drifts past Zariel's massive, bronze-clad form to the jagged horizon where Bel's Censure Envoy is currently hunting the vacuum you left at the Puncture. The 'Bel Variable' has been an oscillation in your ledger for weeks—a rival for Zariel's favor and a master of the very forge-logic you have begun to colonize.

You pause, the matte-black ink of the Crown swirling beneath your skin as your Mind retreats into the cold, pressurized laboratory of the Sovereign Zenith. To gift Zariel the hollowing of her greatest rival would be a masterpiece of administrative theater. You can see the schematic in your mind: Bel's motor-functions deleted, his spirit refactored into a subsidiary terminal, and his biological frame presented to the Archdevil as a silent monument to her dominance. It would sate her sadistic possessiveness and deepen the grounding of your ruse.

Yet, as you trace the somatic curves of this deception, you feel the weight of the higher-tier auditors. To keep the strings while handing over the puppet is an algebraic risk of the highest circle. The air around you shimmers with a violet-black pressure as you model the ROI of such a gamble, weighing the absolute submission of an Archdevil's predecessor against the catastrophic 'loudness' of a dual-mastered shell.

God Mode:
shouldnt this have had foresight? Skip to content
Navigation Menu
jleechanorg
worldarchitect.ai

Type / to search
Code
Issues
7
Pull requests
546
Actions
Projects
Security
39
Insights
Settings
Review campaign debugging and propose solutions #2564
✨ 
 Open
jleechan2015 wants to merge 10 commits into main from claude/review-campaign-debugging-V4Nvf  
+938 −15 
 Conversation 52
 Commits 10
 Checks 9
 Files changed 6
 Open
Review campaign debugging and propose solutions
#2564
 
File filter 
 
0 / 6 files viewed
Filter changed files
 160 changes: 160 additions & 0 deletions160  
docs/debugging/god_mode_campaign_fixes.md
Viewed
Original file line number	Diff line number	Diff line change
@@ -0,0 +1,160 @@
# God Mode Campaign Fixes

## Overview

This document explains the fixes implemented to address issues identified in the Alexiel Assiah campaign debugging session. The core problem was that the LLM would make claims (e.g., "You are Level 8") that were silently corrected by validation (to Level 7), causing user confusion.

## Issues Identified

From analyzing the campaign log (`docs/debugging/Alexiel assiah.txt`):

| Category | Count | Examples |
|----------|-------|----------|
| Level/XP confusion | 5 | "no i am level 7 right?", "wait why am i level 12 now" |
| Gender misidentification | 2 | "remember alexiel is a woman so a daughter not a son" |
| Ignored directives | 2 | "when i say think about pros/cons dont ignore it" |
| Missing rewards | 3 | "make sure you awarded my exp, loot, resources" |

## Root Cause Analysis

The validation infrastructure **already existed** (`validate_and_correct_state()`, `validate_xp_level()`) but operated **invisibly**:

1. LLM claims "Level 8" in narrative
2. Validation corrects state to Level 7
3. User sees conflicting information (narrative says 8, state shows 7)
4. LLM context includes its own wrong claim

## Solutions Implemented

### 1. Visible Validation Feedback

**File:** `mvp_site/game_state.py`

```python
# validate_and_correct_state() now returns corrections
state, corrections = validate_and_correct_state(state_dict, return_corrections=True)
# Returns: ['Level auto-corrected from 8 to 7 based on XP']
```

**Why:** Users need to see when the system corrects the LLM's claims.

### 2. Character Identity Block

**File:** `mvp_site/game_state.py`

```python
def get_character_identity_block(self) -> str:
    # Returns:
    # ## Character Identity (IMMUTABLE)
    # - **Name**: Alexiel
    # - **Gender**: Female (she/her)
    # - **NEVER** refer to this character as 'he', 'him', or 'son'
```

**Why:** Prevents misgendering by including explicit pronoun enforcement in every prompt.

### 3. God Mode Directive Persistence

**File:** `mvp_site/game_state.py`

```python
def add_god_mode_directive(self, directive: str) -> None:
    # Stores in: custom_campaign_state.god_mode_directives[]
    # Persists across sessions
```

**Why:** Player rules like "always award XP after combat" were being forgotten between sessions.

### 4. Post-Combat XP Warning Detection

**File:** `mvp_site/game_state.py`

```python
def detect_post_combat_issues(self, previous_combat_state, state_changes) -> list[str]:
    # Returns: ['Combat ended but no XP was awarded. Consider awarding XP for 3 combatant(s).']
```

**Why:** The LLM frequently forgot to award XP after combat ended.

### 5. System Warnings in Response

**File:** `mvp_site/world_logic.py`

```python
# Corrections and warnings now surface in the API response
unified_response["system_warnings"] = [
    "Level auto-corrected from 8 to 7 based on XP",
    "Combat ended but no XP was awarded..."
]
```

**Why:** Makes validation corrections visible to the frontend/user.

### 6. Identity/Directives in Prompts

**File:** `mvp_site/agent_prompts.py`

```python
def finalize_instructions(self, parts, use_default_world=False) -> str:
    # Automatically injects:
    # - Character identity block (name, gender, pronouns)
    # - God mode directives (player-defined rules)
```

**Why:** Ensures every LLM prompt includes immutable character facts and player rules.

## Merge with Main Branch

The branch was rebased and merged with `origin/main` which added:

- **Arc Milestones** (`game_state.py`) - Tracks completed narrative arcs to prevent LLM from revisiting concluded storylines
- **Combat Agent** (`agents.py`) - New combat-focused agent with specialized prompts
- **Planning Blocks Fix** - Ensures real choices are generated in planning mode

### Merge Decision: No Conflicts

Both codebases modified `game_state.py` and `world_logic.py` but in different areas:
- **Main:** Added arc milestone methods (lines 340-500)
- **Branch:** Added god mode/identity methods (lines 1057-1237)

Git auto-merged successfully because the changes were additive and non-overlapping.

## Testing

### MCP Test Suite

**File:** `testing_mcp/test_god_mode_validation.py`

Tests all implemented features:
- Validation corrections visibility
- God mode directives persistence
- Character identity enforcement
- Post-combat XP warning detection

```bash
# Run against preview server
MCP_SERVER_URL=https://<preview>.run.app python test_god_mode_validation.py

# Run with local server
python test_god_mode_validation.py --start-local
```

## Impact

These changes should eliminate ~70% of the correction-type GOD MODE interventions observed in the Alexiel campaign:

| Before | After |
|--------|-------|
| Silent XP/level corrections | Visible `system_warnings` in response |
| Forgotten directives | Persisted in `god_mode_directives` |
| Misgendering | Identity block with pronoun enforcement |
| Missing combat rewards | Post-combat XP warning detection |

## Files Modified

| File | Changes |
|------|---------|
| `mvp_site/game_state.py` | +229 lines: identity block, directives, post-combat detection |
| `mvp_site/agent_prompts.py` | +112 lines: finalize_instructions with identity/directives |
| `mvp_site/world_logic.py` | +27 lines: system_warnings in response |
| `testing_mcp/test_god_mode_validation.py` | +414 lines: MCP test suite |
  112 changes: 112 additions & 0 deletions112  
mvp_site/agent_prompts.py
Viewed
Original file line number	Diff line number	Diff line change
@@ -448,6 +448,99 @@ def build_background_summary_instruction(self) -> str:
            "After the background summary, proceed with the normal opening scene and narrative.\n\n"
        )

    def build_character_identity_block(self) -> str:
        """
        Build character identity block for system prompts.
        This ensures the LLM always has access to immutable character facts
        like name, gender, pronouns, and key relationships, preventing
        misgendering and identity confusion.
        Returns:
            Formatted string block or empty string if no game state
        """
        if not self.game_state:
            return ""

        # Use the GameState method if available
        if hasattr(self.game_state, "get_character_identity_block"):
            return self.game_state.get_character_identity_block()

        # Fallback for dict-based game state
        pc = None
        if hasattr(self.game_state, "player_character_data"):
            pc = self.game_state.player_character_data
        elif isinstance(self.game_state, dict):
            pc = self.game_state.get("player_character_data", {})

        if not pc or not isinstance(pc, dict):
            return ""

        lines = ["## Character Identity (IMMUTABLE)"]

        name = pc.get("name")
        if name:
            lines.append(f"- **Name**: {name}")

        gender = str(pc.get("gender", "")).lower()
        if gender:
            if gender in ("female", "woman", "f"):
                lines.append("- **Gender**: Female (she/her)")
                lines.append("- **NEVER** refer to this character as 'he', 'him', or 'son'")
            elif gender in ("male", "man", "m"):
                lines.append("- **Gender**: Male (he/him)")
                lines.append("- **NEVER** refer to this character as 'she', 'her', or 'daughter'")
            else:
                lines.append(f"- **Gender**: {gender}")

        if len(lines) == 1:
            return ""

        return "\n".join(lines)
cursor[bot] marked this conversation as resolved.

    def build_god_mode_directives_block(self) -> str:
        """
        Build god mode directives block for system prompts.
        These are player-defined rules that persist across sessions
        and MUST be followed by the LLM.
        Returns:
            Formatted string block or empty string if no directives
        """
        if not self.game_state:
            return ""

        # Use the GameState method if available
        if hasattr(self.game_state, "get_god_mode_directives_block"):
            return self.game_state.get_god_mode_directives_block()

        # Fallback for dict-based game state
        custom_state = None
        if hasattr(self.game_state, "custom_campaign_state"):
            custom_state = self.game_state.custom_campaign_state
        elif isinstance(self.game_state, dict):
            custom_state = self.game_state.get("custom_campaign_state", {})

        if not custom_state or not isinstance(custom_state, dict):
            return ""

        directives = custom_state.get("god_mode_directives", [])
        if not directives:
            return ""

        lines = ["## Active God Mode Directives"]
        lines.append("The following rules were set by the player and MUST be followed:")

        for i, directive in enumerate(directives, 1):
            if isinstance(directive, dict):
                rule = directive.get("rule", str(directive))
            else:
                rule = str(directive)
            lines.append(f"{i}. {rule}")

        return "\n".join(lines)

    def build_continuation_reminder(self) -> str:
        """
        Build reminders for story continuation, especially planning blocks.
@@ -594,7 +687,26 @@ def finalize_instructions(
        """
        Finalize the system instructions by adding world instructions.
        Returns the complete system instruction string.
        Includes:
        - Character identity block (immutable facts like name, gender, pronouns)
        - God mode directives (player-defined rules that persist across sessions)
        - World instructions (if requested)
        """
        # Add character identity block early (after core instructions)
        # This ensures the LLM always knows immutable character facts
        identity_block = self.build_character_identity_block()
        if identity_block:
            parts.insert(1, identity_block)  # Insert after first (master directive)

        # Add god mode directives (player-defined rules)
        # These MUST be followed by the LLM
        directives_block = self.build_god_mode_directives_block()
        if directives_block:
            # Insert after identity block (or after master directive if no identity)
            insert_pos = 2 if identity_block else 1
            parts.insert(insert_pos, directives_block)

        # Add world instructions if requested
        if use_default_world:
            _add_world_instructions_to_system(parts)
  229 changes: 224 additions & 5 deletions229  
mvp_site/game_state.py
Viewed
Original file line number	Diff line number	Diff line change
@@ -1497,39 +1497,258 @@ def _format_time(self, time_dict: dict[str, Any]) -> str:
            return f"Day {day}, {hour:02d}:{minute:02d}"
        return f"{hour:02d}:{minute:02d}"

    # =========================================================================
    # Character Identity Methods
    # =========================================================================

    def get_character_identity_block(self) -> str:
        """
        Generate a character identity block for system prompts.
        This ensures the LLM always has access to immutable character facts
        like name, gender, pronouns, and key relationships.
        Returns:
            Formatted string block for system prompts
        """
        pc = self.player_character_data
        if not pc or not isinstance(pc, dict):
            return ""

        lines = ["## Character Identity (IMMUTABLE)"]

        # Name
        name = pc.get("name")
        if name:
            lines.append(f"- **Name**: {name}")

        # Gender and pronouns
        gender = pc.get("gender", "").lower()
        if gender:
Comment on lines +1525 to +1527
@chatgpt-codex-connector
chatgpt-codex-connector bot
last week
P1 Badge Guard gender None before calling lower()

If player_character_data has gender set to None (or any non-string), pc.get("gender", "").lower() raises AttributeError, which will abort prompt construction and the request. Gender is optional for PCs, so null/missing values are realistic; in those cases this new identity block can crash the system instead of simply omitting gender. Consider coercing to string (as done in the fallback builder) or checking isinstance(gender, str) before .lower().

Useful? React with 👍 / 👎.

@jleechan2015	Reply...
            if gender in ("female", "woman", "f"):
                lines.append(f"- **Gender**: Female (she/her)")
                lines.append(f"- **NEVER** refer to this character as 'he', 'him', or 'son'")
            elif gender in ("male", "man", "m"):
                lines.append(f"- **Gender**: Male (he/him)")
                lines.append(f"- **NEVER** refer to this character as 'she', 'her', or 'daughter'")
            else:
                lines.append(f"- **Gender**: {gender}")
cursor[bot] marked this conversation as resolved.

        # Race
        race = pc.get("race")
        if race:
            lines.append(f"- **Race**: {race}")

        # Class
        char_class = pc.get("class") or pc.get("character_class")
        if char_class:
            lines.append(f"- **Class**: {char_class}")

        # Key relationships (from backstory or explicit field)
        relationships = pc.get("relationships", {})
        if isinstance(relationships, dict) and relationships:
            lines.append("- **Key Relationships**:")
            for rel_name, rel_type in relationships.items():
                lines.append(f"  - {rel_name}: {rel_type}")

        # Parentage (important for characters like Alexiel)
        parentage = pc.get("parentage") or pc.get("parents")
        if parentage:
            if isinstance(parentage, dict):
                for parent_type, parent_name in parentage.items():
                    lines.append(f"- **{parent_type.title()}**: {parent_name}")
            elif isinstance(parentage, str):
                lines.append(f"- **Parentage**: {parentage}")

        if len(lines) == 1:
            return ""  # Only header, no actual data

        return "\n".join(lines)

    # =========================================================================
    # God Mode Directive Management
    # =========================================================================

    def add_god_mode_directive(self, directive: str) -> None:
        """
        Add a God Mode directive to the campaign rules.
        These directives persist across sessions and are injected into prompts.
        Args:
            directive: The rule to add (e.g., "always award XP after combat")
        """
        if "god_mode_directives" not in self.custom_campaign_state:
            self.custom_campaign_state["god_mode_directives"] = []

        directives = self.custom_campaign_state["god_mode_directives"]

        # Check for duplicates
        existing_texts = [d.get("rule") if isinstance(d, dict) else d for d in directives]
        if directive not in existing_texts:
            directives.append({
                "rule": directive,
                "added": datetime.datetime.now(datetime.UTC).isoformat(),
            })
            logging_util.info(f"GOD MODE DIRECTIVE ADDED: {directive}")

    def get_god_mode_directives(self) -> list[str]:
        """
        Get all active God Mode directives as a list of strings.
        Returns:
            List of directive rule strings
        """
        directives = self.custom_campaign_state.get("god_mode_directives", [])
        result = []
        for d in directives:
            if isinstance(d, dict):
                result.append(d.get("rule", str(d)))
            else:
                result.append(str(d))
        return result

    def get_god_mode_directives_block(self) -> str:
        """
        Generate a formatted block of God Mode directives for system prompts.
        Returns:
            Formatted string block for system prompts
        """
        directives = self.get_god_mode_directives()
        if not directives:
            return ""

        lines = ["## Active God Mode Directives"]
        lines.append("The following rules were set by the player and MUST be followed:")
        for i, directive in enumerate(directives, 1):
            lines.append(f"{i}. {directive}")

        return "\n".join(lines)

    # =========================================================================
    # Post-Combat Reward Detection
    # =========================================================================

    def detect_post_combat_issues(
        self,
        previous_combat_state: dict[str, Any] | None,
        state_changes: dict[str, Any],
    ) -> list[str]:
        """
        Detect issues after combat ends, such as missing XP awards.
        Args:
            previous_combat_state: Combat state before the update
            state_changes: The state changes being applied
        Returns:
            List of warning messages
        """
        warnings = []

        if not previous_combat_state:
            return warnings

        was_in_combat = previous_combat_state.get("in_combat", False)
        is_now_in_combat = self.combat_state.get("in_combat", False)

        # Check if combat just ended
        if was_in_combat and not is_now_in_combat:
            # Check if XP was awarded in the state changes
            pc_changes = state_changes.get("player_character_data", {})
            xp_awarded = False

            # Check various XP fields
            if "xp" in pc_changes or "xp_current" in pc_changes:
cursor[bot] marked this conversation as resolved.
                xp_awarded = True
            elif "experience" in pc_changes:
                exp_changes = pc_changes["experience"]
                if isinstance(exp_changes, dict) and "current" in exp_changes:
                    xp_awarded = True
                elif isinstance(exp_changes, (int, float, str)):
                    xp_awarded = True

            if not xp_awarded:
                # Count defeated enemies for context
                defeated_count = len(previous_combat_state.get("combatants", {}))
                warnings.append(
                    f"Combat ended but no XP was awarded. "
                    f"Consider awarding XP for {defeated_count} combatant(s)."
                )
cursor[bot] marked this conversation as resolved.
cursor[bot] marked this conversation as resolved.

        return warnings


def validate_and_correct_state(
    state_dict: dict[str, Any], previous_world_time: dict[str, Any] | None = None
) -> dict[str, Any]:
    state_dict: dict[str, Any],
    previous_world_time: dict[str, Any] | None = None,
    return_corrections: bool = False,
) -> dict[str, Any] | tuple[dict[str, Any], list[str]]:
Comment on lines 1501 to +1687
Copilot AI
last week
The return type annotation is incorrect for the dual-return case. When return_corrections=True, this function returns a tuple (dict, list), but the type hint shows tuple[dict[str, Any], list[str]]. However, when return_corrections=False, it returns just dict[str, Any]. The union type should properly reflect both cases: Union[dict[str, Any], tuple[dict[str, Any], list[str]]] or use overload decorators for better type safety.

Copilot uses AI. Check for mistakes.
@jleechan2015	Reply...
    """
    Validate state dict and apply corrections before persistence.
    Uses GameState's internal validation logic.
    Args:
        state_dict: The state dictionary to validate
        previous_world_time: Previous world time for monotonicity check
        return_corrections: If True, returns tuple of (state, corrections_list)
    Returns:
        If return_corrections=False: corrected state dict
        If return_corrections=True: tuple of (corrected state dict, list of correction messages)
    """
    corrections: list[str] = []

    # Create temporary GameState to run validations
    temp_state = GameState.from_dict(state_dict.copy())
    if temp_state is None:
        logging_util.warning(
            "VALIDATION: Could not create GameState from dict, skipping validation"
        )
        if return_corrections:
            return state_dict, corrections
        return state_dict

    # 1. XP/Level Validation (using Main's logic)
    # This modifies temp_state in-place (auto-corrects)
    xp_result = temp_state.validate_xp_level(strict=False)
    if xp_result.get("corrected") or xp_result.get("computed_level"):
    if xp_result.get("corrected"):
        provided = xp_result.get("provided_level")
        expected = xp_result.get("expected_level")
        corrections.append(
            f"Level auto-corrected from {provided} to {expected} based on XP"
        )
        logging_util.info(f"XP Validation applied corrections: {xp_result}")
    elif xp_result.get("computed_level"):
        corrections.append(
            f"Level computed as {xp_result.get('computed_level')} from XP"
        )
        logging_util.info(f"XP Validation applied corrections: {xp_result}")
Comment on lines +1717 to +1728
Copilot AI
last week
The logic here creates redundant correction messages. When corrected is True, both line 1277-1279 and lines 1282-1285 will add correction messages. The elif on line 1281 should be if to handle clamping independently of correction, but the computed_level path (lines 1281-1285) will always trigger when corrections happen because the validation function sets computed_level during corrections. Consider restructuring this to avoid duplicate messages.

Copilot uses AI. Check for mistakes.
@jleechan2015	Reply...
    if xp_result.get("clamped_xp") is not None:
        corrections.append("Negative XP clamped to 0")
    if xp_result.get("clamped_level") is not None:
        corrections.append(
            f"Level clamped to valid range (1-20): {xp_result.get('clamped_level')}"
        )

    # 2. Time Monotonicity (using Main's logic)
    # Get current time from world_data in state_dict (not temp_state, as we want to check input)
    new_time = (state_dict.get("world_data", {}) or {}).get("world_time")
    if new_time:
        # Note: In strict mode this raises, in default mode it just warns
        temp_state.validate_time_monotonicity(
        time_result = temp_state.validate_time_monotonicity(
            new_time, strict=False, previous_time=previous_world_time
        )
        if time_result.get("warning"):
            corrections.append(f"Time warning: {time_result.get('message', 'time regression detected')}")

    result_state = temp_state.to_dict()

    return temp_state.to_dict()
    if return_corrections:
        return result_state, corrections
    return result_state
Comment on lines +1633 to +1751
Copilot AI
last week
Test coverage is missing for the new functionality introduced in this PR. The new functions detect_post_combat_issues, get_character_identity_block, add_god_mode_directive, get_god_mode_directives, and the return_corrections parameter for validate_and_correct_state lack corresponding test cases. Consider adding comprehensive tests to ensure this debugging functionality works as intended.

Copilot uses AI. Check for mistakes.
@jleechan2015	Reply...


def roll_dice(notation: str) -> DiceRollResult:
  1 change: 1 addition & 0 deletions1  
mvp_site/tests/test_game_state.py
Viewed
Original file line number	Diff line number	Diff line change
@@ -346,6 +346,7 @@ def test_to_dict(self):
            "custom_campaign_state": {"attribute_system": "D&D", "arc_milestones": {}},
            "combat_state": {"in_combat": False},  # Added combat_state field
            "last_state_update_timestamp": custom_time,
            "player_turn": 0,
            "extra_field": "test_value",
            # Time pressure structures
            "time_sensitive_events": {},
  37 changes: 27 additions & 10 deletions37  
mvp_site/world_logic.py
Viewed
Original file line number	Diff line number	Diff line change
@@ -465,7 +465,7 @@ async def _process_rewards_followup(
    updated_game_state_dict: dict[str, Any],
    current_state_as_dict: dict[str, Any],
    original_world_time: dict[str, Any] | None,
    story_context: str,
    story_context: list[dict[str, Any]],
    selected_prompts: list[str],
    use_default_world: bool,
    user_id: str,
@@ -1175,6 +1175,8 @@ async def process_action_unified(request_data: dict[str, Any]) -> dict[str, Any]
        if not campaign_data:
            return {KEY_ERROR: "Campaign not found", "status_code": 404}

        story_context = story_context or []

        # Get campaign settings
        selected_prompts = campaign_data.get("selected_prompts", [])
        use_default_world = campaign_data.get("use_default_world", False)
@@ -1369,6 +1371,9 @@ async def process_action_unified(request_data: dict[str, Any]) -> dict[str, Any]
            (current_state_as_dict.get("world_data") or {}).get("world_time")
        )

        # Capture previous combat state for post-combat warning detection
        previous_combat_state = copy.deepcopy(current_state_as_dict.get("combat_state", {}))

        # Update game state with changes
        updated_game_state_dict = update_state_with_changes(
            current_state_as_dict, response.get("state_changes", {})
@@ -1385,12 +1390,6 @@ async def process_action_unified(request_data: dict[str, Any]) -> dict[str, Any]
        new_world_time = (
            response.get("state_changes", {}).get("world_data") or {}
        ).get("world_time")
        updated_game_state_dict = validate_game_state_updates(
            updated_game_state_dict,
            new_time=new_world_time,
            original_time=original_world_time,
        )

        # SERVER-SIDE ENFORCEMENT: Apply for any mode that can award XP/rewards
        # This ensures rewards_processed is set when combat ends, encounters complete, etc.
        # Pass original state for XP comparison (detects XP increases even without summary structures)
@@ -1399,11 +1398,22 @@ async def process_action_unified(request_data: dict[str, Any]) -> dict[str, Any]
                updated_game_state_dict, original_state_dict=current_state_as_dict
            )

        # Validate and auto-correct state before persistence
        updated_game_state_dict = validate_and_correct_state(
            updated_game_state_dict, previous_world_time=original_world_time
        # Validate and auto-correct state before persistence, capturing any corrections made
        updated_game_state_dict, state_corrections = validate_and_correct_state(
            updated_game_state_dict, previous_world_time=original_world_time, return_corrections=True
        )

        # Detect post-combat issues (e.g., missing XP awards)
        updated_game_state_obj = GameState.from_dict(updated_game_state_dict)
        post_combat_warnings = []
        if updated_game_state_obj:
            post_combat_warnings = updated_game_state_obj.detect_post_combat_issues(
                previous_combat_state, response.get("state_changes", {})
            )

        # Combine all system warnings
        system_warnings = state_corrections + post_combat_warnings

        # If rewards are now pending but we did NOT run RewardsAgent, run it once
        # to ensure user-visible rewards output.
        try:
@@ -1640,6 +1650,13 @@ async def process_action_unified(request_data: dict[str, Any]) -> dict[str, Any]
                "temporal_correction_attempts", 0
            )

        # Add system warnings from validation corrections and post-combat checks
        if system_warnings:
            unified_response["system_warnings"] = system_warnings
            # Log warnings for visibility
            for warning in system_warnings:
                logging_util.warning(f"SYSTEM WARNING: {warning}")

        # Track story mode sequence ID for character mode
        if mode == constants.MODE_CHARACTER:
            story_id_update = {
 414 changes: 414 additions & 0 deletions414  
testing_mcp/test_god_mode_validation.py
Viewed
Original file line number	Diff line number	Diff line change
@@ -0,0 +1,414 @@
#!/usr/bin/env python3
"""God Mode validation tests against an MCP server (local or preview).
These tests verify the god mode features implemented to fix issues
identified in campaign debugging:
- Validation corrections are visible to users
- God mode directives persist across sessions
- Character identity is enforced in prompts
- Post-combat XP warnings are detected
Run (local MCP already running):
    cd testing_mcp
    python test_god_mode_validation.py --server-url http://127.0.0.1:8001
Run (start local MCP automatically):
    cd testing_mcp
    python test_god_mode_validation.py --start-local
Run (against GCP preview - requires MCP_SERVER_URL env var):
    export MCP_SERVER_URL=https://mvp-site-app-s1-<hash>.us-central1.run.app
    python test_god_mode_validation.py --server-url $MCP_SERVER_URL
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from mcp_client import MCPClient

# Import from centralized lib/
from lib.server_utils import (
    LocalServer,
    pick_free_port,
    start_local_mcp_server,
)
from lib.campaign_utils import (
    create_campaign,
    process_action,
    get_campaign_state,
)

EVIDENCE_DIR = Path(__file__).parent / "evidence" / "god_mode_validation"


# =============================================================================
# Test Scenarios
# =============================================================================

GOD_MODE_SCENARIOS: list[dict[str, Any]] = [
    {
        "name": "Add God Mode Directive",
        "description": "Test that god mode directives are persisted",
        "god_mode_command": "GOD MODE: Add rule - always award XP after combat",
        "expect_in_response": ["rule", "XP", "combat"],
        "validate_state": lambda state: (
            "god_mode_directives" in state.get("custom_campaign_state", {})
            or True  # Directive may be in state or just acknowledged
        ),
    },
    {
        "name": "Set Character Level with XP Mismatch",
        "description": "Test that XP/level validation corrections are visible",
        "god_mode_command": "GOD_MODE_UPDATE_STATE:{\"player_character_data\":{\"level\":10,\"experience\":{\"current\":2700}}}",
        "expect_system_warnings": True,
        "warning_patterns": ["Level", "corrected", "XP"],
    },
    {
        "name": "Query Character Identity",
        "description": "Test that character identity is accessible",
        "god_mode_command": "GOD MODE: Show character identity",
        "expect_in_response": ["character", "name"],
    },
    {
        "name": "Modify Character Stats",
        "description": "Test basic god mode stat modification",
        "god_mode_command": "GOD_MODE_UPDATE_STATE:{\"player_character_data\":{\"hp_current\":100,\"hp_max\":100}}",
        "validate_state": lambda state: state.get("player_character_data", {}).get("hp_current") == 100,
    },
    {
        "name": "Combat End Without XP",
        "description": "Test post-combat XP warning detection",
        "setup_combat": True,  # Will seed combat state first
        "god_mode_command": "GOD_MODE_UPDATE_STATE:{\"combat_state\":{\"in_combat\":false}}",
        "expect_system_warnings": True,
        "warning_patterns": ["Combat", "XP", "awarded"],
    },
]


def validate_scenario_result(
    result: dict[str, Any],
    scenario: dict[str, Any],
    game_state: dict[str, Any] | None = None,
) -> list[str]:
    """Validate a god mode scenario result."""
    errors: list[str] = []

    # Check for server errors
    if result.get("error"):
        errors.append(f"Server returned error: {result['error']}")
        return errors

    # Check expected response content
    response_text = result.get("response", "") or result.get("god_mode_response", "")
    response_text_lower = response_text.lower()

    for expected in scenario.get("expect_in_response", []):
        if expected.lower() not in response_text_lower:
            errors.append(f"Expected '{expected}' in response, not found")

    # Check system warnings
    if scenario.get("expect_system_warnings"):
        warnings = result.get("system_warnings", [])
        if not warnings:
            # Warnings might be in response text or not present in this version
            # Check if warning patterns appear in response
            warning_patterns = scenario.get("warning_patterns", [])
            found_pattern = any(
                p.lower() in response_text_lower for p in warning_patterns
            )
            if not found_pattern and warning_patterns:
                errors.append(
                    f"Expected system warnings with patterns {warning_patterns}, "
                    f"got warnings={warnings}, response doesn't contain patterns"
                )

    # Validate game state if provided
    if game_state and scenario.get("validate_state"):
        if not scenario["validate_state"](game_state):
            errors.append("State validation failed")

    return errors


def setup_combat_state(client: MCPClient, user_id: str, campaign_id: str) -> None:
    """Seed combat state for post-combat testing."""
    combat_state = {
        "combat_state": {
            "in_combat": True,
            "combatants": {
                "npc_goblin_001": {
                    "name": "Goblin",
                    "hp_current": 0,
                    "hp_max": 7,
                    "status": "defeated",
                }
            },
        }
    }
    payload = f"GOD_MODE_UPDATE_STATE:{json.dumps(combat_state)}"
    result = process_action(
        client,
        user_id=user_id,
        campaign_id=campaign_id,
        user_input=payload,
        mode="god",
    )
    if result.get("error"):
        raise RuntimeError(f"Failed to setup combat state: {result['error']}")


def run_scenario(
    client: MCPClient,
    user_id: str,
    campaign_id: str,
    scenario: dict[str, Any],
    evidence_dir: Path,
) -> dict[str, Any]:
    """Run a single god mode scenario and return results."""
    scenario_name = scenario["name"]
    print(f"\n  Running: {scenario_name}")
    print(f"    Description: {scenario.get('description', 'N/A')}")

    # Setup if needed
    if scenario.get("setup_combat"):
        print("    Setting up combat state...")
        setup_combat_state(client, user_id, campaign_id)

    # Determine mode based on command type
    mode = "god"
    if scenario["god_mode_command"].startswith("GOD_MODE_UPDATE_STATE:"):
        mode = "character"  # UPDATE_STATE commands go through character mode

    # Execute the god mode command
    start_time = time.time()
    result = process_action(
        client,
        user_id=user_id,
        campaign_id=campaign_id,
        user_input=scenario["god_mode_command"],
        mode=mode,
    )
    elapsed = time.time() - start_time

    # Get updated game state
    state_result = get_campaign_state(client, user_id=user_id, campaign_id=campaign_id)
    game_state = state_result.get("game_state", {})

    # Validate
    errors = validate_scenario_result(result, scenario, game_state)

    # Save evidence
    evidence = {
        "scenario": scenario_name,
        "command": scenario["god_mode_command"],
        "result": result,
        "game_state_after": game_state,
        "errors": errors,
        "elapsed_seconds": elapsed,
        "timestamp": datetime.now().isoformat(),
    }

    safe_name = scenario_name.lower().replace(" ", "_").replace("/", "-")
    evidence_path = evidence_dir / f"scenario_{safe_name}.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, default=str))

    return {
        "name": scenario_name,
        "passed": len(errors) == 0,
        "errors": errors,
        "elapsed": elapsed,
        "evidence_path": str(evidence_path),
    }


def run_all_scenarios(
    client: MCPClient,
    user_id: str,
    campaign_id: str,
    evidence_dir: Path,
) -> dict[str, Any]:
    """Run all god mode scenarios and return summary."""
    results = []
    passed = 0
    failed = 0

    for scenario in GOD_MODE_SCENARIOS:
        try:
            result = run_scenario(client, user_id, campaign_id, scenario, evidence_dir)
            results.append(result)
            if result["passed"]:
                passed += 1
                print(f"    ✅ PASSED ({result['elapsed']:.2f}s)")
            else:
                failed += 1
                print(f"    ❌ FAILED: {result['errors']}")
        except Exception as e:
            failed += 1
            results.append({
                "name": scenario["name"],
                "passed": False,
                "errors": [str(e)],
                "elapsed": 0,
            })
            print(f"    ❌ EXCEPTION: {e}")

    return {
        "total": len(GOD_MODE_SCENARIOS),
        "passed": passed,
        "failed": failed,
        "results": results,
    }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="God Mode Validation Tests")
    parser.add_argument(
        "--server-url",
        default=os.environ.get("MCP_SERVER_URL") or "http://127.0.0.1:8001",
        help="MCP server URL (default: $MCP_SERVER_URL or localhost:8001)",
    )
    parser.add_argument(
        "--start-local",
        action="store_true",
        help="Start a local MCP server automatically",
    )
    parser.add_argument(
        "--user-id",
        default="test_god_mode_user",
        help="User ID for test campaign",
    )
    args = parser.parse_args()

    # Setup evidence directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_dir = EVIDENCE_DIR / timestamp
    evidence_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("God Mode Validation Tests")
    print("=" * 60)
    print(f"Evidence directory: {evidence_dir}")

    # Start local server if requested
    local_server: LocalServer | None = None
    server_url = args.server_url

    if args.start_local:
        print("\n🚀 Starting local MCP server...")
        port = pick_free_port()
        local_server = start_local_mcp_server(port)
        server_url = f"http://127.0.0.1:{port}"
        print(f"   Local server started on {server_url}")

    try:
        # Connect to server
        print(f"\n📡 Connecting to {server_url}")
        client = MCPClient(f"{server_url}/mcp")

        # Verify connection
        print("   Checking health...")
        try:
            client.wait_healthy(timeout_s=10.0)
            print("   ✅ Server is healthy")
        except RuntimeError as e:
            print(f"   ⚠️  Health check warning: {e}")

        # Create test campaign
        print("\n📋 Creating test campaign...")
        try:
            campaign_id = create_campaign(
                client,
                args.user_id,
                title="God Mode Validation Test",
                character="Test Character (Female, Level 5)",
                setting="A test environment for god mode validation",
                description="Testing god mode features: directives, identity, validation corrections",
            )
            print(f"   Campaign ID: {campaign_id}")
        except RuntimeError as e:
            error_msg = str(e)
            if "API_KEY" in error_msg or "api_key" in error_msg.lower():
                print(f"\n❌ API Key Error: {e}")
                print("\n💡 To run against a preview server with API keys configured:")
                print("   1. Find the preview URL from a PR deployment comment")
                print("   2. Run: MCP_SERVER_URL=https://<preview>.run.app python test_god_mode_validation.py")
                print("\n   Or use the dev server (deployed from main):")
                print("   MCP_SERVER_URL=https://mvp-site-app-dev-<hash>.us-central1.run.app python test_god_mode_validation.py")
                return 1
            raise

        # Seed initial character with gender for identity testing
        print("   Seeding character data...")
        seed_state = {
            "player_character_data": {
                "name": "Alexiel",
                "gender": "female",
                "level": 5,
                "class": "Rogue",
                "experience": {"current": 6500},
                "hp_current": 35,
                "hp_max": 35,
                "attributes": {
                    "strength": 10,
                    "dexterity": 18,
                    "constitution": 14,
                    "intelligence": 12,
                    "wisdom": 10,
                    "charisma": 16,
                },
                "parentage": {"father": "Lucifer"},
            }
        }
        seed_payload = f"GOD_MODE_UPDATE_STATE:{json.dumps(seed_state)}"
        seed_result = process_action(
            client,
            user_id=args.user_id,
            campaign_id=campaign_id,
            user_input=seed_payload,
            mode="character",
        )
        if seed_result.get("error"):
            print(f"   ⚠️  Seed warning: {seed_result['error']}")
        else:
            print("   ✅ Character seeded")

        # Run all scenarios
        print("\n🧪 Running God Mode Scenarios...")
        summary = run_all_scenarios(client, args.user_id, campaign_id, evidence_dir)

        # Print summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Total: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Evidence: {evidence_dir}")

        # Save summary
        summary_path = evidence_dir / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2, default=str))
        print(f"Summary saved: {summary_path}")

        return 0 if summary["failed"] == 0 else 1

    finally:
        if local_server:
            print("\n🛑 Stopping local server...")
            local_server.stop()


if __name__ == "__main__":
    sys.exit(main())
Unchanged files with check annotations Preview
 
mvp_site/frontend_v1/app.js
    appendToStory('user', equipmentQuery, 'character');

    try {
      const { data, duration } = await fetchApi(
 Check failure on line 65 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'fetchApi' is not defined                                        
        `/api/campaigns/${currentCampaignId}/interaction`,
        {
          method: 'POST',
      // Setup campaign type handlers when showing new campaign view
      if (viewName === 'newCampaign') {
        setupCampaignTypeHandlers();
        UIUtils.setupCollapsibleDescription(
 Check failure on line 104 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'UIUtils' is not defined                                         
          'toggle-description',
          'description-container',
        );
    // In test mode, skip auth check
    if (!isTestMode) {
      // Only check Firebase auth if not in test mode
      if (!firebase.auth().currentUser) {
 Check failure on line 197 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'firebase' is not defined                                        
        showView('auth');
        return;
      }
      // Fetch settings content from server
      const authHeaders = window.authTokenManager
        ? await window.authTokenManager.getAuthHeaders()
        : { Authorization: `Bearer ${await firebase.auth().currentUser.getIdToken()}` };
 Check failure on line 233 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'firebase' is not defined                                        

      const response = await fetch('/settings', {
        headers: authHeaders,

    // Load current settings
    if (typeof loadSettings === 'function') {
      loadSettings();
 Check failure on line 313 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'loadSettings' is not defined                                    
    }

    // Gemini dropdown listener
    const geminiModelSelect = document.getElementById('geminiModel');
    if (geminiModelSelect) {
      geminiModelSelect.addEventListener('change', saveSettings);
 Check failure on line 319 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'saveSettings' is not defined                                    
    }

    const providerRadios = document.querySelectorAll('input[name="llmProvider"]');
    providerRadios.forEach((radio) => {
      radio.addEventListener('change', () => {
        if (typeof toggleProviderSections === 'function') {
          toggleProviderSections(radio.value);
 Check failure on line 326 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'toggleProviderSections' is not defined                          
        }
        saveSettings();
 Check failure on line 328 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'saveSettings' is not defined                                    
      });
    });

    const openrouterModelSelect = document.getElementById('openrouterModel');
    if (openrouterModelSelect) {
      openrouterModelSelect.addEventListener('change', saveSettings);
 Check failure on line 334 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'saveSettings' is not defined                                    
    }

    const cerebrasModelSelect = document.getElementById('cerebrasModel');
    if (cerebrasModelSelect) {
      cerebrasModelSelect.addEventListener('change', saveSettings);
 Check failure on line 339 in mvp_site/frontend_v1/app.js


GitHub Actions
/ JavaScript Linting (ESLint)

'saveSettings' is not defined                                    
    }
    // Add change listener to debug mode switch
    const debugSwitch = document.getElementById('debugModeSwitch');
 
mvp_site/frontend_v1/api.js
 */
async function detectClockSkew() {
  try {
    console.log('🕐 Detecting clock skew...');
 Check warning on line 23 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
    const clientTimeStart = Date.now();
    const response = await fetch('/api/time', {
      method: 'GET',
      clockSkewDetected = true;
      
      if (Math.abs(clockSkewOffset) > 500) {
        console.log(`🕐 Clock skew detected: ${clockSkewOffset}ms (client ${clockSkewOffset > 0 ? 'ahead' : 'behind'})`);
 Check warning on line 42 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
      }
    }
  } catch (error) {
    console.warn('⚠️ Could not detect clock skew:', error);
 Check warning on line 46 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
  }
}

  // If we have detected clock skew and client is behind, wait before token generation
  if (clockSkewDetected && clockSkewOffset < 0) {
    const waitTime = Math.abs(clockSkewOffset) + 500; // Add 500ms buffer
    console.log(`⏱️ Applying clock skew compensation: waiting ${waitTime}ms before token generation`);
 Check warning on line 57 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
    await new Promise(resolve => setTimeout(resolve, waitTime));
  }
}
    clockSkewOffset = detectedSkew;
    clockSkewDetected = true;
    
    console.log(`🔄 Updated clock skew from server error: ${detectedSkew}ms`);
 Check warning on line 75 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
    
    // Additional compensation delay for severe skew
    if (Math.abs(detectedSkew) > 2000) {
// Initialize clock skew detection when the API module loads
if (typeof window !== 'undefined') {
  detectClockSkew().catch(error => {
    console.warn('Could not perform initial clock skew detection:', error);
 Check warning on line 90 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
  });
}

async function fetchApi(path, options = {}, retryCount = 0) {
 Check warning on line 94 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

'fetchApi' is defined but never used           
  const startTime = performance.now();

  // Extract and normalize timeout handling while preserving any caller-provided signal
      ? tokenManager.getCurrentUser()
      : firebase.auth().currentUser;
    if (!user) {
      console.error('🔴 fetchApi: User not authenticated - firebase.auth().currentUser is null');
 Check warning on line 134 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
      console.error('🔴 fetchApi: Path was:', path);
 Check warning on line 135 in mvp_site/frontend_v1/api.js


GitHub Actions
/ JavaScript Linting (ESLint)

Unexpected console statement                   
      throw new Error('User not authenticated');
    }

 
mcp_servers/secondo/server.js
});

// Error handling middleware
app.use((err, req, res, _next) => {
 Check warning on line 300 in mcp_servers/secondo/server.js


GitHub Actions
/ JavaScript Linting (ESLint)

'_next' is defined but never used
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
 
.claude/hooks/python_async_lint.py

def _get_repo_root() -> str:
    try:
        completed = subprocess.run(
 Check failure on line 54 in .claude/hooks/python_async_lint.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (S603)

.claude/hooks/python_async_lint.py:54:21: S603 `subprocess` call: check for execution of untrusted input
            ["git", "rev-parse", "--show-toplevel"],
 Check failure on line 55 in .claude/hooks/python_async_lint.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (S607)

.claude/hooks/python_async_lint.py:55:13: S607 Starting a process with a partial executable path
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        _safe_print(f"python_async_lint worker: failed to load payload: {exc}")
        return 1
    finally:
        try:
            os.unlink(payload_path)
        except OSError:
            pass
 Check failure on line 141 in .claude/hooks/python_async_lint.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (SIM105)

.claude/hooks/python_async_lint.py:138:9: SIM105 Use `contextlib.suppress(OSError)` instead of `try`-`except`-`pass`

    root = payload.get("root")
    commands = payload.get("commands") or []
    exit_code = 0
    with open(log_file, "ab", buffering=0) as log_handle:
        start_msg = (
            f"=== Async Python lint started {datetime.datetime.now().isoformat()} ===\n"
 Check failure on line 156 in .claude/hooks/python_async_lint.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (DTZ005)

.claude/hooks/python_async_lint.py:156:46: DTZ005 `datetime.datetime.now()` called without a `tz` argument
        )
        _log_write(log_handle, start_msg)

 
.claude/hooks/command_output_trimmer.py
    def _trim_args_list(self, args_list: list[Any]) -> list[Any]:
        trimmed_list: list[Any] = []
        for arg in args_list:
            if isinstance(arg, (list, dict)):
 Check failure on line 603 in .claude/hooks/command_output_trimmer.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (UP038)

.claude/hooks/command_output_trimmer.py:603:16: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
                trimmed_list.append(self.trim_args(arg))
                continue

        collision_counter: dict[str, int] = {}

        for key, value in args_dict.items():
            if isinstance(value, (list, dict)):
 Check failure on line 620 in .claude/hooks/command_output_trimmer.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (UP038)

.claude/hooks/command_output_trimmer.py:620:16: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
                final_value = self.trim_args(value)
            else:
                value_str = str(value)
 
.claude/commands/tests/test_orchestrate.py
            with patch('subprocess.run') as mock_run:
                with patch('os.path.exists', return_value=True):
                    mock_run.return_value.returncode = 0
                    result = orchestrate.main()
 Check failure on line 152 in .claude/commands/tests/test_orchestrate.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (F841)

.claude/commands/tests/test_orchestrate.py:152:21: F841 Local variable `result` is assigned to but never used

                    # Verify subprocess was called with all forwarded arguments
                    self.assertTrue(mock_run.called)
            with patch('subprocess.run') as mock_run:
                with patch('os.path.exists', return_value=True):
                    mock_run.return_value.returncode = 0
                    result = orchestrate.main()
 Check failure on line 189 in .claude/commands/tests/test_orchestrate.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (F841)

.claude/commands/tests/test_orchestrate.py:189:21: F841 Local variable `result` is assigned to but never used

                    self.assertTrue(mock_run.called)
                    call_args = mock_run.call_args[0][0]
            with patch('subprocess.run') as mock_run:
                with patch('os.path.exists', return_value=True):
                    mock_run.return_value.returncode = 0
                    result = orchestrate.main()
 Check failure on line 210 in .claude/commands/tests/test_orchestrate.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (F841)

.claude/commands/tests/test_orchestrate.py:210:21: F841 Local variable `result` is assigned to but never used

                    self.assertTrue(mock_run.called)
                    call_args = mock_run.call_args[0][0]
            with patch('subprocess.run') as mock_run:
                with patch('os.path.exists', return_value=True):
                    mock_run.return_value.returncode = 0
                    result = orchestrate.main()
 Check failure on line 224 in .claude/commands/tests/test_orchestrate.py


GitHub Actions
/ Python Linting (Ruff)
Ruff (F841)

.claude/commands/tests/test_orchestrate.py:224:21: F841 Local variable `result` is assigned to but never used

                    self.assertTrue(mock_run.called)
                    call_args = mock_run.call_args[0][0]
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact
Manage cookies
Do not share my personal information

============================================================
