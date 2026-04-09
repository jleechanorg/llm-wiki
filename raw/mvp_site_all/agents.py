"""
Agent Architecture for WorldArchitect.AI

This module provides the agent architecture for handling different interaction
modes in the game. Each agent encapsulates mode-specific logic and has a focused
subset of system prompts.

Class Hierarchy:
- BaseAgent: Abstract base class with common functionality
  - FixedPromptAgent: Base for agents with fixed prompt sets
    - GodModeAgent: Handles administrative commands (god mode)
    - PlanningAgent: Handles strategic planning (think mode)
    - InfoAgent: Handles equipment/inventory queries (trimmed prompts)
    - RewardsAgent: Handles rewards, loot, and progression-related logic
  - StoryModeAgent: Handles narrative storytelling with living world (character mode)
  - CombatAgent: Handles active combat encounters (combat mode)

Agent Selection Priority (used by get_agent_for_input):
1. GodModeAgent: Administrative commands (highest priority)
2. Character creation completion override (transition to StoryModeAgent)
3. CampaignUpgradeAgent: Ascension ceremonies (divine/sovereign) - STATE-BASED
4. CharacterCreationAgent: Character creation flow (creation focus) - STATE-BASED
5. PlanningAgent: Strategic planning (think mode) - EXPLICIT OVERRIDE
6. Semantic Intent Classifier (PRIMARY BRAIN): Routes based on semantic analysis of user input
   - Uses FastEmbed (BAAI/bge-small-en-v1.5) to classify intent
   - Can route to: CombatAgent, RewardsAgent, InfoAgent, CharacterCreationAgent, LevelUpAgent, CampaignUpgradeAgent, PlanningAgent, FactionManagementAgent
   - Falls back to StoryModeAgent if no match
7. API explicit mode override (if provided)
8. StoryModeAgent: Default narrative storytelling

Usage:
    from mvp_site.agents import (
        get_agent_for_input,
        StoryModeAgent,
        GodModeAgent,
        PlanningAgent,
        InfoAgent,
        CombatAgent,
    )

    # Get appropriate agent for user input
    agent = get_agent_for_input(user_input, game_state)

    # Build system instructions
    instructions = agent.build_system_instructions(
        selected_prompts=["narrative", "mechanics"],
        use_default_world=False
    )

Each agent has:
- REQUIRED_PROMPTS: Prompts that are always loaded
- OPTIONAL_PROMPTS: Prompts that may be conditionally loaded
- MODE: The mode identifier for this agent
"""

from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from mvp_site import constants, intent_classifier, logging_util
from mvp_site.agent_prompts import PromptBuilder, _load_instruction_file
from mvp_site.faction.tools import FACTION_TOOLS
from mvp_site.faction_state_util import is_faction_minigame_enabled

if TYPE_CHECKING:
    from mvp_site.game_state import GameState

# ============================================================================
# CONSTANTS
# ============================================================================

# NOTE: DIALOG_KEYWORDS removed - ALL dialog routing uses classifier only
# See CLAUDE.md: "NO KEYWORD MATCHING for dialog detection"


# ============================================================================
# PROMPT ORDER INVARIANTS
# ============================================================================
# These invariants ensure consistent prompt loading order across all agents.
# The LLM processes prompts in order, so the head order establishes authority.

# Mandatory head order invariants:
# 1. master_directive MUST be first (establishes authority)
# 2. game_state and planning_protocol MUST be consecutive (anchors schema)
#    - Mode-specific prompts (god_mode, think) may appear between master_directive
#      and the game_state→planning_protocol pair, but not between those two elements

MANDATORY_FIRST_PROMPT = constants.PROMPT_TYPE_MASTER_DIRECTIVE
GAME_STATE_PLANNING_PAIR = (
    constants.PROMPT_TYPE_GAME_STATE,
    constants.PROMPT_TYPE_PLANNING_PROTOCOL,
)
EXPLICIT_SEMANTIC_INTENT_THRESHOLD = 0.8


def _extract_current_xp(player_data: Any) -> int:
    """Extract current XP from canonical and legacy player_character_data formats."""
    if not isinstance(player_data, dict):
        return 0

    xp_raw = None
    experience = player_data.get("experience")
    if isinstance(experience, dict):
        xp_raw = experience.get("current")
    elif experience is not None:
        xp_raw = experience

    if xp_raw is None:
        xp_raw = player_data.get("xp") or player_data.get("xp_current")

    if isinstance(xp_raw, str):
        xp_raw = xp_raw.replace(",", "")

    try:
        return max(0, int(xp_raw))
    except (TypeError, ValueError):
        return 0


def _is_stale_level_up_pending(
    custom_state: dict[str, Any],
    rewards_pending: dict[str, Any],
    player_data: dict[str, Any],
) -> bool:
    """True when level_up_pending is set but XP/rewards do not support level-up."""
    if not isinstance(custom_state, dict) or not custom_state.get("level_up_pending"):
        return False
    if custom_state.get("level_up_in_progress"):
        return False
    if isinstance(rewards_pending, dict) and rewards_pending.get("level_up_available"):
        return False

    level_raw = player_data.get("level") if isinstance(player_data, dict) else 1
    try:
        current_level = int(level_raw)
    except (TypeError, ValueError):
        current_level = 1
    current_level = max(1, current_level)

    next_level_xp = constants.get_xp_for_level(current_level + 1)
    current_xp = _extract_current_xp(player_data)
    return current_xp < next_level_xp


def validate_prompt_order(
    order: tuple[str, ...], agent_name: str = "unknown"
) -> list[str]:
    """
    Validate that prompt order satisfies head invariants.

    Invariants checked:
    1. master_directive is first (index 0)
    2. game_state and planning_protocol are consecutive (game_state → planning_protocol)

    Args:
        order: Ordered tuple of prompt types
        agent_name: Agent name for error messages

    Returns:
        List of validation errors (empty if valid)
    """
    errors: list[str] = []

    if not order:
        errors.append(f"{agent_name}: REQUIRED_PROMPT_ORDER is empty")
        return errors

    # Invariant 0b: duplicates not allowed (catch early, with indices)
    seen: dict[str, int] = {}
    for idx, prompt in enumerate(order):
        if prompt in seen:
            errors.append(
                f"{agent_name}: Duplicate prompt type in REQUIRED_PROMPT_ORDER: "
                f"{prompt!r} at indices {seen[prompt]} and {idx}"
            )
        else:
            seen[prompt] = idx

    # Invariant 1: master_directive must be first
    if order[0] != MANDATORY_FIRST_PROMPT:
        errors.append(
            f"{agent_name}: First prompt must be {MANDATORY_FIRST_PROMPT!r}, "
            f"got {order[0]!r}"
        )

    # Invariant 2: game_state and planning_protocol must both exist and be consecutive
    req_gs, req_pp = GAME_STATE_PLANNING_PAIR
    missing_prompts = [p for p in (req_gs, req_pp) if p not in order]
    if missing_prompts:
        missing_list = ", ".join(repr(p) for p in missing_prompts)
        errors.append(
            f"{agent_name}: Missing required prompt(s) in order: {missing_list}"
        )
        return errors  # Can't check adjacency if members are missing

    gs_idx = order.index(req_gs)
    pp_idx = order.index(req_pp)
    if pp_idx != gs_idx + 1:
        errors.append(
            f"{agent_name}: planning_protocol must immediately follow game_state. "
            f"game_state at index {gs_idx}, planning_protocol at {pp_idx}"
        )

    return errors


def _is_spicy_mode_enabled(game_state: GameState | dict | None) -> bool:
    """Check if spicy_mode is enabled in user_settings.

    Handles both GameState objects and dicts with proper type checking.

    Args:
        game_state: GameState object, dict, or None

    Returns:
        True if spicy_mode is explicitly True, False otherwise
    """
    if game_state is None:
        return False
    if isinstance(game_state, dict):
        settings = game_state.get("user_settings")
    else:
        settings = getattr(game_state, "user_settings", None)
    if not isinstance(settings, dict):
        return False
    return settings.get("spicy_mode") is True


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.

    Agents are responsible for:
    - Defining which system prompts they require/support
    - Building system instructions for LLM calls
    - Detecting whether they should handle a given input
    - Pre-processing user input if needed

    Each agent has a focused subset of all possible system prompts,
    allowing it to specialize in its task without prompt overload.

    Attributes:
        REQUIRED_PROMPT_ORDER: Ordered tuple of prompts always loaded (explicit order)
        REQUIRED_PROMPTS: Prompts that are always loaded for this agent (set view)
        OPTIONAL_PROMPTS: Prompts that may be conditionally loaded
        MODE: The mode identifier for this agent
    """

    # Class-level prompt definitions - override in subclasses
    # REQUIRED_PROMPT_ORDER: Explicit ordered tuple (source of truth for order)
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = ()
    # REQUIRED_PROMPTS: Set view for membership testing (derived from order)
    REQUIRED_PROMPTS: frozenset[str] = frozenset()
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()
    MODE: str = ""
    # Cache to avoid re-validating prompt order on every instantiation
    _prompt_order_validated: bool = False

    def __init__(self, game_state: GameState | None = None) -> None:
        """
        Initialize the agent.

        Args:
            game_state: GameState object for dynamic instruction generation.
                        If None, static fallback instructions will be used.
        """
        self._ensure_prompt_order_valid()
        self.game_state = game_state
        self._prompt_builder = PromptBuilder(game_state)

    @property
    def prompt_builder(self) -> PromptBuilder:
        """Access the underlying PromptBuilder for advanced operations."""
        return self._prompt_builder

    @property
    def advances_time(self) -> bool:
        """Whether this agent advances world time during story generation.

        Time-advancing agents (StoryMode, Combat, Dialog, etc.) progress the world
        clock and typically include living_world instruction for background events.
        Non-time-advancing agents override this property to return False.

        Default: True (most agents advance time)
        Override to False for non-advancing agents (e.g., GodMode, Planning,
        Info, CharacterCreation, Rewards, DeferredRewards).

        Note: Living-world prompt inclusion is currently configured explicitly per
        agent via REQUIRED_PROMPT_ORDER and related prompt configuration.
        """
        return True

    @abstractmethod
    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build the complete system instructions for this agent.

        Args:
            selected_prompts: User-selected prompt types (narrative, mechanics, etc.)
            use_default_world: Whether to include world content in instructions
            include_continuation_reminder: Whether to include continuation reminders
            turn_number: Current turn number (used for living world advancement)
            dice_roll_strategy: Dice roll strategy for conditional dice instructions

        Returns:
            Complete system instruction string for the LLM call
        """
        ...  # Abstract method - implemented by subclasses

    @classmethod
    def matches_input(cls, _user_input: str) -> bool:
        """
        Check if this agent should handle the given input.

        Override in subclasses to implement mode-specific detection logic.

        Args:
            _user_input: Raw user input text (unused in base class)

        Returns:
            True if this agent should handle the input
        """
        return False

    @classmethod
    def matches_game_state(cls, _game_state: GameState | None) -> bool:
        """
        Check if this agent should handle the current game state.

        Override in subclasses to implement game-state-based detection logic.

        Args:
            _game_state: Current GameState object (unused in base class)

        Returns:
            True if this agent should handle the game state
        """
        return False

    def preprocess_input(self, user_input: str) -> str:
        """
        Preprocess user input before sending to LLM.

        Override in subclasses if input transformation is needed.

        Args:
            user_input: Raw user input text

        Returns:
            Processed input text
        """
        return user_input

    def get_all_prompts(self) -> frozenset[str]:
        """Get the union of required and optional prompts for this agent."""
        return self.REQUIRED_PROMPTS | self.OPTIONAL_PROMPTS

    @classmethod
    def validate_prompt_order(cls) -> list[str]:
        """
        Validate this agent's REQUIRED_PROMPT_ORDER against head invariants.

        Returns:
            List of validation errors (empty if valid)
        """
        return validate_prompt_order(cls.REQUIRED_PROMPT_ORDER, cls.__name__)

    @classmethod
    def _ensure_prompt_order_valid(cls) -> None:
        """
        Runtime validation hook for prompt order invariants.

        Raises:
            ValueError if REQUIRED_PROMPT_ORDER violates invariants.
        """
        if cls._prompt_order_validated:
            return

        errors = cls.validate_prompt_order()
        if errors:
            logging_util.error(
                "Invalid REQUIRED_PROMPT_ORDER for %s: %s", cls.__name__, errors
            )
            raise ValueError(
                f"Invalid REQUIRED_PROMPT_ORDER for {cls.__name__}: "
                + "; ".join(errors)
            )

        cls._prompt_order_validated = True

    def prompt_order(self) -> tuple[str, ...]:
        """
        Return the ordered prompt types for this agent.

        Override in subclasses if dynamic ordering is needed.
        Default returns the class-level REQUIRED_PROMPT_ORDER.

        Returns:
            Ordered tuple of prompt type constants
        """
        return self.REQUIRED_PROMPT_ORDER

    def builder_flags(self) -> dict[str, bool]:
        """
        Return builder configuration flags for this agent.

        Override in subclasses to customize builder behavior.
        Default: no debug instructions.

        Returns:
            Dict with builder flags (include_debug, etc.)
        """
        return {"include_debug": False}

    @property
    def requires_action_resolution(self) -> bool:
        """
        Whether this agent requires action_resolution in the LLM response.

        Override in subclasses to disable this requirement (e.g., God Mode, Character Creation).
        Default: True (Story Mode, Combat Mode, etc. require it for audit trails).
        """
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(mode={self.MODE}, required={len(self.REQUIRED_PROMPTS)}, optional={len(self.OPTIONAL_PROMPTS)})"


class FixedPromptAgent(BaseAgent):
    """
    Base class for agents with a fixed prompt set.

    Provides a default build_system_instructions() that uses build_for_agent(),
    eliminating the need for `del unused_params` patterns in subclasses.

    Subclasses only need to:
    - Define REQUIRED_PROMPT_ORDER (inherited from BaseAgent)
    - Override builder_flags() if they need debug instructions
    - Override finalize_with_world() if they need world content

    This simplifies agents that don't use selected_prompts, turn_number,
    or other dynamic parameters.
    """

    # Whether this agent should include world content in finalized instructions
    INCLUDE_WORLD_CONTENT: bool = False

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions using the fixed prompt set.

        This default implementation ignores dynamic parameters and builds
        instructions using the agent's REQUIRED_PROMPT_ORDER and builder_flags().

        Subclasses can override if they need dynamic behavior.
        """
        # Use build_for_agent for consistent instruction building
        parts = self._prompt_builder.build_for_agent(
            self, dice_roll_strategy=dice_roll_strategy, turn_number=turn_number
        )

        # Finalize with world content based on class setting
        del selected_prompts, use_default_world, include_continuation_reminder
        del llm_requested_sections, dice_roll_strategy
        # Note: turn_number passed to build_for_agent above
        return self._prompt_builder.finalize_instructions(
            parts, use_default_world=self.INCLUDE_WORLD_CONTENT
        )


class StoryModeAgent(BaseAgent):
    """
    Agent for Story Mode (Character Mode) interactions.

    This agent handles narrative storytelling, character actions,
    and standard gameplay. It uses the full set of narrative and
    mechanics prompts to generate immersive story content.

    Responsibilities:
    - Narrative generation with planning blocks
    - Character action handling
    - Game mechanics integration (combat, skill checks)
    - Entity tracking and state updates
    - Temporal consistency enforcement

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Game state instructions (data structure compliance)
    3. Debug instructions (dice rolls, state tracking)
    4. Character template (conditional - when narrative enabled)
    5. Narrative/Mechanics (based on campaign settings)
    6. D&D SRD reference
    7. Continuation reminders (planning blocks, temporal enforcement)
    8. Living world instruction (every turn, injected last after narrative/mechanics)
    9. World content (conditional)
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → dnd_srd
    # Note: Narrative/Mechanics are added dynamically in build_system_instruction_parts
    # Note: PROMPT_TYPE_LIVING_WORLD is excluded here; build_system_instruction_parts
    # appends it explicitly AFTER narrative/mechanics/continuation blocks so it lands last,
    # reducing prompt competition from the 3009-line game_state block. See rev-m36u.
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Planning block schema
        constants.PROMPT_TYPE_DND_SRD,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # Optional prompts - loaded based on campaign settings
    OPTIONAL_PROMPTS: frozenset[str] = frozenset(
        {
            constants.PROMPT_TYPE_NARRATIVE,
            constants.PROMPT_TYPE_MECHANICS,
            constants.PROMPT_TYPE_CHARACTER_TEMPLATE,
        }
    )

    MODE: str = constants.MODE_CHARACTER

    def _add_deferred_rewards_instruction(
        self, parts: list[str], turn_number: int
    ) -> None:
        """
        Add deferred rewards instruction for parallel injection every N scenes.

        PARALLEL INJECTION: The deferred rewards instruction runs IN PARALLEL with
        story mode (same LLM call) every N scenes (configured via
        constants.DEFERRED_REWARDS_SCENE_INTERVAL, default 10).

        This catches any missed XP/loot awards without double-counting by:
        1. Scanning recent scenes for qualifying rewards
        2. Cross-referencing encounter_history to prevent duplicates
        3. Verifying rewards haven't already been processed

        Only StoryModeAgent triggers parallel deferred rewards - explicit checks
        via DeferredRewardsAgent use a separate prompt set.

        Args:
            parts: List of instruction parts to append to
            turn_number: Current turn number (parallel injection on turn 10, 20, 30, etc.)
        """
        builder = self._prompt_builder
        if builder.should_include_deferred_rewards(turn_number):
            deferred_rewards_instruction = builder.build_deferred_rewards_instruction(
                turn_number,
                force_include=False,  # Respect interval check
            )
            if deferred_rewards_instruction:
                parts.append(deferred_rewards_instruction)
                logging_util.info(
                    f"🎁 DEFERRED_REWARDS_PARALLEL: Added instruction for turn {turn_number}"
                )

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions for story mode.

        Uses the full prompt hierarchy for immersive storytelling:
        - Core instructions (master directive, game state, debug)
        - Character template (if narrative is selected)
        - Selected prompts (narrative, mechanics)
        - System references (D&D SRD)
        - Continuation reminders (planning blocks, temporal enforcement)
        - Living world instruction (every turn, appended last)
        - World content (if enabled)

        Args:
            selected_prompts: User-selected prompt types
            use_default_world: Whether to include world content
            include_continuation_reminder: Whether to add planning block reminders
                                           (True for continue_story, False for initial)
            turn_number: Current turn number (used for living world advancement)
            llm_requested_sections: Sections the LLM requested via meta.needs_detailed_instructions
                                    from the previous turn (e.g., ["relationships", "reputation"])

        Returns:
            Complete system instruction string
        """
        parts = self.build_system_instruction_parts(
            selected_prompts=selected_prompts,
            include_continuation_reminder=include_continuation_reminder,
            turn_number=turn_number,
            llm_requested_sections=llm_requested_sections,
            dice_roll_strategy=dice_roll_strategy,
        )

        # Finalize with world content if requested
        return self._prompt_builder.finalize_instructions(parts, use_default_world)

    def build_system_instruction_parts(
        self,
        selected_prompts: list[str] | None = None,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> list[str]:
        """
        Build the ordered instruction parts for story mode before finalization.

        This helper returns the base instruction list so callers (like initial
        story generation) can insert additional blocks before world lore is
        appended via finalize_instructions.

        Args:
            selected_prompts: User-selected prompt types
            include_continuation_reminder: Whether to add planning block reminders
            turn_number: Current turn number (used for living world advancement)
            llm_requested_sections: Sections the LLM requested via meta.needs_detailed_instructions
                                    from the previous turn (e.g., ["relationships", "reputation"])

        Returns:
            List of ordered system instruction parts (without world content).
        """
        # Create a local copy to avoid mutating the caller's list
        effective_prompts = list(selected_prompts) if selected_prompts else []

        # StoryModeAgent ALWAYS requires Narrative instructions to produce valid story content.
        # This ensures the LLM knows how to write immersive prose even if the user
        # selected only "Mechanics" or nothing at all.
        if constants.PROMPT_TYPE_NARRATIVE not in effective_prompts:
            effective_prompts.append(constants.PROMPT_TYPE_NARRATIVE)
            logging_util.debug(
                "Added mandatory PROMPT_TYPE_NARRATIVE to StoryModeAgent"
            )

        builder = self._prompt_builder
        # Build core instructions (master directive, game state, debug).
        # Pass advances_time=False to suppress the global LW injection inside
        # build_from_order — we append LW explicitly at the end so it lands
        # AFTER narrative/mechanics/continuation blocks (prompt isolation goal).
        parts: list[str] = builder.build_from_order(
            self.REQUIRED_PROMPT_ORDER,
            include_debug=self.builder_flags().get("include_debug", False),
            dice_roll_strategy=dice_roll_strategy,
            turn_number=turn_number,
            advances_time=False,
        )

        # Add character-related instructions (conditional)
        builder.add_character_instructions(parts, effective_prompts)

        # Add selected prompt instructions (narrative, mechanics)
        # Pass LLM-requested sections to load detailed prompts dynamically
        builder.add_selected_prompt_instructions(
            parts,
            effective_prompts,
            llm_requested_sections=llm_requested_sections,
            dice_roll_strategy=dice_roll_strategy,
        )

        # Add system reference instructions (D&D SRD)
        # Note: SRD added here instead of order to maintain character/narrative focus

        # Add continuation-specific reminders for story continuation
        if include_continuation_reminder:
            parts.append(builder.build_continuation_reminder(dice_roll_strategy))

        # PARALLEL INJECTION: Add deferred rewards instruction every N scenes (default: 10)
        # This runs IN PARALLEL with story mode (same LLM call) to catch missed rewards
        # without requiring explicit user request. The LLM scans recent scenes and fills
        # rewards_box if any XP/loot was missed, while deduplicating to prevent double-counting.
        self._add_deferred_rewards_instruction(parts, turn_number)

        # Living world is appended LAST (after narrative/mechanics/continuation) so it
        # does not compete with the 3009-line game_state block. See rev-m36u.
        if self.advances_time and turn_number >= 1:
            living_world_instruction = builder.build_living_world_instruction(
                turn_number
            )
            if living_world_instruction:
                parts.append(living_world_instruction)

        return parts

    def builder_flags(self) -> dict[str, bool]:
        """Story mode includes debug instructions."""
        return {"include_debug": True}

    @classmethod
    def matches_input(
        cls, user_input: str, _game_state: GameState | None = None
    ) -> bool:
        """
        Story mode is the default - matches any non-god-mode input.

        Args:
            user_input: Raw user input text

        Returns:
            True if the input does NOT start with "GOD MODE:"
        """
        return not user_input.strip().upper().startswith("GOD MODE:")


class GodModeAgent(FixedPromptAgent):
    """
    Agent for God Mode (Administrative) interactions.

    This agent handles administrative commands for correcting mistakes,
    modifying campaign state, and making out-of-game changes. It does
    NOT advance the narrative - that's story mode's job.

    Responsibilities:
    - Administrative state modifications
    - Campaign corrections and fixes
    - Character stat adjustments
    - Inventory modifications
    - Timeline/location corrections
    - NPC relationship changes

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. God mode instruction (administrative behavior)
    3. Game state instructions (state structure reference)
    4. Planning protocol (planning block schema)
    5. D&D SRD (game rules knowledge)
    6. Mechanics (detailed game rules)
    7. (Optional) Faction management - when armies present
    8. (Optional) Faction minigame - when enabled
    9. (Dynamic) Divine/Sovereign system - based on campaign tier

    Note: No narrative instructions - god mode doesn't tell stories.
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → god_mode → game_state → planning_protocol → dnd_srd → mechanics
    # Note: Divine/Sovereign prompts loaded via campaign tier system in finalize_instructions()
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GOD_MODE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # Optional prompts - loaded conditionally based on game state
    OPTIONAL_PROMPTS: frozenset[str] = frozenset(
        {
            constants.PROMPT_TYPE_FACTION_MANAGEMENT,  # When player has armies (20+ units)
            constants.PROMPT_TYPE_FACTION_MINIGAME,  # When faction_minigame.enabled=true
        }
    )

    MODE: str = constants.MODE_GOD

    # Uses FixedPromptAgent.build_system_instructions() - no del patterns needed

    @property
    def advances_time(self) -> bool:
        """GodMode does NOT advance world time (administrative queries only).

        GodMode is for corrections/admin, not narrative progression. It should
        not trigger living_world events and advances by 1 microsecond for ordering.
        """
        return False

    def prompt_order(self) -> tuple[str, ...]:
        """
        Return ordered prompt types, conditionally including faction prompts.

        Faction prompts load based on game state:
        - FACTION_MANAGEMENT: When player has armies (total_strength >= 20)
        - FACTION_MINIGAME: When faction_minigame.enabled = true

        Returns:
            Ordered tuple of prompt type constants
        """
        prompts = list(self.REQUIRED_PROMPT_ORDER)

        # Check game state for faction systems
        if isinstance(self.game_state, dict):
            custom_state = self.game_state.get("custom_campaign_state", {})
            army_data = self.game_state.get("army_data", {})
        else:
            custom_state = getattr(self.game_state, "custom_campaign_state", {})
            army_data = getattr(self.game_state, "army_data", {})
            if not isinstance(custom_state, dict):
                custom_state = {}
            if not isinstance(army_data, dict):
                army_data = {}

        # Load faction management prompt if player has armies (20+ units)
        total_strength_raw = (
            army_data.get("total_strength", 0) if isinstance(army_data, dict) else 0
        )
        try:
            total_strength = int(total_strength_raw or 0)
        except (TypeError, ValueError):
            total_strength = 0

        if total_strength >= 20:
            prompts.append(constants.PROMPT_TYPE_FACTION_MANAGEMENT)

        # Load faction minigame prompt if enabled
        faction_minigame = (
            custom_state.get("faction_minigame", {})
            if isinstance(custom_state, dict)
            else {}
        )
        if isinstance(faction_minigame, dict) and faction_minigame.get(
            "enabled", False
        ):
            prompts.append(constants.PROMPT_TYPE_FACTION_MINIGAME)

        return tuple(prompts)

    @classmethod
    def matches_input(cls, user_input: str, mode: str | None = None) -> bool:
        """
        God mode is triggered by "GOD MODE:" prefix OR mode="god" parameter.

        Uses constants.is_god_mode() for centralized detection logic.

        Args:
            user_input: Raw user input text
            mode: Optional mode parameter from request (e.g., "god", "character")

        Returns:
            True if god mode should be activated (via prefix or mode param)
        """
        return constants.is_god_mode(user_input, mode)

    def preprocess_input(self, user_input: str) -> str:
        """
        Preprocess god mode input.

        Inserts a warning reminder that God Mode is for administrative
        changes only and should not advance the narrative. The warning
        is inserted AFTER the "GOD MODE:" prefix (if present) to preserve
        the prefix for system instruction pattern matching.

        Args:
            user_input: Raw user input (may or may not have "GOD MODE:" prefix)

        Returns:
            Input with warning inserted after GOD MODE prefix (or prepended if no prefix)
        """
        # Check if input starts with "GOD MODE:" prefix (case insensitive)
        trimmed_input = user_input.lstrip()
        input_upper = trimmed_input.upper()
        if input_upper.startswith(constants.GOD_MODE_PREFIX.upper()):
            # Find the prefix position in trimmed input (ensures it starts at column 0)
            prefix_end = trimmed_input.upper().find(":") + 1
            # Insert warning AFTER the prefix to preserve "GOD MODE:" pattern matching
            return (
                trimmed_input[:prefix_end]
                + " "
                + constants.GOD_MODE_WARNING_PREFIX.strip()
                + " "
                + trimmed_input[prefix_end:].lstrip()
            )
        # If no prefix (triggered via mode=god parameter), prepend warning
        return constants.GOD_MODE_WARNING_PREFIX + user_input

    @property
    def requires_action_resolution(self) -> bool:
        """God mode is administrative and does not require action resolution audit trails."""
        return False


class CharacterCreationAgent(BaseAgent):
    """
    Agent for Character Creation & Level-Up Mode.

    This agent handles character creation AND level-ups with focused prompts.
    TIME DOES NOT ADVANCE during this mode - it's a "pause menu" for character
    building. The story only resumes when the user explicitly confirms they're done.

    PRECEDENCE: Second highest (just below GodModeAgent).

    Trigger Conditions (matches_game_state returns True when):
    1. New campaign: character_creation_completed is False
    2. No character: player_character_data.name is empty
    3. Level-up pending: level_up_pending flag is True

    Responsibilities:
    - Guide character concept development (new characters)
    - Handle race/class/background selection
    - Manage ability score assignment
    - Develop personality and backstory
    - Process level-ups with full D&D 5e rules
    - Handle ASI/Feat selection, new spells, class features
    - Confirm completion before transitioning to story

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Game state instruction (canonical schema for equipment/spells/stats)
    3. Character creation instruction (creation + level-up flow)
    4. D&D SRD (mechanics reference for options)
    5. Mechanics (detailed D&D rules for level-up choices)

    Note: NO narrative or combat prompts - time is frozen during this mode.
    """

    # Minimal prompts for focused character creation and level-up
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        # Ensure character creation outputs stay aligned with /equipment, /spells, /stats UI buttons.
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_CHARACTER_CREATION,
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,  # Full D&D rules for creation and level-up
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts - keep it focused
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_CHARACTER_CREATION

    @property
    def advances_time(self) -> bool:
        """Character creation is a pause/menu flow and does not advance time."""
        return False

    @classmethod
    def validate_prompt_order(cls) -> list[str]:
        """
        Override validation to allow missing planning_protocol/world lore.
        Character creation uses a minimal prompt set but still includes game_state schemas.
        """
        errors = []
        if not cls.REQUIRED_PROMPT_ORDER:
            errors.append(f"{cls.__name__}: REQUIRED_PROMPT_ORDER is empty")
            return errors

        if cls.REQUIRED_PROMPT_ORDER[0] != constants.PROMPT_TYPE_MASTER_DIRECTIVE:
            errors.append(
                f"{cls.__name__}: First prompt must be {constants.PROMPT_TYPE_MASTER_DIRECTIVE!r}"
            )

        return errors

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions for character creation mode.

        Uses a focused prompt set for character building and level-up:
        - Master directive (authority)
        - Game state instruction (canonical schemas)
        - Character creation instruction (focused creation flow)
        - D&D SRD (mechanics reference)
        - Mechanics (detailed D&D rules for choices)

        No narrative, no combat, no world lore - keeps prompts focused while still
        including canonical game state schemas.

        Returns:
            Minimal system instruction string for character creation
        """
        # Parameters intentionally unused - character creation uses fixed minimal set
        del selected_prompts, use_default_world, include_continuation_reminder
        del llm_requested_sections

        builder = self._prompt_builder

        # Build character creation instructions (focused prompt set)
        parts: list[str] = builder.build_from_order(
            self.REQUIRED_PROMPT_ORDER,
            dice_roll_strategy=dice_roll_strategy,
            turn_number=turn_number,
            advances_time=self.advances_time,
        )

        # Living world instructions must fire on the first character-creation turn
        # for each unique player_turn. Time does not advance (advances_time=False),
        # so build_from_order skips LW. We append it explicitly — but only when
        # last_living_world_turn < turn_number to avoid duplicate LW injection on
        # back-and-forth clicks within the same character-creation session.
        _gs = builder.game_state
        if isinstance(_gs, dict):
            _last_lw_turn_raw = _gs.get("last_living_world_turn", 0)
        else:
            _last_lw_turn_raw = getattr(_gs, "last_living_world_turn", 0)
        try:
            _last_lw_turn = int(_last_lw_turn_raw or 0)
        except (TypeError, ValueError):
            _last_lw_turn = 0
        if turn_number >= 1 and turn_number > _last_lw_turn:
            living_world_instruction = builder.build_living_world_instruction(
                turn_number
            )
            if living_world_instruction:
                parts.append(living_world_instruction)

        # CRITICAL: Add companion instruction EARLY (right after master directive) if companions exist
        # This ensures the LLM sees it BEFORE character creation instructions that might conflict
        # Security: Insert AFTER master directive (position 1) to maintain prompt hierarchy
        companion_instruction = builder.build_companion_instruction()
        if companion_instruction and "ACTIVE COMPANIONS" in companion_instruction:
            # Insert at position 1 (AFTER master directive) to maintain security hierarchy
            # finalize_instructions() will insert identity/directives at position 1-2,
            # so companion instruction will be at position 1, right after master directive
            parts.insert(1, companion_instruction)
            logging_util.info(
                "🎭 CharacterCreationAgent: Added companion instruction after master directive (position 1) for existing companions"
            )

        # Finalize WITHOUT world lore (character creation doesn't need it)
        # Note: finalize_instructions() will insert identity/directives after master directive,
        # pushing companion instruction to position 2 (after identity) or keeping it at 1
        del dice_roll_strategy
        return builder.finalize_instructions(parts, use_default_world=False)

    @classmethod
    def matches_game_state(  # noqa: PLR0912, PLR0915
        cls, game_state: GameState | None
    ) -> bool:
        """
        Check if character creation or level-up mode should be active.

        This mode is active when:
        1. game_state exists
        2. AND one of these conditions:
           a) character_creation_completed is False (new character)
           b) Character doesn't have a name/class yet
           c) level_up_pending flag is True (level-up in progress)

        Args:
            game_state: Current GameState object

        Returns:
            True if character creation or level-up is in progress
        """
        if game_state is None:
            logging_util.debug("🎭 CHARACTER_CREATION_CHECK: game_state is None")
            return False

        # Exclude faction mode - FactionManagementAgent should handle faction actions
        # even during level-up to ensure faction_header is generated
        # Use centralized utility for consistent extraction and validation
        if is_faction_minigame_enabled(game_state):
            logging_util.debug(
                "🎭 CHARACTER_CREATION_CHECK: faction_minigame.enabled=True, "
                "deferring to FactionManagementAgent"
            )
            return False

        # Get custom_campaign_state safely
        custom_state = {}
        if hasattr(game_state, "custom_campaign_state"):
            custom_state = game_state.custom_campaign_state or {}
        elif isinstance(game_state, dict):
            custom_state = game_state.get("custom_campaign_state", {}) or {}

        if not isinstance(custom_state, dict):
            custom_state = {}

        rewards_pending: dict[str, Any] = {}
        if hasattr(game_state, "rewards_pending"):
            rewards_value = game_state.rewards_pending
            if isinstance(rewards_value, dict):
                rewards_pending = rewards_value
        elif isinstance(game_state, dict):
            rewards_value = game_state.get("rewards_pending", {})
            if isinstance(rewards_value, dict):
                rewards_pending = rewards_value

        player_data: dict[str, Any] = {}
        if hasattr(game_state, "player_character_data"):
            player_value = game_state.player_character_data
            if isinstance(player_value, dict):
                player_data = player_value
        elif isinstance(game_state, dict):
            player_value = game_state.get("player_character_data", {})
            if isinstance(player_value, dict):
                player_data = player_value

        # Check for level-up pending (using correct rewards_pending location)
        level_up_pending = False

        # Check explicit flag in custom_state (for backward compatibility/mocks)
        if custom_state.get("level_up_pending", False):
            level_up_pending = True

        # Also check standard rewards_pending location (always, not just as fallback).
        # A legitimate new level-up via rewards_pending should be honored even if
        # there's a stale level_up_pending flag in custom_state.
        if not level_up_pending:
            # Check for fresh level-up signal from rewards_pending
            level_up_from_rewards = isinstance(
                rewards_pending, dict
            ) and rewards_pending.get("level_up_available", False)
            if level_up_from_rewards:
                level_up_pending = True

        # CRITICAL: Apply same stale flag guards as level-up routing (agents.py:2864-2876)
        # to ensure consistent detection across character creation check and level-up modal lock.
        # WITHOUT these guards, routing and injection disagree on modal active state.
        #
        # Explicit False flags ALWAYS take precedence over stale rewards_pending data.
        # This ensures consistency with get_agent_for_input and _inject_modal_finish_choice_if_needed.
        level_up_in_progress = custom_state.get("level_up_in_progress")
        if level_up_in_progress is False:
            logging_util.info(
                "🔓 CHARACTER_CREATION_CHECK: level_up_in_progress=False explicitly set, "
                "not activating level-up (stale flag guard)"
            )
            level_up_pending = False

        level_up_pending_flag = custom_state.get("level_up_pending")
        if level_up_pending_flag is False and not bool(level_up_in_progress):
            logging_util.info(
                "🔓 CHARACTER_CREATION_CHECK: level_up_pending=False explicitly set, "
                "not activating level-up (stale flag guard)"
            )
            level_up_pending = False

        if level_up_pending and _is_stale_level_up_pending(
            custom_state, rewards_pending, player_data
        ):
            logging_util.info(
                "🔓 CHARACTER_CREATION_CHECK: Ignoring stale level_up_pending "
                "(XP below next-level threshold and no rewards_pending signal)"
            )
            level_up_pending = False

        if level_up_pending:
            logging_util.info(
                "🎭 CHARACTER_CREATION_CHECK: level_up_pending/available=True, entering level-up mode"
            )
            return True

        if custom_state.get("character_creation_completed", False):
            logging_util.debug(
                "🎭 CHARACTER_CREATION_CHECK: character_creation_completed=True"
            )
            return False

        # Check if character has a name (indicates creation may be done)
        pc_data = None
        if hasattr(game_state, "player_character_data"):
            pc_data = game_state.player_character_data
        elif isinstance(game_state, dict):
            pc_data = game_state.get("player_character_data", {})

        if pc_data and isinstance(pc_data, dict):
            # If character has a name AND class, likely creation is done
            # (unless explicitly marked as in-progress)
            char_name = pc_data.get("name", "")
            char_class = pc_data.get("class", "") or pc_data.get("character_class", "")

            if char_name and char_class:
                # Character has name and class - check if explicitly in creation mode
                in_creation_mode = custom_state.get(
                    "character_creation_in_progress", False
                )

                if not in_creation_mode:
                    # Check nested structure
                    char_creation_data = custom_state.get("character_creation")
                    if isinstance(char_creation_data, dict):
                        in_creation_mode = char_creation_data.get("in_progress", False)

                if not in_creation_mode:
                    logging_util.debug(
                        f"🎭 CHARACTER_CREATION_CHECK: Character has name='{char_name}' "
                        f"and class='{char_class}', creation assumed complete"
                    )
                    return False

        # Default: if campaign is new and character isn't complete, we're in creation
        logging_util.info("🎭 CHARACTER_CREATION_CHECK: Character creation mode ACTIVE")
        return True

    @classmethod
    def matches_input(cls, user_input: str) -> bool:
        """
        Check if user input indicates character creation completion.

        Returns True if the input suggests they want to START the story,
        which means we should transition OUT of character creation.

        Note: This returns True to MATCH when user is DONE with creation,
        which the get_agent_for_input logic uses to transition to StoryMode.

        Args:
            user_input: Raw user input text

        Returns:
            True if user indicates they're done with character creation
        """
        lower = user_input.lower().strip()
        # Normalize curly apostrophes to straight apostrophes
        lower = lower.replace("\u2019", "'")

        logging_util.debug(f"Matches Input Check: '{lower}'")

        if re.search(r"\bnot\s+(?:yet\s+)?(?:done|finished|ready)\b", lower):
            logging_util.debug("Matches Input: False (Negative match)")
            return False
        # Catch "don't start" and "don't begin"
        if re.search(r"\bdo(?:n't| not|nt)\s+(?:start|begin)\b", lower):
            logging_util.debug("Matches Input: False (Negative match)")
            return False

        # Check for valid completion patterns first (before exclusions)
        # These patterns indicate clear intent to complete character creation
        completion_patterns = [
            r"\bstart\s+(?:the\s+)?(?:story|adventure)\b",
            r"\bbegin\s+(?:the\s+)?(?:story|adventure)\b",
            r"\bstart\s+(?:the\s+)?game\b",
            r"\bbegin\s+(?:the\s+)?game\b",
        ]
        # If input contains a valid completion pattern, allow it even if it also contains "ready to start"
        has_completion_pattern = any(re.search(p, lower) for p in completion_patterns)

        # Explicitly exclude ambiguous "ready to start" ONLY if it's not part of a valid completion phrase
        # Examples: "I'm ready to start" (ambiguous) vs "I'm ready to start the adventure" (clear intent)
        if not has_completion_pattern and "ready to start" in lower:
            logging_util.debug(
                "Matches Input: False (Ambiguous 'ready to start' without completion phrase)"
            )
            return False

        patterns = [
            r"\bi'?m\s+done\b",
            r"\bi'?m\s+finished\b",
            r"\bi\s+am\s+done\b",
            r"\bi\s+am\s+finished\b",
            r"\bready\s+to\s+play\b",
            r"\bthat'?s\s+everything\b",
            r"\bcharacter\s+(?:is\s+)?complete\b",
            r"\b(?:done|finished)\s+(?:creating|leveling)\b",
            r"\blevel-?up\s+complete\b",
            r"\blet'?s\s+play\b",
            r"\b(?:back\s+to|continue)\s+adventure\b",
            # Additional robustness for natural language
            r"\blooks\s+perfect\b",
            r"\bperfect!?\s+(?:let'?s|i'?m)\b",
        ] + completion_patterns  # Include completion patterns in main pattern list

        result = any(re.search(pattern, lower) for pattern in patterns)
        if result:
            logging_util.debug("Matches Input: True (Matched pattern)")
        return result

    @property
    def requires_action_resolution(self) -> bool:
        """Character creation is a setup phase and does not require action resolution audit trails."""
        return False


class LevelUpAgent(BaseAgent):
    """
    Agent for dedicated D&D 5e level-up mode.

    This modal agent handles level-up decisions only. TIME DOES NOT ADVANCE
    while level-up is active.
    """

    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        # Ensure level-up outputs stay aligned with /equipment, /spells, /stats UI buttons.
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_LEVEL_UP,
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_LEVEL_UP

    @property
    def advances_time(self) -> bool:
        """Level-up is a pause/menu flow and does not advance time."""
        return False

    @classmethod
    def validate_prompt_order(cls) -> list[str]:
        """Allow minimal prompt order for dedicated level-up flow."""
        errors = []
        if not cls.REQUIRED_PROMPT_ORDER:
            errors.append(f"{cls.__name__}: REQUIRED_PROMPT_ORDER is empty")
            return errors

        if cls.REQUIRED_PROMPT_ORDER[0] != constants.PROMPT_TYPE_MASTER_DIRECTIVE:
            errors.append(
                f"{cls.__name__}: First prompt must be {constants.PROMPT_TYPE_MASTER_DIRECTIVE!r}"
            )

        return errors

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """Build focused system instructions for D&D 5e level-up only."""
        del selected_prompts, use_default_world, include_continuation_reminder
        del turn_number, llm_requested_sections

        builder = self._prompt_builder
        parts: list[str] = builder.build_from_order(
            self.REQUIRED_PROMPT_ORDER,
            dice_roll_strategy=dice_roll_strategy,
            advances_time=self.advances_time,
        )

        del dice_roll_strategy
        return builder.finalize_instructions(parts, use_default_world=False)

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:  # noqa: PLR0912
        """Level-up mode is active if level_up_pending is true in campaign state."""
        if game_state is None:
            return False

        # Resilient state extraction (consistent with get_agent_for_input)
        custom_state: dict[str, Any] = {}
        rewards_pending: dict[str, Any] = {}

        if hasattr(game_state, "custom_campaign_state"):
            val = game_state.custom_campaign_state
            if isinstance(val, dict):
                custom_state = val
        elif isinstance(game_state, dict):
            val = game_state.get("custom_campaign_state", {})
            if isinstance(val, dict):
                custom_state = val

        if hasattr(game_state, "rewards_pending"):
            val = game_state.rewards_pending
            if isinstance(val, dict):
                rewards_pending = val
        elif isinstance(game_state, dict):
            val = game_state.get("rewards_pending", {})
            if isinstance(val, dict):
                rewards_pending = val

        player_data: dict[str, Any] = {}
        if hasattr(game_state, "player_character_data"):
            val = game_state.player_character_data
            if isinstance(val, dict):
                player_data = val
        elif isinstance(game_state, dict):
            val = game_state.get("player_character_data", {})
            if isinstance(val, dict):
                player_data = val

        # Check for completion/cancellation override (prevents modal trap)
        if custom_state.get("level_up_complete", False) or custom_state.get(
            "level_up_cancelled", False
        ):
            return False

        # Respect explicit stale guards. If these fields are explicitly false,
        # do not reactivate level-up from leftover pending/rewards flags.
        level_up_in_progress = custom_state.get("level_up_in_progress")
        if level_up_in_progress is False:
            return False

        level_up_pending = custom_state.get("level_up_pending")
        if level_up_pending is False and not bool(level_up_in_progress):
            return False

        if _is_stale_level_up_pending(custom_state, rewards_pending, player_data):
            return False

        # Check all level-up signals (consistent with get_agent_for_input)
        return (
            custom_state.get("level_up_in_progress", False)
            or custom_state.get("level_up_pending", False)
            or rewards_pending.get("level_up_available", False)
        )

    @classmethod
    def matches_input(cls, _user_input: str) -> bool:
        """Level-up mode is state-driven; input text does not force this agent."""
        return False

    @property
    def requires_action_resolution(self) -> bool:
        """Level-up is a setup/management phase without action resolution trails."""
        return False


class PlanningAgent(FixedPromptAgent):
    """
    Agent for Think Mode (Strategic Planning) interactions.

    This agent handles strategic planning and tactical analysis where the
    character pauses to think WITHOUT advancing the narrative. Time only
    advances by 1 microsecond to maintain temporal ordering.

    PlanningAgent sits at priority 2 in agent selection: it is checked
    immediately after GodModeAgent and before all other specialized
    agents (Info, Combat, Rewards) and StoryModeAgent. When a user
    explicitly enters Think Mode, this agent handles the input ahead of
    all non-god interactions.

    Responsibilities:
    - Deep strategic analysis with multiple options
    - Pros/cons evaluation for each approach
    - Confidence assessment for tactical choices
    - Internal monologue generation (character's thoughts)
    - Microsecond-only time advancement (no narrative time)

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Think mode instruction (planning behavior)
    3. Game state instructions (state structure reference)
    4. D&D SRD (game rules knowledge)

    Note: No narrative advancement - world is frozen while character thinks.
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → think → game_state → planning_protocol → dnd_srd
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_THINK,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Planning block schema (canonical)
        constants.PROMPT_TYPE_DND_SRD,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts for think mode - it's focused on planning
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_THINK

    # Uses FixedPromptAgent.build_system_instructions() - no del patterns needed

    @property
    def advances_time(self) -> bool:
        """PlanningAgent does NOT advance world time (strategic planning only).

        Think mode is for planning without time progression. It should not trigger
        living_world events and advances by 1 microsecond for ordering.
        """
        return False

    @classmethod
    def matches_input(cls, user_input: str, mode: str | None = None) -> bool:
        """
        Think mode is triggered by "THINK:" prefix or explicit mode selection.

        Uses constants.is_think_mode() for centralized detection logic.
        Note: matches_input() is called during agent selection, which happens
        AFTER the frontend has normalized the input (adding THINK: prefix when
        mode == "think"), so the mode parameter is typically not needed here.

        Args:
            user_input: Raw user input text
            mode: Optional mode parameter from request (rarely needed since
                  frontend normalizes input before agent selection)

        Returns:
            True if think mode is detected via prefix or mode
        """
        return constants.is_think_mode(user_input, mode)

    def preprocess_input(self, user_input: str) -> str:
        """
        Preprocess think mode input.

        Preserves the "THINK:" prefix for the LLM to recognize
        the planning command context.

        Args:
            user_input: Raw user input with "THINK:" prefix

        Returns:
            Input unchanged (LLM needs to see the THINK: prefix)
        """
        return user_input

    @property
    def requires_action_resolution(self) -> bool:
        """Think Mode is for planning and does not require action resolution audit trails."""
        return False


# --- INFO QUERY CLASSIFICATION ---
# Conservative patterns: Only route to InfoAgent for CLEAR info-only queries

INFO_QUERY_PATTERNS = [
    "show me my",  # "show me my equipment"
    "what do i have",  # "what do I have equipped"
    "list my",  # "list my items"
    "check my",  # "check my inventory"
    "what's in my",  # "what's in my backpack"
    "what am i wearing",
    "what am i carrying",
    "my equipment",  # "show my equipment"
    "my inventory",  # "check my inventory"
    "my gear",  # "list my gear"
    "my items",  # "show my items"
    "my weapons",  # "what are my weapons"
    "what weapons",  # "what weapons do I have"
    "do i have",  # "what items do I have" - broader pattern
]

# If ANY action verb present, stay in StoryMode (conservative)
STORY_ACTION_VERBS = [
    "find",
    "buy",
    "sell",
    "search",
    "look for",
    "upgrade",
    "equip",
    "unequip",
    "drop",
    "pick up",
    "use",
    "trade",
    "get",
    "acquire",
    "steal",
    "loot",
    "craft",
    "repair",
]


class InfoAgent(FixedPromptAgent):
    """
    Agent for Information Queries (Equipment, Inventory, Stats).

    This agent handles pure information queries with TRIMMED system prompts
    to improve LLM compliance with exact item naming. It does NOT advance
    the narrative - use StoryModeAgent for any action-based queries.

    Responsibilities:
    - Equipment listing with exact item names
    - Inventory display (backpack, weapons, equipped items)
    - Character stats display
    - Pure information retrieval (no story advancement)

    System Prompt Hierarchy (TRIMMED for focus):
    1. Master directive (establishes AI authority)
    2. Game state instructions (contains Equipment Query Protocol)
    3. Planning protocol (canonical planning_block schema)

    Note: NO narrative, mechanics, or character_template prompts.
    This reduces prompt from ~2000 lines to ~1100 lines, improving
    LLM focus on the Equipment Query Protocol.
    """

    # Required prompts - ordered tuple (TRIMMED for focus)
    # Order: master → game_state → planning_protocol
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,  # Contains Equipment Query Protocol
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts - keep it focused
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_INFO

    # Info mode doesn't need world lore - keep focused on equipment/inventory
    INCLUDE_WORLD_CONTENT: bool = False

    @property
    def advances_time(self) -> bool:
        """InfoAgent does NOT advance world time (pure information queries).

        Info queries retrieve data without time progression. They should not
        trigger living_world events and advance by 1 microsecond for ordering.
        """
        return False

    @property
    def requires_action_resolution(self) -> bool:
        """Info queries are for data retrieval and do not require action resolution audit trails."""
        return False

    @classmethod
    def matches_input(cls, user_input: str) -> bool:
        """
        Conservative detection: Only route to InfoAgent for CLEAR info-only queries.

        Route to InfoAgent only when:
        1. Input matches an info query pattern (show/list/check)
        2. No action verbs present (find/buy/sell/search)

        If uncertain, returns False (defaults to StoryModeAgent).

        Args:
            user_input: Raw user input text

        Returns:
            True only for clear info-only queries
        """
        lower = user_input.lower()

        # If ANY action verb present, it's a story query
        if any(verb in lower for verb in STORY_ACTION_VERBS):
            return False

        # Only route to InfoAgent for clear info patterns
        return any(pattern in lower for pattern in INFO_QUERY_PATTERNS)


class CombatAgent(BaseAgent):
    """
    Agent for Combat Mode (Active Combat Encounters).

    This agent handles tactical combat encounters with focused prompts for
    dice rolls, initiative tracking, combat rewards, and boss equipment.
    It is automatically selected when game_state.combat_state.in_combat is True.

    Responsibilities:
    - Initiative and turn order management
    - Combat dice roll enforcement (attacks, saves, damage)
    - Combat state tracking (HP, conditions, position)
    - Combat end rewards (XP, loot, resources)
    - Boss/Special NPC equipment enforcement
    - Combat session tracking with unique IDs

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Game state instructions (combat_state schema - loaded before combat rules)
    3. Combat system instruction (tactical combat rules)
    4. Narrative instruction (DM Note protocol, cinematic style)
    5. D&D SRD (combat rules reference)
    6. Mechanics (detailed combat mechanics)
    7. Debug instructions (combat logging)

    Note: Combat mode automatically transitions back to story mode when combat ends.
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → combat → narrative → dnd_srd → mechanics → living_world
    # Include PROMPT_TYPE_LIVING_WORLD for background events during combat/social challenges.
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_COMBAT,
        constants.PROMPT_TYPE_NARRATIVE,  # DM Note protocol and cinematic style
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,  # Detailed combat mechanics
        constants.PROMPT_TYPE_LIVING_WORLD,  # Background events
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts for combat mode - it's focused on tactical combat
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_COMBAT

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions for combat mode.

        Uses build_from_order() with REQUIRED_PROMPT_ORDER to enforce invariants,
        then finalizes with optional world content for combat in specific locations.

        Note: Living world is included via REQUIRED_PROMPT_ORDER for combat/social
        turns that route through CombatAgent.

        Args:
            selected_prompts: Unused - combat uses fixed prompt set
            use_default_world: Whether to include world content
            include_continuation_reminder: Unused - combat uses fixed prompt set
            turn_number: Current turn number (used for living world scheduling)
            llm_requested_sections: Unused - combat uses fixed prompt set

        Returns:
            Complete system instruction string for combat encounters
        """
        # Parameters intentionally unused - combat mode uses fixed prompt set
        del selected_prompts, include_continuation_reminder
        del llm_requested_sections

        builder = self._prompt_builder

        # Use build_from_order() with REQUIRED_PROMPT_ORDER to enforce invariants
        # This ensures prompts are loaded in the validated order with debug included
        parts: list[str] = builder.build_from_order(
            self.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            dice_roll_strategy=dice_roll_strategy,
            turn_number=turn_number,
            advances_time=self.advances_time,
        )

        # Finalize with optional world instructions (for combat in specific locations)
        del dice_roll_strategy
        return builder.finalize_instructions(parts, use_default_world=use_default_world)

    def builder_flags(self) -> dict[str, bool]:
        """Combat mode includes debug instructions for combat logging."""
        return {"include_debug": True}

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:
        """
        Check if combat mode should be active based on game state.

        Combat mode is triggered when:
        - game_state is not None
        - game_state.is_in_combat() returns True

        Uses standardized GameState.is_in_combat() helper for consistent access.

        Args:
            game_state: Current GameState object

        Returns:
            True if combat is active and CombatAgent should be used
        """
        if game_state is None:
            logging_util.debug("⚔️ COMBAT_CHECK: game_state is None, not in combat")
            return False

        # Use standardized helper method for consistent combat state access
        in_combat = game_state.is_in_combat()
        combat_state = game_state.get_combat_state()

        logging_util.info(
            f"⚔️ COMBAT_CHECK: in_combat={in_combat}, "
            f"combat_state_keys={list(combat_state.keys())}"
        )
        return in_combat

    @classmethod
    def matches_input(cls, _user_input: str) -> bool:
        """
        Combat mode is NOT triggered by input - only by game state.

        Args:
            _user_input: Raw user input text (unused)

        Returns:
            Always False - use matches_game_state instead
        """
        return False


class RewardsAgent(FixedPromptAgent):
    """
    Agent for Rewards Mode (XP, Loot, Level-Up Processing).

    This agent handles ALL reward processing from any source:
    - Combat victories (triggered after combat ends)
    - Non-combat encounters (heists, social victories, stealth successes)
    - Quest completions
    - Milestone achievements

    Responsibilities:
    - XP calculation and awarding from any source
    - Loot distribution and inventory updates
    - Level-up detection and processing
    - Encounter history archival
    - Resource restoration (if applicable)

    Trigger Conditions (matches_game_state returns True when):
    1. combat_phase == "ended" AND combat_summary exists
    2. encounter_state.encounter_completed == true
    3. rewards_pending exists in game_state

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Game state instructions (state structure reference)
    3. Rewards system instruction (XP/loot/level-up rules)
    4. D&D SRD (game rules for XP thresholds)
    5. Mechanics (detailed level-up rules)

    Note: After rewards are processed, this agent transitions back to story mode.
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → rewards → dnd_srd → mechanics
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_REWARDS,
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts for rewards mode - focused on reward processing
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_REWARDS

    # Rewards mode doesn't need world lore - focused on reward processing
    INCLUDE_WORLD_CONTENT: bool = False

    @property
    def advances_time(self) -> bool:
        """Rewards processing is administrative and does not advance world time."""
        return False

    @property
    def requires_action_resolution(self) -> bool:
        """Rewards mode is administrative and does not require action resolution audit trails."""
        return False

    def builder_flags(self) -> dict[str, bool]:
        """Rewards mode includes debug instructions for reward processing logging."""
        return {"include_debug": True}

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:
        """
        Check if rewards mode should be active based on game state.

        Rewards mode is triggered when ANY of these conditions are true:
        1. combat_phase == "ended" AND combat_summary exists
        2. encounter_state.encounter_completed == true AND encounter_summary exists
        3. rewards_pending exists in game_state

        Args:
            game_state: Current GameState object

        Returns:
            True if rewards are pending and RewardsAgent should be used
        """
        if game_state is None:
            logging_util.debug(
                "🏆 REWARDS_CHECK: game_state is None, no rewards pending"
            )
            return False

        # Check 1: Combat just ended with summary (needs reward processing)
        combat_state = game_state.get_combat_state()
        # Use centralized constant for combat finished phases
        if (
            combat_state.get("combat_phase") in constants.COMBAT_FINISHED_PHASES
            and combat_state.get("combat_summary")
            and not combat_state.get("rewards_processed", False)
        ):
            logging_util.info(
                "🏆 REWARDS_CHECK: Combat ended with summary, rewards pending"
            )
            return True

        # Check 2: Encounter completed (non-combat rewards)
        encounter_state = game_state.get_encounter_state()
        encounter_completed = encounter_state.get("encounter_completed", False)
        encounter_summary = encounter_state.get("encounter_summary")
        encounter_processed = encounter_state.get("rewards_processed", False)

        if encounter_completed:
            if not isinstance(encounter_summary, dict):
                logging_util.debug(
                    "🏆 REWARDS_CHECK: Encounter completed but encounter_summary missing/invalid"
                )
            elif encounter_summary.get("xp_awarded") is None:
                logging_util.debug(
                    "🏆 REWARDS_CHECK: Encounter completed but encounter_summary missing xp_awarded"
                )
            elif not encounter_processed:
                logging_util.info(
                    "🏆 REWARDS_CHECK: Encounter completed, rewards pending"
                )
                return True

        # Check 3: Explicit rewards_pending flag
        rewards_pending = game_state.get_rewards_pending()
        if rewards_pending and not rewards_pending.get("processed", False):
            logging_util.info(
                f"🏆 REWARDS_CHECK: Explicit rewards_pending={rewards_pending}"
            )
            return True

        logging_util.debug("🏆 REWARDS_CHECK: No rewards pending")
        return False

    @classmethod
    def matches_input(cls, _user_input: str) -> bool:
        """
        Rewards mode is NOT triggered by input - only by game state.

        Args:
            _user_input: Raw user input text (unused)

        Returns:
            Always False - use matches_game_state instead
        """
        return False


class DeferredRewardsAgent(RewardsAgent):
    """
    Agent for Deferred Rewards Processing (Parallel to Story Mode).

    This agent inherits from RewardsAgent but runs as part of the story mode
    LLM call every N scenes (default: 10). It scans for missed rewards and
    fills the rewards_box without double-counting.

    Key Differences from RewardsAgent:
    - Runs IN PARALLEL with story mode (same LLM call)
    - Triggered by scene count, not game state flags
    - Focuses on catching MISSED rewards, not processing pending ones
    - Must verify rewards haven't already been processed before awarding

    Usage:
    - Primary mechanism: Deferred rewards instruction added to StoryModeAgent
    - This class provides the specialized prompt set for explicit invocation
    - Can be used standalone if explicit deferred rewards check is needed

    Deduplication Protocol:
    1. Check combat_state.rewards_processed flag
    2. Check encounter_state.rewards_processed flag
    3. Cross-reference encounter_history for duplicates
    4. Compare expected XP vs actual to detect already-applied rewards

    System Prompt Hierarchy (inherits from RewardsAgent):
    1. Master directive (establishes AI authority)
    2. Game state instructions (state structure reference)
    3. Planning protocol (canonical planning block schema)
    4. Rewards (base rewards processing rules)
    5. Deferred rewards instruction (catch-up rewards rules)
    6. D&D SRD (game rules for XP thresholds)
    7. Mechanics (detailed level-up rules)
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → rewards → deferred_rewards → dnd_srd → mechanics
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_REWARDS,
        constants.PROMPT_TYPE_DEFERRED_REWARDS,
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # Mode identifier for deferred rewards
    MODE: str = constants.MODE_REWARDS  # Uses same mode as rewards

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions for deferred rewards mode.

        Includes deferred rewards instruction on top of base rewards prompts.
        The deferred rewards instruction adds special rules for:
        - Scanning recent scenes for missed rewards
        - Deduplication to prevent double-counting
        - Sets source field to "deferred" in rewards_box for catch-up awards

        Args:
            selected_prompts: List of prompt types (unused - fixed prompt set)
            use_default_world: Whether to use default world (unused)
            include_continuation_reminder: Include continuation reminder (unused)
            turn_number: Current turn number for context
            llm_requested_sections: LLM-requested sections (unused)
            dice_roll_strategy: Dice roll strategy (unused - deferred rewards doesn't roll dice)

        Returns:
            Complete system instruction string for deferred rewards processing
        """
        del (
            selected_prompts,
            include_continuation_reminder,
            use_default_world,
            llm_requested_sections,
        )
        del dice_roll_strategy  # Deferred rewards doesn't need dice instructions

        builder = self._prompt_builder

        # Use build_from_order() with REQUIRED_PROMPT_ORDER to enforce invariants
        # build_from_order handles deferred rewards context automatically
        parts: list[str] = builder.build_from_order(
            self.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            turn_number=turn_number,
            advances_time=self.advances_time,
        )

        # Finalize without world instructions
        return builder.finalize_instructions(parts, use_default_world=False)

    @classmethod
    def should_run_deferred_check(cls, turn_number: int) -> bool:
        """
        Check if deferred rewards should run based on scene count.

        Args:
            turn_number: Current scene/turn number

        Returns:
            True if deferred rewards check should run (every N scenes)
        """
        # Delegate to PromptBuilder to maintain a single source of truth
        return PromptBuilder(None).should_include_deferred_rewards(turn_number)


class DialogAgent(FixedPromptAgent):
    """
    Agent for Dialog/Conversation Mode.

    This agent handles conversation-heavy scenes where players engage in
    extended NPC interactions. It focuses on character personalities, dialog
    flow, and narrative immersion while reducing mechanical overhead.

    Responsibilities:
    - NPC dialog with distinct character voices
    - Personality expression via speech patterns
    - Social skill integration (persuasion, deception, etc.)
    - Relationship dynamics and trust building
    - Natural conversation flow and turn-taking

    Trigger Conditions:
    1. mode="dialog" parameter passed explicitly
    2. Semantic intent classification indicates dialog
    3. Active dialog context in game state (dialog continuity)
    4. NOT during active combat (CombatAgent takes priority)

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Game state instructions (state structure reference)
    3. Planning protocol (canonical planning block schema)
    4. Dialog system instruction (conversation excellence)
    5. Narrative lite instruction (action resolution + guardrails)
    6. Character template (NPC personality templates)
    7. Relationship instruction (NPC relationship dynamics)
    8. Living world instruction (background world progression)

    Note: Excludes mechanics, combat, and D&D SRD to reduce token overhead
    and focus the LLM on dialog quality while preserving living world events.
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → dialog → narrative_lite → character_template → relationship → living_world
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_DIALOG,
        constants.PROMPT_TYPE_NARRATIVE_LITE,  # Lightweight mechanics for dialog (9KB vs 76KB)
        constants.PROMPT_TYPE_CHARACTER_TEMPLATE,
        constants.PROMPT_TYPE_RELATIONSHIP,
        constants.PROMPT_TYPE_LIVING_WORLD,  # Restored for background events
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts - focused dialog mode
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_DIALOG

    # Dialog mode doesn't need world lore - focused on character interactions
    INCLUDE_WORLD_CONTENT: bool = False

    def builder_flags(self) -> dict[str, bool]:
        """Dialog mode does not include debug instructions (focused on narrative)."""
        return {"include_debug": False}

    @classmethod
    def matches_input(cls, _user_input: str, _mode: str | None = None) -> bool:
        """
        DialogAgent cannot be triggered through input patterns or mode forcing.

        Dialog mode is ONLY triggered by:
        1. Semantic intent classifier detecting dialog-focused input
        2. Game state continuity (active dialog context from previous turn)

        Args:
            _user_input: Raw user input text
            mode: Optional mode parameter from request (ignored for DialogAgent)

        Returns:
            Always False - DialogAgent must be selected by semantic classifier or game state
        """
        # DialogAgent is an INTERNAL mode - users cannot force it
        # Selection happens only through:
        # - Priority 7: Semantic intent classification (MODE_DIALOG from classifier)
        # - Priority 5c: Game state continuity (matches_game_state)
        return False

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:
        """
        Check if game state indicates dialog context.

        Dialog continuity is handled via dialog_context, recent dialog actions,
        or dialog-heavy planning blocks from prior turns.
        This method maintains dialog flow across turns by detecting active
        dialog scenes, recent dialog actions, or dialog-heavy planning blocks.

        Dialog mode does NOT trigger during combat - CombatAgent takes priority.

        Args:
            game_state: Current GameState object

        Returns:
            True if state indicates active dialog
        """
        if game_state is None:
            return False

        # Don't trigger during active combat
        if game_state.is_in_combat():
            return False

        # 1. Check for active dialog context flag
        # (This allows explicit state-based persistence of dialog mode)
        dialog_context = getattr(game_state, "dialog_context", None)
        if isinstance(dialog_context, dict) and dialog_context.get("active", False):
            return True

        # 2. Check if the last action was dialog-related
        # 2. Check if the last action was dialog-related
        last_action = getattr(game_state, "last_action_type", None)
        return last_action in (
            "talk",
            "dialog",
            "conversation",
            "persuasion",
            "deception",
            "intimidation",
            "performance",
            "insight",
        )


class HeavyDialogAgent(DialogAgent):
    """
    Escalated dialog agent for high-stakes conversations.

    Use this for major relationship scenes, companion discussions, and
    conversations where richer mechanics/world context improves output quality.
    """

    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_DIALOG,
        constants.PROMPT_TYPE_NARRATIVE,
        constants.PROMPT_TYPE_MECHANICS,
        constants.PROMPT_TYPE_CHARACTER_TEMPLATE,
        constants.PROMPT_TYPE_RELATIONSHIP,
        constants.PROMPT_TYPE_REPUTATION,
        constants.PROMPT_TYPE_LIVING_WORLD,
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()
    MODE: str = constants.MODE_DIALOG_HEAVY
    INCLUDE_WORLD_CONTENT: bool = False

    def builder_flags(self) -> dict[str, bool]:
        """Heavy dialog mode keeps debug disabled like regular dialog mode."""
        return {"include_debug": False}


# --- FACTION/ARMY MANAGEMENT DETECTION ---
# Patterns that trigger FactionManagementAgent for forces 20+ units

FACTION_QUERY_PATTERNS = [
    # Basic army management
    "army status",
    "army report",
    "force status",
    "force report",
    "recruit ",
    "disband ",
    "pay troops",
    "fortify position",
    "forced march",
    "battle plan",
    "mass combat",
    "morale check",
    "unit blocks",
    "upkeep",
    "my army",
    "my forces",
    "troop strength",
    "rally troops",
    "tactical retreat",
    "flanking order",
    "commander bonus",
    # Faction minigame patterns
    "faction status",
    "faction rankings",
    "faction power",
    "faction territory",
    "faction citizens",
    "faction arcana",
    "deploy spies",
    "intel report",
    "intel operation",
    "spy mission",
    "assault ",
    "skirmish ",
    "pillage ",
    "build farms",
    "build training",
    "build artisans",
    "build library",
    "build mana font",
    "build fortification",
    "build ward",
    "build shadow network",
    "alliance propose",
    "alliance status",
    "faction prestige",
    "council vote",
    "appoint ",
    "apotheosis",
    "end turn",
    "my faction",
    "lineage traits",
    "faction research",
]

# Patterns that allow enabling the faction minigame (can bypass enabled check)
# These are the ONLY patterns that work when minigame is disabled
FACTION_ENABLEMENT_PATTERNS = [
    "enable_faction_minigame",
    "enable faction mode",
    "enable faction minigame",
    "faction minigame",
]

# Operational patterns that REQUIRE minigame enabled=True
# These are blocked when minigame is disabled to prevent accidental triggering
FACTION_MINIGAME_PATTERNS = [
    "faction status",
    "faction rankings",
    "faction power",
    "deploy spies",
    "intel report",
    "intel operation",
    "assault ",
    "skirmish ",
    "pillage ",
    "alliance propose",
    "alliance status",
    "apotheosis",
    "end turn",
    "lineage traits",
    "my faction",
    "faction citizens",
    "faction arcana",
    "faction prestige",
]

# Explicit settings commands for spicy mode toggles (handled server-side).
SPICY_TOGGLE_ENABLE_PHRASES = {
    "enable spicy mode",
    "enable_spicy_mode",
    "activate spicy mode",
    "start spicy mode",
}
SPICY_TOGGLE_EXIT_PHRASES = {
    "exit spicy mode",
    "exit_spicy_mode",
    "disable spicy mode",
    "disable_spicy_mode",
    "stop spicy mode",
    "return from spicy mode",
}
SPICY_TOGGLE_UI_PREFIXES = (
    "main character:",
    "player:",
    "user:",
)


def _normalize_spicy_toggle_input(user_input: str) -> str:
    """Normalize user input for spicy toggle command matching."""
    # Strip known UI prefixes like "Main Character:" without stripping narrative colons.
    normalized = user_input.strip()
    lowered = normalized.lower()
    for prefix in SPICY_TOGGLE_UI_PREFIXES:
        if lowered.startswith(prefix):
            normalized = normalized[len(prefix) :].strip()
            break

    normalized = normalized.lower().rstrip(".!?")
    for separator in (" - ", " — ", " – "):
        if separator in normalized:
            normalized = normalized.split(separator, 1)[0].strip()
            break
    return normalized


# Minimum force threshold for automatic faction mode activation
FACTION_FORCE_THRESHOLD = 20


class SpicyModeAgent(DialogAgent):
    """
    Agent for Spicy/Mature Mode interactions.

    This agent handles intimate and romantic content with a specialized literary style.
    It behaves like DialogAgent for conversation flow but adds a spicy mode instruction
    to guide tone and content.

    Key Differences from DialogAgent:
    - Adds PROMPT_TYPE_SPICY_MODE to the dialog prompt stack
    - Focuses on literary quality, sensory details, and emotional depth
    - Handles explicit content boundaries ("fade to black" vs "explicit")

    System Prompt Hierarchy (Dialog + Spicy):
    1. Master directive
    2. Game state instructions
    3. Planning protocol
    4. Dialog system instruction
    5. Spicy Mode Instruction (literary style guide)
    6. Character template
    7. Relationship instruction
    """

    # Required prompts - ordered tuple
    # Dialog prompt stack with an added spicy mode instruction.
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        constants.PROMPT_TYPE_DIALOG,
        constants.PROMPT_TYPE_SPICY_MODE,  # Specialized prompt
        constants.PROMPT_TYPE_NARRATIVE,  # Required for living world integration
        constants.PROMPT_TYPE_CHARACTER_TEMPLATE,
        constants.PROMPT_TYPE_RELATIONSHIP,
        constants.PROMPT_TYPE_LIVING_WORLD,  # Declarative living world integration
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts - focused dialog mode plus spicy instruction
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    MODE: str = constants.MODE_SPICY
    INCLUDE_WORLD_CONTENT: bool = False

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:
        """Match when user_settings.spicy_mode is explicitly enabled."""
        return _is_spicy_mode_enabled(game_state)


class FactionManagementAgent(BaseAgent):
    """
    Agent for Faction/Army Management (Forces 20+ Units).

    This agent handles strategic mass combat, army management, and the
    WorldAI Faction Management mini-game. It uses specialized prompts
    for unit blocks, daily upkeep, morale, mass combat resolution, and
    when in minigame mode, faction vs faction strategy.

    Responsibilities:
    - Unit block management (10 soldiers each)
    - Daily upkeep tracking and treasury management
    - Morale system and desertion mechanics
    - Mass combat resolution (army vs army)
    - Commander abilities and lieutenant system
    - Battle results and XP calculation
    - [Minigame] Faction vs AI faction strategic gameplay
    - [Minigame] Territory, citizens, arcana resource management
    - [Minigame] Intel operations with spies and elites
    - [Minigame] Noble alliances, prestige, and council system
    - [Minigame] Apotheosis ritual win condition

    Trigger Conditions (matches_game_state returns True when):
    1. army_data.total_strength >= 20 in game_state
    2. faction_minigame.enabled = true in game_state
    3. User input contains faction-related commands

    System Prompt Hierarchy:
    1. Master directive (establishes AI authority)
    2. Game state instructions (army_data/faction_minigame schema)
    3. Faction management instruction (mass combat rules)
    4. Narrative instruction (CRITICAL: contains code_execution dice rules)
    5. [Optional] Faction minigame instruction (strategic layer)
    6. D&D SRD (base rules reference)
    7. Mechanics (detailed game mechanics)

    Dice Handling:
    - Uses narrative_system_instruction.md for code_execution dice rules
    - Ensures dice rolls use random.randint() via Gemini code_execution
    - Evidence saved to Firestore: see .claude/skills/dice-authenticity-standards.md

    Note: Agent selection via classifier - no longer forced when minigame enabled.
    """

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → faction_management → narrative → dnd_srd → mechanics
    # NOTE: narrative_system_instruction is included because it contains CRITICAL dice
    # handling rules (code_execution for dice, NEVER fabricate) that faction_management
    # needs but doesn't duplicate. Without it, the LLM may output fabricated dice values.
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Required adjacent to game_state
        constants.PROMPT_TYPE_FACTION_MANAGEMENT,
        constants.PROMPT_TYPE_NARRATIVE,  # Dice handling rules (code_execution, no fabrication)
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,
        constants.PROMPT_TYPE_LIVING_WORLD,  # Declarative living world integration
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # Optional: Faction minigame (loaded when minigame is enabled)
    OPTIONAL_PROMPTS: frozenset[str] = frozenset(
        {
            constants.PROMPT_TYPE_FACTION_MINIGAME,
        }
    )

    MODE: str = constants.MODE_FACTION

    def __init__(
        self,
        game_state: GameState | None = None,
        *,
        force_minigame_prompt: bool = False,
    ) -> None:
        """Initialize FactionManagementAgent with optional minigame detection."""
        super().__init__(game_state)
        self._minigame_enabled = self._detect_minigame_enabled()
        self._force_minigame_prompt = bool(force_minigame_prompt)

    def _detect_minigame_enabled(self) -> bool:
        """
        Detect if faction minigame is enabled.

        The minigame requires campaign enablement and respects user settings:
        1. Campaign setting: faction_minigame.enabled must be True
        2. User setting: faction_minigame_enabled (if present) must not be False

        Returns:
            True when campaign is enabled and user has not disabled it
        """
        if self.game_state is None:
            return False

        # Extract user_settings if available
        user_settings = None
        if hasattr(self.game_state, "user_settings") and isinstance(
            self.game_state.user_settings, dict
        ):
            user_settings = self.game_state.user_settings
        elif isinstance(self.game_state, dict):
            candidate_settings = self.game_state.get("user_settings")
            if isinstance(candidate_settings, dict):
                user_settings = candidate_settings

        # Use centralized utility for consistent extraction and validation
        return is_faction_minigame_enabled(
            self.game_state,
            check_user_setting=True,
            user_settings=user_settings,
        )

    @property
    def minigame_enabled(self) -> bool:
        """Check if the faction minigame is active."""
        return self._minigame_enabled

    def get_tools(self) -> list[dict]:
        """Get faction tools when minigame is enabled.

        Returns FACTION_TOOLS for LLM function calling when the faction
        minigame is active. These tools allow the LLM to call backend
        Python code for battle simulation, intel operations, etc.

        Returns:
            List of tool definitions, or empty list if minigame disabled.
        """
        if self._minigame_enabled or self._force_minigame_prompt:
            return FACTION_TOOLS
        return []

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions for faction/army management mode.

        Uses a focused prompt set for strategic mass combat:
        - Master directive (authority)
        - Faction management instruction (mass combat, upkeep, morale)
        - [Optional] Faction minigame instruction (if minigame enabled)
        - Game state (army_data structure)
        - D&D SRD (base rules)
        - Mechanics (detailed game mechanics)

        Args:
            llm_requested_sections: Unused - faction mode uses fixed prompt set

        Returns:
            Complete system instruction string for faction management
        """
        # Parameters intentionally unused - faction mode uses fixed prompt set
        del (
            selected_prompts,
            include_continuation_reminder,
            llm_requested_sections,
        )
        # Note: dice_roll_strategy NOT deleted - passed to build_for_agent

        builder = self._prompt_builder

        # Build faction mode instructions using the standard builder flow
        # This ensures all required prompts (including planning_protocol) are loaded in order
        parts: list[str] = builder.build_for_agent(
            self, dice_roll_strategy=dice_roll_strategy, turn_number=turn_number
        )

        # Add minigame instruction if enabled or explicitly requested
        if self._minigame_enabled or self._force_minigame_prompt:
            try:
                minigame_content = _load_instruction_file(
                    constants.PROMPT_TYPE_FACTION_MINIGAME
                )
                if minigame_content:
                    parts.append(minigame_content)
                    # Add mandatory faction continuation reminder
                    parts.append(builder.build_faction_continuation_reminder())
                    logging_util.info(
                        "🎮 FACTION_MINIGAME: Loaded minigame instruction"
                    )
            except FileNotFoundError:
                logging_util.warning(
                    "🎮 FACTION_MINIGAME: Minigame instruction file not found"
                )

        # Finalize with optional world instructions (for context)
        return builder.finalize_instructions(parts, use_default_world=use_default_world)

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:  # noqa: PLR0912
        """
        Check if faction mode should be active based on game state.

        Faction mode is triggered when:
        - faction_minigame.enabled is True in game state
        - AND army_data exists in game_state AND total_strength >= FACTION_FORCE_THRESHOLD (20)

        Note: The enabled flag FULLY controls faction management. If enabled=False,
        faction agent is never selected regardless of force thresholds.

        Exception: matches_input() allows FACTION_MINIGAME_PATTERNS to bypass enabled check
        for explicit enablement flows (e.g., "enable faction mode", "faction status").

        Args:
            game_state: Current GameState object

        Returns:
            True if faction management is active and FactionManagementAgent should be used
        """
        if game_state is None:
            logging_util.debug(
                "🏰 FACTION_CHECK: game_state is None, not in faction mode"
            )
            return False

        # 🚨 SETTING FULLY CONTROLS: Check enabled flag first
        # Use centralized utility for consistent extraction and validation
        if not is_faction_minigame_enabled(game_state):
            logging_util.debug(
                "🏰 FACTION_CHECK: Minigame disabled (enabled=False), not selecting faction agent"
            )
            return False

        # Minigame is enabled - check if we have forces >= threshold
        # Get army_data from game state
        army_data = None
        if hasattr(game_state, "army_data"):
            army_data = game_state.army_data
        elif hasattr(game_state, "data") and isinstance(game_state.data, dict):
            game_state_dict = game_state.data.get("game_state")
            if isinstance(game_state_dict, dict):
                army_data = game_state_dict.get("army_data")
            else:
                army_data = None

        # Ensure army_data is a dict (handle None or other types)
        if not isinstance(army_data, dict):
            army_data = None

        if not army_data or not isinstance(army_data, dict):
            logging_util.debug(
                "🏰 FACTION_CHECK: No army_data in game_state (enabled=True but no forces)"
            )
            return False

        # Check total_strength threshold
        total_strength_raw = army_data.get("total_strength", 0)
        try:
            total_strength = int(total_strength_raw or 0)
        except (TypeError, ValueError):
            total_strength = 0

        has_forces = total_strength >= FACTION_FORCE_THRESHOLD

        if has_forces:
            logging_util.info(
                f"🏰 FACTION_CHECK: Active with {total_strength} soldiers "
                f"(threshold: {FACTION_FORCE_THRESHOLD}, enabled=True)"
            )
        else:
            logging_util.debug(
                f"🏰 FACTION_CHECK: total_strength={total_strength} "
                f"< threshold={FACTION_FORCE_THRESHOLD} (enabled=True but insufficient forces)"
            )

        return has_forces

    @classmethod
    def matches_input(
        cls, user_input: str, game_state: GameState | None = None
    ) -> bool:
        """
        Check if input contains faction/army management commands.

        Triggers FactionManagementAgent for army-related queries like:
        - "army status", "force report"
        - "recruit infantry", "disband archers"
        - "battle plan", "mass combat"

        Args:
            user_input: Raw user input text
            game_state: Optional game state for context gating

        Returns:
            True if input matches faction management patterns and faction
            context is active
        """
        lower = user_input.lower()

        # Enablement patterns can ALWAYS bypass the enabled check.
        # This allows users to enable the faction minigame even when it's disabled.
        # Example: "enable faction mode" or asking about "faction minigame"
        if any(pattern in lower for pattern in FACTION_ENABLEMENT_PATTERNS):
            return True

        # Operational patterns (deploy spies, assault, etc.) require minigame enabled.
        # This prevents accidental triggering when the user hasn't opted into the feature.
        if not cls.matches_game_state(game_state):
            return False

        # When minigame IS enabled, check both minigame and query patterns
        if any(pattern in lower for pattern in FACTION_MINIGAME_PATTERNS):
            return True

        return any(pattern in lower for pattern in FACTION_QUERY_PATTERNS)


class CampaignUpgradeAgent(BaseAgent):
    """
    Agent for handling campaign tier upgrades (divine/multiverse ascension ceremonies).

    This agent handles the one-time upgrade ceremonies when a player transitions:
    - Normal (mortal) → Divine (Divine Leverage system)
    - Divine or Normal → Sovereign (Multiversal campaign)

    After the ceremony completes, the StoryModeAgent handles ongoing gameplay
    with the new tier's mechanics via optional prompts.

    Priority: Just below GodModeAgent (highest priority after admin commands).
    """

    MODE = constants.MODE_CAMPAIGN_UPGRADE

    # Required prompts - ordered tuple (source of truth for loading order)
    # Order: master → game_state → planning_protocol → dnd_srd → mechanics
    REQUIRED_PROMPT_ORDER: tuple[str, ...] = (
        constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        constants.PROMPT_TYPE_GAME_STATE,
        constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
        constants.PROMPT_TYPE_DND_SRD,
        constants.PROMPT_TYPE_MECHANICS,
        constants.PROMPT_TYPE_LIVING_WORLD,  # Declarative living world integration
    )
    REQUIRED_PROMPTS: frozenset[str] = frozenset(REQUIRED_PROMPT_ORDER)

    # No optional prompts - ceremony prompts are selected dynamically
    OPTIONAL_PROMPTS: frozenset[str] = frozenset()

    @property
    def requires_action_resolution(self) -> bool:
        """Ascension ceremonies are setup events and do not require action resolution audit trails."""
        return False

    def __init__(self, game_state: GameState | None = None) -> None:
        """Initialize the CampaignUpgradeAgent with game state."""
        super().__init__(game_state)
        self._upgrade_type: str | None = None
        if game_state is not None:
            self._upgrade_type = game_state.get_pending_upgrade_type()

    def build_system_instructions(
        self,
        selected_prompts: list[str] | None = None,
        use_default_world: bool = False,
        include_continuation_reminder: bool = True,
        turn_number: int = 0,
        llm_requested_sections: list[str] | None = None,
        dice_roll_strategy: str | None = None,
    ) -> str:
        """
        Build system instructions for campaign upgrade ceremony.

        Returns prompts appropriate for the pending upgrade type
        (divine ascension or multiverse ascension).

        Args:
            selected_prompts: User-selected prompt types (unused - ceremony uses fixed set)
            use_default_world: Whether to include world content (unused)
            include_continuation_reminder: Whether to add reminders (unused)
            turn_number: Current turn number (unused)
            llm_requested_sections: LLM-requested sections (unused)

        Returns:
            Complete system instruction string for the upgrade ceremony
        """
        # Parameters intentionally unused - ceremony uses fixed prompt set
        del (
            selected_prompts,
            use_default_world,
            include_continuation_reminder,
        )
        del llm_requested_sections
        # Note: dice_roll_strategy NOT deleted - passed to build_from_order below

        builder = self._prompt_builder

        # Use build_from_order() with REQUIRED_PROMPT_ORDER to load all required prompts
        # This ensures DND_SRD and MECHANICS are included (matching CombatAgent's pattern)
        parts: list[str] = builder.build_from_order(
            self.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            dice_roll_strategy=dice_roll_strategy,
            turn_number=turn_number,
            advances_time=self.advances_time,
        )

        # Add the appropriate ascension ceremony prompt
        if self._upgrade_type == "multiverse":
            parts.append(
                _load_instruction_file(constants.PROMPT_TYPE_SOVEREIGN_ASCENSION)
            )
            logging_util.info(
                "🌌 CAMPAIGN_UPGRADE: Loading Sovereign ascension ceremony"
            )
        elif self._upgrade_type == "divine":
            parts.append(_load_instruction_file(constants.PROMPT_TYPE_DIVINE_ASCENSION))
            logging_util.info("✨ CAMPAIGN_UPGRADE: Loading Divine ascension ceremony")
        else:
            # Edge case: upgrade flagged but type not determined
            logging_util.warning(
                f"⚠️ CAMPAIGN_UPGRADE: Unknown upgrade type '{self._upgrade_type}', "
                "falling back to core instructions only"
            )

        # Finalize without world content (ceremony doesn't need world lore)
        return builder.finalize_instructions(parts, use_default_world=False)

    @classmethod
    def matches_game_state(cls, game_state: GameState | None) -> bool:
        """
        Check if a campaign upgrade is available based on game state.

        Returns True if:
        - Divine upgrade available (mortal tier, divine_potential >= 100 or level >= 25)
        - Multiverse upgrade available (any tier, universe_control >= 70)

        Args:
            game_state: Current game state to check

        Returns:
            True if an upgrade ceremony should be triggered
        """
        if game_state is None:
            return False

        return game_state.is_campaign_upgrade_available()

    @classmethod
    def matches_input(cls, _user_input: str) -> bool:
        """
        Campaign upgrade is NOT triggered by input - only by game state.

        Args:
            _user_input: Raw user input text (unused)

        Returns:
            Always False - use matches_game_state instead
        """
        return False


def get_agent_for_input(  # noqa: PLR0911, PLR0912, PLR0915
    user_input: str,
    game_state: GameState | None = None,
    mode: str | None = None,
    last_ai_response: str | None = None,
) -> tuple[BaseAgent, dict[str, Any]]:
    """
    Factory function to get the appropriate agent for user input.

    Primary routing is handled by the Semantic Intent Classifier.
    Safety overrides (God Mode) and state-based checks are checked first.

    Priority:
    1. GodModeAgent (Manual override)
    2. Character Creation Completion Override
    3. MODAL AGENT LOCK (Character Creation/Level-Up active)
    4. CampaignUpgradeAgent (State-based - when upgrade is available)
    5. CharacterCreationAgent (State-based - when char creation is active)
    6. PlanningAgent (Explicit override - "THINK:" prefix or mode="think")
    7. Semantic Intent Classification (PRIMARY BRAIN)
       - CombatAgent: Routes on semantic intent (can initiate combat if not active)
       - RewardsAgent: Routes on semantic intent (can check for missed rewards)
       - CharacterCreationAgent: Routes on semantic intent (can initiate recreation)
       - LevelUpAgent: Routes on semantic intent (can initiate level-up workflow)
       - CampaignUpgradeAgent: Routes on semantic intent (can guide toward ascension)
       - FactionManagementAgent: Routes on semantic intent (can initiate faction management)
    8. API Explicit Mode (Forced via UI/Param)
    9. StoryModeAgent (Default)

    Returns:
        Tuple of (agent, metadata) where metadata contains:
        - intent: The classified intent mode (e.g., "dialog", "combat")
        - classifier_source: How agent was selected ("semantic_intent", "state_based", "explicit_override", "keyword_fallback")
        - confidence: Classification confidence (0.0-1.0) if from semantic classifier
        - routing_priority: Priority level string (e.g., "1_god_mode", "7_semantic_dialog")
    """
    # 1. Safety Override: GOD MODE
    if GodModeAgent.matches_input(user_input, mode):
        logging_util.info("🔮 GOD_MODE_DETECTED: Using GodModeAgent")
        metadata = {
            "intent": constants.MODE_GOD,
            "classifier_source": "explicit_override",
            "confidence": 1.0,
            "routing_priority": "1_god_mode",
        }
        return GodModeAgent(game_state), metadata

    custom_state: dict[str, Any] = {}
    rewards_pending: dict[str, Any] = {}
    player_data: dict[str, Any] = {}
    if game_state is not None:
        if hasattr(game_state, "custom_campaign_state"):
            state_value = game_state.custom_campaign_state
            if isinstance(state_value, dict):
                custom_state = state_value
        elif isinstance(game_state, dict):
            state_value = game_state.get("custom_campaign_state", {})
            if isinstance(state_value, dict):
                custom_state = state_value

        if hasattr(game_state, "rewards_pending"):
            rewards_value = game_state.rewards_pending
            if isinstance(rewards_value, dict):
                rewards_pending = rewards_value
        elif isinstance(game_state, dict):
            rewards_value = game_state.get("rewards_pending", {})
            if isinstance(rewards_value, dict):
                rewards_pending = rewards_value

        if hasattr(game_state, "player_character_data"):
            player_value = game_state.player_character_data
            if isinstance(player_value, dict):
                player_data = player_value
        elif isinstance(game_state, dict):
            player_value = game_state.get("player_character_data", {})
            if isinstance(player_value, dict):
                player_data = player_value

    # 2. Character Creation Completion Override: explicit completion exits modal flow
    char_creation_started = custom_state.get("character_creation_in_progress", False)
    char_creation_completed = custom_state.get("character_creation_completed", False)
    if (
        char_creation_started
        and CharacterCreationAgent.matches_input(user_input)
        and not char_creation_completed
    ):
        logging_util.info("🎭 CHARACTER_CREATION_COMPLETE: Transitioning to Story")
        # Mutate state to finalize (aligned with original behavior)
        custom_state["character_creation_in_progress"] = False
        custom_state["character_creation_completed"] = True
        custom_state["character_creation_stage"] = "complete"
        custom_state["level_up_pending"] = False
        metadata = {
            "intent": constants.MODE_CHARACTER,
            "classifier_source": "state_based",
            "confidence": 1.0,
            "routing_priority": "3_char_creation_complete",
        }
        return StoryModeAgent(game_state), metadata

    # 3. Modal Agent Lock: keep users in character creation / level-up until explicit exit
    char_creation_started = custom_state.get("character_creation_in_progress", False)
    char_creation_completed = custom_state.get("character_creation_completed", False)
    if char_creation_started and not char_creation_completed:
        logging_util.info(
            "🔒 MODAL_LOCK: CharacterCreationAgent locked - bypassing all other routing including classifier"
        )
        metadata = {
            "intent": constants.MODE_CHARACTER_CREATION,
            "classifier_source": "modal_lock",
            "confidence": 1.0,
            "routing_priority": "3_modal_char_creation",
        }
        return CharacterCreationAgent(game_state), metadata

    level_up_modal_active = custom_state.get(
        "level_up_in_progress", False
    ) or custom_state.get("level_up_pending", False)
    level_up_modal_active = level_up_modal_active or rewards_pending.get(
        "level_up_available", False
    )

    # Check for completion/cancellation override (like CharacterCreationAgent)
    level_up_completed = custom_state.get("level_up_complete", False)
    level_up_cancelled = custom_state.get("level_up_cancelled", False)

    # Exit modal if completed or cancelled
    level_up_exit_active = level_up_completed or level_up_cancelled
    if level_up_exit_active:
        logging_util.info(
            f"🔓 LEVEL_UP_EXIT: Modal exiting (complete={level_up_completed}, cancelled={level_up_cancelled})"
        )
        level_up_modal_active = False

    # Additional check: if explicitly set to False, respect that (stale flag guard)
    level_up_in_progress = custom_state.get("level_up_in_progress")
    if level_up_in_progress is False:
        logging_util.info(
            "🔓 LEVEL_UP_STALE_FLAG: level_up_in_progress=False explicitly set, not activating modal"
        )
        level_up_modal_active = False

    level_up_pending_flag = custom_state.get("level_up_pending")
    if level_up_pending_flag is False and not bool(level_up_in_progress):
        logging_util.info(
            "🔓 LEVEL_UP_STALE_FLAG: level_up_pending=False explicitly set, not activating modal"
        )
        level_up_modal_active = False

    if level_up_modal_active and _is_stale_level_up_pending(
        custom_state, rewards_pending, player_data
    ):
        logging_util.info(
            "🔓 LEVEL_UP_STALE_FLAG: level_up_pending ignored "
            "(XP below next-level threshold and no rewards_pending signal)"
        )
        level_up_modal_active = False

    if level_up_modal_active:
        logging_util.info(
            "🔒 MODAL_LOCK: LevelUpAgent locked - bypassing all other routing including classifier"
        )
        metadata = {
            "intent": constants.MODE_LEVEL_UP,
            "classifier_source": "modal_lock",
            "confidence": 1.0,
            "routing_priority": "3_modal_level_up",
        }
        return LevelUpAgent(game_state), metadata

    # 4. State-based: Campaign upgrade ceremonies (divine/multiverse ascension)
    # This check happens BEFORE character creation since upgrades are more important
    if CampaignUpgradeAgent.matches_game_state(game_state):
        logging_util.info(
            "⬆️ CAMPAIGN_UPGRADE_AVAILABLE (STATE-BASED): Using CampaignUpgradeAgent"
        )
        metadata = {
            "intent": constants.MODE_CAMPAIGN_UPGRADE,
            "classifier_source": "state_based",
            "confidence": 1.0,
            "routing_priority": "4_campaign_upgrade_state",
        }
        return CampaignUpgradeAgent(game_state), metadata

    # 5. State-based Context (Character Creation only - Combat/Rewards handled via semantic classifier)
    if level_up_exit_active:
        logging_util.info(
            "🔓 LEVEL_UP_EXIT: Skipping CharacterCreationAgent state lock to avoid stale level-up recapture"
        )
    elif CharacterCreationAgent.matches_game_state(game_state):
        logging_util.info("🎭 CHARACTER_CREATION_ACTIVE: Using CharacterCreationAgent")
        metadata = {
            "intent": constants.MODE_CHARACTER_CREATION,
            "classifier_source": "state_based",
            "confidence": 1.0,
            "routing_priority": "5_char_creation_state",
        }
        return CharacterCreationAgent(game_state), metadata

    # 5b. State-based: Faction Minigame Enabled
    # NOTE: Previously this FORCED FactionManagementAgent, bypassing the classifier.
    # This caused ALL inputs to route to faction agent when minigame was enabled,
    # even non-faction actions like exploration, dialog, or combat.
    # Now we let the semantic classifier decide based on user intent (step 7).
    # FactionManagementAgent will still be selected for faction-related inputs
    # via MODE_FACTION classification.
    #
    # The faction minigame state is used by:
    # - FactionManagementAgent.get_tools() to provide faction tools
    # - FactionManagementAgent.build_system_instructions() to load minigame prompts
    if FactionManagementAgent.matches_game_state(game_state):
        logging_util.debug(
            "🏰 FACTION_MINIGAME_ENABLED: Classifier will route faction-related inputs"
        )

    # 5c. State-based: Active Combat (in_combat=True) → FORCE CombatAgent
    # Combat takes priority over dialog when both are active
    try:
        if CombatAgent.matches_game_state(game_state):
            logging_util.info("⚔️ COMBAT_ACTIVE (STATE-BASED): Using CombatAgent")
            metadata = {
                "intent": constants.MODE_COMBAT,
                "classifier_source": "state_based",
                "confidence": 1.0,
                "routing_priority": "5c_combat_state",
            }
            return CombatAgent(game_state), metadata
    except (TypeError, AttributeError) as e:
        # Defensive: Mock objects or incomplete game_state may cause errors
        logging_util.debug("CombatAgent state check failed: %s", e)

    # 7. Semantic Intent Classification (EARLY - before dialog state check)
    # Run classifier EARLY so we can use its result to override dialog routing.
    # This ensures faction enablement ("enable_faction_minigame") routes to
    # FactionManagementAgent even when dialog context is active.

    def _should_skip_classifier_context(
        *,
        state: GameState | None,
        last_response: str | None,
    ) -> bool:
        if not last_response or not last_response.strip():
            return False

        # Skip context on first actionable turn to avoid character-creation bleed
        player_turn = None
        if isinstance(state, dict):
            player_turn = state.get("player_turn")
        else:
            player_turn = getattr(state, "player_turn", None)
        if isinstance(player_turn, int) and player_turn == 0:
            return True

        marker = last_response.upper()
        return (
            "CHARACTER CREATION" in marker
            or "CHARACTER CUSTOMIZATION" in marker
            or "[CHARACTER CREATION" in marker
            or "[LEVEL UP" in marker
        )

    # Run classifier early (before dialog state check)
    intent_mode = constants.MODE_CHARACTER
    confidence = 0.0
    start_time = time.time()
    # Spicy mode toggle biases the classifier toward spicy intent (without forcing).
    spicy_bias = _is_spicy_mode_enabled(game_state)

    try:
        # Pass context (last AI response) to the classifier to improve accuracy
        context_for_classifier = last_ai_response
        if _should_skip_classifier_context(
            state=game_state,
            last_response=last_ai_response,
        ):
            context_for_classifier = None
            logging_util.info(
                "🧠 CLASSIFIER_CONTEXT_SKIPPED: first_turn_or_char_creation_context"
            )
        intent_mode, confidence = intent_classifier.classify_intent(
            user_input,
            context=context_for_classifier,
            spicy_bias=spicy_bias,
        )
        elapsed_time = time.time() - start_time
        ctx_flag = " [WITH_CONTEXT]" if last_ai_response else ""
        logging_util.info(
            f"🧠 CLASSIFIER: classify_intent(){ctx_flag} completed in {elapsed_time * 1000:.2f}ms"
        )
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging_util.warning(
            f"🧠 CLASSIFIER: Error during classification: {e}. Defaulting to MODE_CHARACTER. (took {elapsed_time * 1000:.2f}ms)"
        )
        intent_mode = constants.MODE_CHARACTER
        confidence = 0.0

    # Security safeguard: MODE_GOD must never come from the classifier
    if intent_mode == constants.MODE_GOD:
        logging_util.warning(
            "🚨 SECURITY: Classifier returned MODE_GOD (invalid). Defaulting to MODE_CHARACTER."
        )
        intent_mode = constants.MODE_CHARACTER

    # 5d. State-based: Dialog Context Active → DialogAgent
    # Only triggers if combat is NOT active (combat checked first)
    # AND classifier did NOT return a high-confidence override intent
    #
    # POLICY DECISION: State-based dialog routing is ALLOWED and INTENTIONAL
    # - This is NOT keyword matching - it's state validation via DialogAgent.matches_game_state()
    # - Purpose: Preserve multi-turn conversation continuity
    # - Example: User is mid-conversation with NPC → next input continues dialog
    # - Prevents context loss when LLM maintains active_dialog_npc in game state
    # - New dialog initiations still go through semantic classifier (Priority 7)
    #
    # EXCEPTION: Classifier-detected faction/spicy/heavy-dialog intent overrides dialog routing
    # - MODE_FACTION with confidence >= 0.7 bypasses dialog state
    # - MODE_SPICY with confidence >= 0.7 bypasses dialog state
    # - MODE_DIALOG_HEAVY (any confidence) bypasses dialog state
    #   * Heavy dialog is a semantic routing decision that should never downgrade to DialogAgent
    #   * If classifier says heavy, trust it regardless of confidence (bead PR-mde)
    # - This allows "enable_faction_minigame", spicy content, and heavy dialog to route correctly mid-dialog
    #
    # DETERMINISTIC OVERRIDE: Exact "enable_faction_minigame" command always overrides dialog
    # - This prevents the enable command from being silently ignored when classifier confidence is low
    # - Ensures users mid-dialog can always enable the faction minigame
    is_explicit_enable_command = user_input.strip().lower() == "enable_faction_minigame"
    classifier_overrides_dialog = is_explicit_enable_command or (
        (intent_mode == constants.MODE_FACTION and confidence >= 0.7)
        or (intent_mode == constants.MODE_SPICY and confidence >= 0.7)
        or (intent_mode == constants.MODE_DIALOG_HEAVY)
    )
    try:
        if (
            DialogAgent.matches_game_state(game_state)
            and not classifier_overrides_dialog
        ):
            logging_util.info(
                "💬 DIALOG_CONTEXT_ACTIVE (STATE-BASED): Using DialogAgent",
            )
            metadata = {
                "intent": constants.MODE_DIALOG,
                "classifier_source": "state_based",
                "confidence": 1.0,
                "routing_priority": "5d_dialog_state",
            }
            return DialogAgent(game_state), metadata
    except (TypeError, AttributeError) as e:
        # Defensive: Mock objects or incomplete game_state may cause errors
        logging_util.debug("DialogAgent state check failed: %s", e)

    # 6. Explicit Overrides (THINK: prefix or API mode params)
    if PlanningAgent.matches_input(user_input, mode):
        logging_util.info(
            "🧠 THINK_MODE_DETECTED: Using PlanningAgent (Explicit Override)"
        )
        metadata = {
            "intent": constants.MODE_THINK,
            "classifier_source": "explicit_override",
            "confidence": 1.0,
            "routing_priority": "6_think_override",
        }
        return PlanningAgent(game_state), metadata

    # 6b. Choice Matching - KEYWORD ROUTING REMOVED
    # See CLAUDE.md: "NO KEYWORD MATCHING for dialog detection"
    # Choice matching still detects explicit choice selections, but routing
    # is delegated to the semantic classifier (section 7) instead of keywords.
    # This ensures ALL dialog routing goes through the classifier as required.

    # 7. Semantic Intent Routing (using classifier result from 5c)
    # NOTE: intent_mode and confidence already computed in section 5c above

    if intent_mode == constants.MODE_THINK:
        logging_util.info(
            f"🧠 SEMANTIC_INTENT_THINK: ({confidence:.2f}) -> PlanningAgent"
        )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_think",
        }
        return PlanningAgent(game_state), metadata

    if intent_mode == constants.MODE_INFO:
        logging_util.info(f"📦 SEMANTIC_INTENT_INFO: ({confidence:.2f}) -> InfoAgent")
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_info",
        }
        return InfoAgent(game_state), metadata

    if intent_mode == constants.MODE_COMBAT:
        # Route to CombatAgent based on semantic intent
        # Agent can handle both active combat and initiating new combat
        if CombatAgent.matches_game_state(game_state):
            logging_util.info(
                f"⚔️ SEMANTIC_INTENT_COMBAT: ({confidence:.2f}) -> CombatAgent (combat active)"
            )
        else:
            logging_util.info(
                f"⚔️ SEMANTIC_INTENT_COMBAT: ({confidence:.2f}) -> CombatAgent (initiating combat)"
            )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_combat",
        }
        return CombatAgent(game_state), metadata

    if intent_mode == constants.MODE_REWARDS:
        # Route to RewardsAgent based on semantic intent
        # Agent can handle both pending rewards and checking for missed rewards
        if RewardsAgent.matches_game_state(game_state):
            logging_util.info(
                f"🏆 SEMANTIC_INTENT_REWARDS: ({confidence:.2f}) -> RewardsAgent (rewards pending)"
            )
        else:
            logging_util.info(
                f"🏆 SEMANTIC_INTENT_REWARDS: ({confidence:.2f}) -> RewardsAgent (checking for rewards)"
            )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_rewards",
        }
        return RewardsAgent(game_state), metadata

    if intent_mode == constants.MODE_DEFERRED_REWARDS:
        # Route to DeferredRewardsAgent for explicit missed rewards check
        logging_util.info(
            f"🔍 SEMANTIC_INTENT_DEFERRED_REWARDS: ({confidence:.2f}) -> DeferredRewardsAgent (explicit check)"
        )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_deferred_rewards",
        }
        return DeferredRewardsAgent(game_state), metadata

    if intent_mode == constants.MODE_LEVEL_UP:
        # Mirror CharacterCreationAgent safeguards to prevent low-confidence
        # semantic misfires from freezing time via modal/non-time-advancing agents.
        level_up_active = LevelUpAgent.matches_game_state(game_state)
        explicit_intent_threshold = EXPLICIT_SEMANTIC_INTENT_THRESHOLD
        is_explicit_request = confidence >= explicit_intent_threshold

        if level_up_active or is_explicit_request:
            logging_util.info(
                f"🆙 SEMANTIC_INTENT_LEVEL_UP: ({confidence:.2f}) -> LevelUpAgent"
            )
            metadata = {
                "intent": intent_mode,
                "classifier_source": "semantic_intent",
                "confidence": confidence,
                "routing_priority": "7_semantic_level_up",
            }
            return LevelUpAgent(game_state), metadata

        logging_util.info(
            f"🆙 SEMANTIC_INTENT_LEVEL_UP: ({confidence:.2f}) below threshold with inactive level-up state; falling back"
        )

    if intent_mode == constants.MODE_CHARACTER_CREATION:
        # Route to CharacterCreationAgent only when either:
        # 1) character creation/level-up is active in game state, or
        # 2) semantic classifier is highly confident (explicit-request threshold).
        # This prevents semantic misfires (e.g. "time skip"/"resume story") from
        # freezing time via CharacterCreationAgent.
        char_creation_active = CharacterCreationAgent.matches_game_state(game_state)
        # Use high-confidence threshold to treat as explicit request
        # This replaces legacy regex-based keyword matching per NLP guidelines
        explicit_intent_threshold = EXPLICIT_SEMANTIC_INTENT_THRESHOLD
        is_explicit_request = confidence >= explicit_intent_threshold

        if not char_creation_active and not is_explicit_request:
            logging_util.warning(
                f"🎭 SEMANTIC_INTENT_CHAR_CREATION_SUPPRESSED: ({confidence:.2f}) "
                "classifier predicted character_creation but confidence was below "
                f"explicit threshold ({explicit_intent_threshold}) and state is not "
                "in character-creation mode. Falling back to StoryModeAgent."
            )
        elif char_creation_active:
            logging_util.info(
                f"🎭 SEMANTIC_INTENT_CHAR_CREATION: ({confidence:.2f}) -> CharacterCreationAgent (char creation active)"
            )
            metadata = {
                "intent": intent_mode,
                "classifier_source": "semantic_intent",
                "confidence": confidence,
                "routing_priority": "7_semantic_char_creation",
            }
            return CharacterCreationAgent(game_state), metadata
        else:
            logging_util.info(
                f"🎭 SEMANTIC_INTENT_CHAR_CREATION: ({confidence:.2f}) -> CharacterCreationAgent (explicit high-confidence request)"
            )
            metadata = {
                "intent": intent_mode,
                "classifier_source": "semantic_intent",
                "confidence": confidence,
                "routing_priority": "7_semantic_char_creation",
            }
            return CharacterCreationAgent(game_state), metadata

    if intent_mode == constants.MODE_FACTION:
        # Route to FactionManagementAgent based on semantic intent
        # Agent can handle both active faction minigame and initiating faction management
        minigame_enabled = FactionManagementAgent.matches_game_state(game_state)
        if minigame_enabled:
            logging_util.info(
                f"🏰 SEMANTIC_INTENT_FACTION: ({confidence:.2f}) -> FactionManagementAgent (faction minigame active)"
            )
        else:
            logging_util.info(
                f"🏰 SEMANTIC_INTENT_FACTION: ({confidence:.2f}) -> FactionManagementAgent (initiating faction management)"
            )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_faction",
        }
        return (
            FactionManagementAgent(
                game_state,
                force_minigame_prompt=not minigame_enabled,
            ),
            metadata,
        )

    if intent_mode == constants.MODE_CAMPAIGN_UPGRADE:
        # Route to CampaignUpgradeAgent based on semantic intent
        # Agent can handle upgrade ceremonies and guide players toward ascension
        if CampaignUpgradeAgent.matches_game_state(game_state):
            logging_util.info(
                f"⬆️ SEMANTIC_INTENT_CAMPAIGN_UPGRADE: ({confidence:.2f}) -> CampaignUpgradeAgent (upgrade available)"
            )
        else:
            logging_util.info(
                f"⬆️ SEMANTIC_INTENT_CAMPAIGN_UPGRADE: ({confidence:.2f}) -> CampaignUpgradeAgent (guiding toward ascension)"
            )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_campaign_upgrade",
        }
        return CampaignUpgradeAgent(game_state), metadata

    if intent_mode == constants.MODE_DIALOG:
        # Route to standard dialog agent for semantic MODE_DIALOG.
        # Heavy dialog is classifier-only via MODE_DIALOG_HEAVY.
        if DialogAgent.matches_game_state(game_state):
            logging_util.info(
                "💬 SEMANTIC_INTENT_DIALOG: (%.2f) -> DialogAgent (dialog context active)",
                confidence,
            )
        else:
            logging_util.info(
                "💬 SEMANTIC_INTENT_DIALOG: (%.2f) -> DialogAgent (initiating dialog)",
                confidence,
            )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_dialog",
        }
        return DialogAgent(game_state), metadata

    if intent_mode == constants.MODE_DIALOG_HEAVY:
        logging_util.info(
            "💬 SEMANTIC_INTENT_DIALOG_HEAVY: (%.2f) -> HeavyDialogAgent",
            confidence,
        )
        metadata = {
            "intent": intent_mode,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "7_semantic_dialog_heavy",
        }
        return HeavyDialogAgent(game_state), metadata

    if intent_mode == constants.MODE_SPICY:
        # Check if this is a spicy toggle command (enable/exit spicy mode).
        # Toggle commands should NOT route to SpicyModeAgent - they just update settings
        # and should be handled as character mode requests.
        normalized_input = _normalize_spicy_toggle_input(user_input)
        is_spicy_toggle = (
            normalized_input in SPICY_TOGGLE_ENABLE_PHRASES
            or normalized_input in SPICY_TOGGLE_EXIT_PHRASES
        )

        if is_spicy_toggle:
            # Skip spicy routing - let toggle commands fall through to character mode.
            # The settings update is handled server-side in world_logic.py.
            logging_util.info(
                f"🌶️ SPICY_TOGGLE_DETECTED: '{user_input}' is a toggle command, "
                "skipping SpicyModeAgent routing -> character mode"
            )
            # Don't return here - fall through to character mode
        else:
            # Route to SpicyModeAgent based on semantic intent, regardless of toggle state.
            # Toggle state is handled server-side and should not block semantic routing.
            logging_util.info(
                f"🌶️ SEMANTIC_INTENT_SPICY: ({confidence:.2f}) -> SpicyModeAgent"
            )
            metadata = {
                "intent": intent_mode,
                "classifier_source": "semantic_intent",
                "confidence": confidence,
                "routing_priority": "7_semantic_spicy",
            }
            return SpicyModeAgent(game_state), metadata

    # 8. API Explicit Mode (USER-FACING MODES ONLY)
    # CRITICAL: Only allow forcing user-accessible modes (character, god, think)
    # Internal agent modes (dialog, combat, rewards, etc.) must be auto-selected by system
    if mode:
        # Normalize mode to lowercase for case-insensitive comparison (consistent with Priority 1 and 4)
        normalized_mode = mode.lower() if isinstance(mode, str) else mode

        # Allow forcing user-facing modes only
        if normalized_mode == constants.MODE_THINK:
            logging_util.info(f"🔌 API_EXPLICIT_MODE: mode={mode} -> PlanningAgent")
            metadata = {
                "intent": constants.MODE_THINK,
                "classifier_source": "explicit_mode",
                "confidence": 1.0,
                "routing_priority": "8_api_explicit_think",
            }
            return PlanningAgent(game_state), metadata
        if normalized_mode == constants.MODE_GOD:
            logging_util.info(f"🔌 API_EXPLICIT_MODE: mode={mode} -> GodModeAgent")
            metadata = {
                "intent": constants.MODE_GOD,
                "classifier_source": "explicit_mode",
                "confidence": 1.0,
                "routing_priority": "8_api_explicit_god",
            }
            return GodModeAgent(game_state), metadata
        if normalized_mode == constants.MODE_DEFERRED_REWARDS:
            logging_util.info(
                f"🔌 API_EXPLICIT_MODE: mode={mode} -> DeferredRewardsAgent (explicit check)"
            )
            metadata = {
                "intent": constants.MODE_DEFERRED_REWARDS,
                "classifier_source": "explicit_mode",
                "confidence": 1.0,
                "routing_priority": "8_api_explicit_deferred_rewards",
            }
            return DeferredRewardsAgent(game_state), metadata
        if normalized_mode in (
            constants.MODE_INFO,
            constants.MODE_COMBAT,
            constants.MODE_REWARDS,
            constants.MODE_CHARACTER_CREATION,
            constants.MODE_LEVEL_UP,
            constants.MODE_FACTION,
            constants.MODE_CAMPAIGN_UPGRADE,
            constants.MODE_DIALOG,
            constants.MODE_DIALOG_HEAVY,
            constants.MODE_SPICY,
        ):
            # These are INTERNAL modes - users cannot force them
            # Log warning and fall through to automatic selection
            logging_util.warning(
                f"⚠️ INVALID_MODE_FORCING: User attempted to force internal mode={mode}. "
                f"Internal modes (info, combat, rewards, character_creation, level_up, faction, campaign_upgrade, dialog, dialog_heavy, spicy) "
                f"must be auto-selected by the system. Falling through to automatic agent selection."
            )
            # Fall through to automatic selection logic below
        # MODE_CHARACTER falls through to default StoryModeAgent

    # 8. Default Fallback (always returns StoryModeAgent if no other agent matched)
    if intent_mode == constants.MODE_CHARACTER:
        logging_util.info(
            f"🎭 SEMANTIC_INTENT_STORY: ({confidence:.2f}) -> StoryModeAgent"
        )
        metadata = {
            "intent": constants.MODE_CHARACTER,
            "classifier_source": "semantic_intent",
            "confidence": confidence,
            "routing_priority": "10_default_story",
            "raw_classifier_intent": intent_mode,
            "raw_classifier_confidence": confidence,
            "raw_classifier_source": "semantic_intent",
        }
    else:
        # Fallback for any unexpected intent_mode values
        logging_util.info(
            f"🎭 DEFAULT_FALLBACK: intent_mode={intent_mode} -> StoryModeAgent"
        )
        metadata = {
            "intent": constants.MODE_CHARACTER,
            "classifier_source": "default_fallback",
            "confidence": 0.0,
            "routing_priority": "10_default_fallback",
            "raw_classifier_intent": intent_mode,
            "raw_classifier_confidence": confidence,
            "raw_classifier_source": "semantic_intent",
        }
    return StoryModeAgent(game_state), metadata


# ============================================================================
# ALL AGENT CLASSES (for validation)
# ============================================================================
ALL_AGENT_CLASSES: tuple[type[BaseAgent], ...] = (
    StoryModeAgent,
    GodModeAgent,
    CharacterCreationAgent,
    LevelUpAgent,
    FactionManagementAgent,
    CampaignUpgradeAgent,
    PlanningAgent,
    InfoAgent,
    CombatAgent,
    RewardsAgent,
    DeferredRewardsAgent,
    HeavyDialogAgent,
    DialogAgent,
    SpicyModeAgent,
)


def mode_advances_time(mode: str | None) -> bool:
    """Return whether the supplied agent mode advances world time."""
    if mode is None or mode not in _MODE_ADVANCES_TIME_CACHE:
        return True
    return _MODE_ADVANCES_TIME_CACHE[mode]


_MODE_ADVANCES_TIME_CACHE: dict[str, bool] = {
    constants.MODE_CHARACTER: True,
    constants.MODE_DIALOG: True,
    constants.MODE_DIALOG_HEAVY: True,
    constants.MODE_COMBAT: True,
    constants.MODE_GOD: False,
    constants.MODE_THINK: False,
    constants.MODE_INFO: False,
    constants.MODE_REWARDS: False,
    constants.MODE_DEFERRED_REWARDS: False,
    constants.MODE_CHARACTER_CREATION: False,
    constants.MODE_LEVEL_UP: False,
    constants.MODE_CAMPAIGN_UPGRADE: True,
    constants.MODE_FACTION: True,
    constants.MODE_SPICY: True,
}


def validate_all_agent_prompt_orders() -> dict[str, list[str]]:
    """
    Validate prompt order invariants for all agent classes.

    Returns:
        Dict mapping agent class names to their validation errors.
        Empty dict means all agents are valid.
    """
    errors = {}
    for agent_cls in ALL_AGENT_CLASSES:
        agent_errors = agent_cls.validate_prompt_order()
        if agent_errors:
            errors[agent_cls.__name__] = agent_errors
    return errors


# Export all public classes and functions
__all__ = [
    "BaseAgent",
    "StoryModeAgent",
    "GodModeAgent",
    "CharacterCreationAgent",
    "LevelUpAgent",
    "CampaignUpgradeAgent",
    "PlanningAgent",
    "InfoAgent",
    "CombatAgent",
    "RewardsAgent",
    "FactionManagementAgent",
    "HeavyDialogAgent",
    "DialogAgent",
    "SpicyModeAgent",
    "get_agent_for_input",
    "FACTION_QUERY_PATTERNS",
    "FACTION_MINIGAME_PATTERNS",
    "FACTION_FORCE_THRESHOLD",
    "validate_prompt_order",
    "validate_all_agent_prompt_orders",
    "mode_advances_time",
    "ALL_AGENT_CLASSES",
    "MANDATORY_FIRST_PROMPT",
    "GAME_STATE_PLANNING_PAIR",
]
