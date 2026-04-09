"""
Context Compaction - Token Budget Allocation and Component Compaction

This module implements component-level token budget allocation for LLM requests,
ensuring story context quality while preventing any single component from
consuming excessive tokens.

Key Responsibilities:
- Allocate token budgets across LLM request components (min/max constraints)
- Compact oversized components using component-specific strategies
- Generate and persist budget warnings for user awareness
- Maintain guaranteed minimum allocations (especially story context)

Architecture:
This module was extracted from llm_service.py to isolate budget allocation logic
per user request. The functions here implement a min-first, fill-to-max allocation
strategy that guarantees story context gets at least 30% of the token budget.

Budget Allocation Strategy (Min-First, Fill-to-Max):
1. MEASURE all component sizes
2. ALLOCATE minimums to all components (68% total)
3. FILL to maximums in priority order with remaining budget (32%)
4. GIVE remaining budget to story context (can exceed 60% soft max)
5. COMPACT over-budget components (except system instruction unless >100k)

Priority order for fill-to-max:
1. system_instruction (10-40%, NO compaction unless >100k, warn if over 40%)
2. game_state (5-20%, compact if over)
3. core_memories (20-30%, compact if over)
4. entity_tracking (3-15%, compact if over)
5. story_context (30-60%, guaranteed min 30%, gets leftovers)

Dependencies:
- token_utils: Token estimation utilities
- logging_util: Structured logging infrastructure
"""

import json
from dataclasses import dataclass
from typing import Any

from mvp_site import logging_util
from mvp_site.token_utils import estimate_tokens

# ============================================================================
# BUDGET ALLOCATION CONSTANTS
# ============================================================================
# These percentages define min/max token allocations for each component.
# Minimums sum to 68% of total budget, leaving 32% for fill-to-max allocation.

# System Instruction (campaign settings, world lore, game rules)
BUDGET_SYSTEM_INSTRUCTION_MIN: float = 0.10  # 10% minimum
BUDGET_SYSTEM_INSTRUCTION_WARN: float = 0.40  # 40% warning threshold
BUDGET_SYSTEM_INSTRUCTION_MAX: float = (
    0.50  # 50% maximum (soft cap - warning if exceeded)
)
SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD: int = 100_000  # Force-compact if > 100k tokens

# Game State (character stats, location, inventory, quests)
BUDGET_GAME_STATE_MIN: float = 0.05  # 5% minimum
BUDGET_GAME_STATE_MAX: float = 0.20  # 20% maximum

# Core Memories (campaign-critical facts and summaries)
# NOTE: These are campaign-critical facts accumulated over the entire game.
# A large budget preserves narrative context that the LLM needs to maintain
# consistency across long-running campaigns (1000+ turns).
BUDGET_CORE_MEMORIES_MIN: float = 0.20  # 20% minimum
BUDGET_CORE_MEMORIES_MAX: float = 0.30  # 30% maximum

# Entity Tracking (NPC context for current scene)
BUDGET_ENTITY_TRACKING_MIN: float = 0.03  # 3% minimum
BUDGET_ENTITY_TRACKING_MAX: float = 0.15  # 15% maximum

# Story Context (recent narrative history)
# NOTE: Reduced from 40% to 30% to accommodate increased core_memories budget (20-30%).
# Story still gets 30% guaranteed minimum, and can expand to 60% if other components are small.
BUDGET_STORY_CONTEXT_MIN: float = 0.30  # 30% minimum (GUARANTEED)
BUDGET_STORY_CONTEXT_MAX: float = 0.60  # 60% soft maximum
BUDGET_STORY_CONTEXT_ABSOLUTE_MIN: float = 0.15  # 15% emergency floor

# ============================================================================
# GAME STATE COMPACTION PRIORITY TIERS
# ============================================================================
# Define which game state fields are preserved during compaction.
# Lower priority fields are dropped first when budget is tight.

GAME_STATE_PRIORITY_CRITICAL: tuple[str, ...] = (
    "current_hp",
    "max_hp",
    "temp_hp",
    "armor_class",
    "current_location",
    "in_combat",
    "combat_participants",
    "turn_order",
)

GAME_STATE_PRIORITY_HIGH: tuple[str, ...] = (
    "inventory",
    "active_quests",
    "character_name",
    "abilities",
    "skills",
)

GAME_STATE_PRIORITY_MEDIUM: tuple[str, ...] = (
    "world_data",  # Will be selectively trimmed
    "world_events",  # LW state required for continuity and cross-turn coherence
    "reputation",
)

GAME_STATE_PRIORITY_LOW: tuple[str, ...] = (
    "completed_quests",
    "quest_history",
    "dialogue_history",
)


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class BudgetAllocation:
    """
    Budget allocation result for a single component.

    Tracks measured size, allocated tokens, and whether compaction was applied.
    """

    component: str
    measured_tokens: int
    allocated_tokens: int
    was_compacted: bool = False
    compaction_ratio: float = 1.0  # allocated / measured (1.0 if no compaction)

    @property
    def utilization_pct(self) -> float:
        """Percentage of allocated budget used."""
        if self.allocated_tokens <= 0:
            return 0.0
        return self.measured_tokens / self.allocated_tokens * 100


@dataclass
class RequestBudgetResult:
    """
    Complete budget allocation result for an LLM request.

    Contains allocations for all components, warnings, and compacted content.
    """

    max_input_allowed: int
    allocations: dict[str, BudgetAllocation]
    warnings: list[dict[str, Any]]
    compacted_content: dict[str, Any]

    def get_story_budget(self) -> int:
        """Get allocated tokens for story_context component."""
        story_alloc = self.allocations.get("story_context")
        return story_alloc.allocated_tokens if story_alloc else 0

    def get_allocation(self, component: str) -> BudgetAllocation | None:
        """Get allocation for a specific component."""
        return self.allocations.get(component)

    def log_summary(self) -> str:
        """Generate detailed log summary of budget allocations."""
        lines = [f"📊 BUDGET_ALLOCATION_SUMMARY (budget={self.max_input_allowed:,}tk):"]
        for component, alloc in self.allocations.items():
            # FIX Bug worktree_logs6-6lg: Guard division by zero
            pct = (
                (alloc.allocated_tokens / self.max_input_allowed * 100)
                if self.max_input_allowed > 0
                else 0.0
            )
            status = "🔨 COMPACTED" if alloc.was_compacted else "✅ OK"
            lines.append(
                f"  {component}: {alloc.measured_tokens:,}tk -> "
                f"{alloc.allocated_tokens:,}tk ({pct:.1f}%) {status}"
            )
        if self.warnings:
            lines.append(
                f"  ⚠️ WARNINGS: {len(self.warnings)} budget warnings generated"
            )
        return "\n".join(lines)


# ============================================================================
# BUDGET ALLOCATION
# ============================================================================


def _allocate_request_budget(  # noqa: PLR0912, PLR0915
    max_input_allowed: int,
    system_instruction: str,
    game_state_json: str,
    core_memories: str,
    entity_tracking_estimate: int,
    story_context: list[dict[str, Any]],
    checkpoint_block: str | None = None,
    sequence_id_list: str | None = None,
) -> RequestBudgetResult:
    """
    Allocate tokens across request components with min/max enforcement.

    Strategy (Min-First, Fill-to-Max):
    1. MEASURE all component sizes (including checkpoint/sequence)
    2. ALLOCATE minimums to all components (68% total)
    3. FILL to maximums in priority order with remaining budget (32%)
    4. GIVE remaining budget to story context (can exceed 60%)
    5. COMPACT over-budget components (except system instruction unless >100k)

    Priority order for fill-to-max:
    1. system_instruction (10-40%, NO compaction unless >100k, warn if over 40%)
    2. game_state (5-20%, compact if over)
    3. core_memories (20-30%, compact if over)
    4. entity_tracking (3-15%, compact if over)
    5. checkpoint_block (0-2%, fixed size, no compaction)
    6. sequence_id (0-1%, fixed size, no compaction)
    7. story_context (30-60%, guaranteed min 30%, gets leftovers)

    Args:
        max_input_allowed: Total token budget for input (after output reserve)
        system_instruction: Full system instruction text
        game_state_json: Serialized game state JSON string
        core_memories: Core memories summary text
        entity_tracking_estimate: Pre-estimated entity tracking tokens
        story_context: List of story turn entries
        checkpoint_block: Optional checkpoint block text (quest/location/party state)
        sequence_id_list: Optional comma-separated sequence ID list

    Returns:
        RequestBudgetResult with allocations, warnings, and compacted content
    """
    # =========================================================================
    # STEP 1: MEASURE all component sizes
    # =========================================================================
    # FIX bead worktree_logs6-5c2: Measure all fields sent to LLM, not just text.
    # The stripped story context includes: text, actor, mode, sequence_id.
    # Previously only measured entry["text"], causing underestimation.
    essential_story_fields = {"text", "actor", "mode", "sequence_id"}
    story_text_parts = []
    for entry in story_context:
        if isinstance(entry, dict):
            for field in essential_story_fields:
                val = entry.get(field)
                if val is not None:
                    story_text_parts.append(str(val))
    story_text = "".join(story_text_parts)
    measurements = {
        "system_instruction": estimate_tokens(system_instruction),
        "game_state": estimate_tokens(game_state_json),
        "core_memories": estimate_tokens(core_memories),
        "entity_tracking": entity_tracking_estimate,
        "checkpoint_block": (
            estimate_tokens(checkpoint_block) if checkpoint_block is not None else 0
        ),
        "sequence_id": (
            estimate_tokens(sequence_id_list) if sequence_id_list is not None else 0
        ),
        "story_context": estimate_tokens(story_text),
    }

    total_measured = sum(measurements.values())
    logging_util.info(
        f"📊 MEASURED_SIZES: "
        f"system={measurements['system_instruction']:,}tk, "
        f"state={measurements['game_state']:,}tk, "
        f"memories={measurements['core_memories']:,}tk, "
        f"entities={measurements['entity_tracking']:,}tk, "
        f"checkpoint={measurements['checkpoint_block']:,}tk, "
        f"sequence={measurements['sequence_id']:,}tk, "
        f"story={measurements['story_context']:,}tk, "
        f"total={total_measured:,}tk (budget={max_input_allowed:,}tk)"
    )

    # =========================================================================
    # STEP 2: ALLOCATE MINIMUMS to all components
    # =========================================================================
    # Note: checkpoint_block and sequence_id are fixed-size components
    # They get their measured size as allocation (not percentage-based)
    min_allocations = {
        "system_instruction": int(max_input_allowed * BUDGET_SYSTEM_INSTRUCTION_MIN),
        "game_state": int(max_input_allowed * BUDGET_GAME_STATE_MIN),
        "core_memories": int(max_input_allowed * BUDGET_CORE_MEMORIES_MIN),
        "entity_tracking": int(max_input_allowed * BUDGET_ENTITY_TRACKING_MIN),
        "checkpoint_block": measurements["checkpoint_block"],  # Fixed size
        "sequence_id": measurements["sequence_id"],  # Fixed size
        "story_context": int(max_input_allowed * BUDGET_STORY_CONTEXT_MIN),
    }

    total_min = sum(min_allocations.values())

    degradation_warnings: list[dict[str, Any]] = []

    if total_min > max_input_allowed:
        # DEGRADATION: Preserve fixed-size components and reduce flexible budgets instead
        overage = total_min - max_input_allowed
        logging_util.error(
            f"📊 BUDGET_OVERFLOW: Component minimums ({total_min:,}tk) exceed budget ({max_input_allowed:,}tk). "
            f"Overage: {overage:,}tk. Attempting emergency degradation."
        )

        # TIER 1: Reduce story_context minimum (preferred - truncate story entries)
        story_absolute_min = int(max_input_allowed * BUDGET_STORY_CONTEXT_ABSOLUTE_MIN)
        if overage > 0:
            available_reduction = max(
                min_allocations["story_context"] - story_absolute_min, 0
            )
            story_reduction = min(available_reduction, overage)
            if story_reduction > 0:
                min_allocations["story_context"] -= story_reduction
                overage -= story_reduction
                # Only log and warn when actual reduction occurred
                original_story_min = int(max_input_allowed * BUDGET_STORY_CONTEXT_MIN)
                logging_util.error(
                    f"🔻 EMERGENCY: Reduced story_context minimum by {story_reduction:,}tk "
                    f"({original_story_min:,}tk → {min_allocations['story_context']:,}tk, "
                    f"floor={story_absolute_min:,}tk). "
                    f"Narrative quality will be degraded!"
                )
                degradation_warnings.append(
                    {
                        "component": "story_context",
                        "severity": "warning",
                        "measured_tokens": measurements["story_context"],
                        "allocated_tokens": min_allocations["story_context"],
                        "message": (
                            f"Story context minimum reduced by {story_reduction:,}tk "
                            f"to fit request budget."
                        ),
                        "ui_message": (
                            "⚠️ Story context was reduced to fit the model budget. "
                            "Longer story history may be truncated."
                        ),
                        "persist_key": "budget_warning_story_context_reduced",
                    }
                )

        # TIER 2: Reduce entity_tracking minimum (least critical after story)
        if overage > 0:
            entity_reduction = min(min_allocations["entity_tracking"], overage)
            min_allocations["entity_tracking"] -= entity_reduction
            overage -= entity_reduction
            logging_util.warning(
                f"🔻 DEGRADATION: Reduced entity_tracking by {entity_reduction:,}tk "
                f"({min_allocations['entity_tracking']:,}tk remaining)"
            )

        # TIER 3: Reduce core_memories minimum
        if overage > 0:
            memories_reduction = min(min_allocations["core_memories"], overage)
            min_allocations["core_memories"] -= memories_reduction
            overage -= memories_reduction
            logging_util.warning(
                f"🔻 DEGRADATION: Reduced core_memories by {memories_reduction:,}tk "
                f"({min_allocations['core_memories']:,}tk remaining)"
            )

        # TIER 4: Reduce game_state minimum
        if overage > 0:
            state_reduction = min(min_allocations["game_state"], overage)
            min_allocations["game_state"] -= state_reduction
            overage -= state_reduction
            logging_util.warning(
                f"🔻 DEGRADATION: Reduced game_state by {state_reduction:,}tk "
                f"({min_allocations['game_state']:,}tk remaining)"
            )

        # TIER 5: Reduce system_instruction minimum (last resort)
        if overage > 0:
            system_reduction = min(min_allocations["system_instruction"], overage)
            min_allocations["system_instruction"] -= system_reduction
            overage -= system_reduction
            logging_util.warning(
                f"🔻 DEGRADATION: Reduced system_instruction by {system_reduction:,}tk "
                f"({min_allocations['system_instruction']:,}tk remaining)"
            )

        # Recalculate total after degradation
        total_min = sum(min_allocations.values())

        # LAST RESORT: If still can't fit, raise ValueError
        if total_min > max_input_allowed:
            raise ValueError(
                f"Cannot allocate request even after emergency degradation. "
                f"Minimums ({total_min:,}tk) still exceed budget ({max_input_allowed:,}tk). "
                f"Request is fundamentally too large. Consider increasing model context window "
                f"or reducing campaign complexity."
            )

        logging_util.info(
            f"📊 DEGRADATION_COMPLETE: Total minimums reduced to {total_min:,}tk "
            f"(fits within {max_input_allowed:,}tk budget)"
        )

    remaining_budget = max_input_allowed - total_min
    min_pct = (total_min / max_input_allowed * 100) if max_input_allowed > 0 else 0.0
    remaining_pct = (
        (remaining_budget / max_input_allowed * 100) if max_input_allowed > 0 else 0.0
    )
    logging_util.info(
        f"📊 MIN_ALLOCATION: total_min={total_min:,}tk ({min_pct:.1f}%), "
        f"remaining={remaining_budget:,}tk ({remaining_pct:.1f}%)"
    )

    # =========================================================================
    # STEP 3: FILL TO MAXIMUMS in priority order
    # =========================================================================
    allocations = min_allocations.copy()

    # Priority order: (component, max_percentage)
    fill_order = [
        ("system_instruction", BUDGET_SYSTEM_INSTRUCTION_MAX),
        ("game_state", BUDGET_GAME_STATE_MAX),
        ("core_memories", BUDGET_CORE_MEMORIES_MAX),
        ("entity_tracking", BUDGET_ENTITY_TRACKING_MAX),
        ("story_context", BUDGET_STORY_CONTEXT_MAX),
    ]

    for component, max_pct in fill_order:
        max_tokens = int(max_input_allowed * max_pct)
        current_allocation = allocations[component]
        actual_size = measurements[component]

        # How much more can this component use?
        additional_space = max_tokens - current_allocation
        additional_needed = actual_size - current_allocation

        if additional_needed > 0 and additional_space > 0 and remaining_budget > 0:
            # Give this component more budget (up to its max and available budget)
            additional_grant = min(
                additional_needed, additional_space, remaining_budget
            )
            allocations[component] += additional_grant
            remaining_budget -= additional_grant

            logging_util.debug(
                f"📊 FILL_TO_MAX: {component} "
                f"{current_allocation:,}tk -> {allocations[component]:,}tk "
                f"(+{additional_grant:,}tk)"
            )

    # =========================================================================
    # STEP 4: GIVE REMAINING BUDGET TO STORY
    # =========================================================================
    if remaining_budget > 0:
        story_actual = measurements["story_context"]
        story_current = allocations["story_context"]

        if story_actual > story_current:
            # Story has more content than allocated - give it more budget
            additional_grant = min(story_actual - story_current, remaining_budget)
            allocations["story_context"] += additional_grant
            remaining_budget -= additional_grant

            logging_util.info(
                f"📊 BONUS_TO_STORY: story_context "
                f"{story_current:,}tk -> {allocations['story_context']:,}tk "
                f"(+{additional_grant:,}tk bonus)"
            )

    if remaining_budget > 0:
        unused_pct = (
            (remaining_budget / max_input_allowed * 100)
            if max_input_allowed > 0
            else 0.0
        )
        logging_util.debug(
            f"📊 UNUSED_BUDGET: {remaining_budget:,}tk ({unused_pct:.1f}%) unused"
        )

    # =========================================================================
    # STEP 5: COMPACT OVER-BUDGET COMPONENTS and generate warnings
    # =========================================================================
    warnings: list[dict[str, Any]] = list(degradation_warnings)
    compacted_content: dict[str, Any] = {}
    budget_allocations: dict[str, BudgetAllocation] = {}

    for component, allocated_tokens in allocations.items():
        actual_tokens = measurements[component]
        was_compacted = False
        compaction_ratio = 1.0

        if actual_tokens <= allocated_tokens:
            # Fits in budget - use as-is
            if component == "system_instruction":
                compacted_content[component] = system_instruction

                # Generate warning if system instruction exceeds 40% threshold (even if within budget)
                warn_threshold_tokens = int(
                    max_input_allowed * BUDGET_SYSTEM_INSTRUCTION_WARN
                )
                if actual_tokens > warn_threshold_tokens:
                    pct = (
                        (actual_tokens / max_input_allowed * 100)
                        if max_input_allowed > 0
                        else 0.0
                    )
                    warnings.append(
                        {
                            "component": "system_instruction",
                            "severity": "warning",
                            "measured_tokens": actual_tokens,
                            "allocated_tokens": allocated_tokens,
                            "message": (
                                f"System instruction ({actual_tokens:,}tk) exceeds "
                                f"recommended threshold ({warn_threshold_tokens:,}tk, {BUDGET_SYSTEM_INSTRUCTION_WARN * 100:.0f}%)."
                            ),
                            "ui_message": (
                                f"⚠️ System prompts are using {actual_tokens:,} tokens "
                                f"({pct:.1f}% of budget). "
                                f"Consider simplifying campaign settings or world lore to improve "
                                f"narrative quality."
                            ),
                            "persist_key": "budget_warning_system_instruction",
                        }
                    )
                    logging_util.warning(
                        f"⚠️ SYSTEM_INSTRUCTION_OVER_WARN_THRESHOLD: {actual_tokens:,}tk > "
                        f"{warn_threshold_tokens:,}tk ({BUDGET_SYSTEM_INSTRUCTION_WARN * 100:.0f}%). "
                        f"UI warning generated."
                    )
            elif component == "game_state":
                compacted_content[component] = game_state_json
            elif component == "core_memories":
                compacted_content[component] = core_memories
            elif component == "entity_tracking":
                compacted_content[component] = entity_tracking_estimate
            elif component == "checkpoint_block":
                compacted_content[component] = checkpoint_block or ""
            elif component == "sequence_id":
                compacted_content[component] = sequence_id_list or ""
            # story_context: No compaction here - handled by _truncate_context() in llm_service
        else:
            # Over budget - compact or warn
            overage = actual_tokens - allocated_tokens

            if component == "system_instruction":
                # FIX bead worktree_logs6-1mh: Always compact when over budget,
                # not just when over 100k emergency threshold. This ensures total
                # input stays within max_input_allowed and prevents provider errors.
                compacted_text = _compact_system_instruction(
                    system_instruction, allocated_tokens
                )
                compacted_content[component] = compacted_text
                was_compacted = True
                compaction_ratio = allocated_tokens / actual_tokens

                # Determine severity based on whether it exceeded emergency threshold
                is_emergency = actual_tokens > SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD
                severity = "critical" if is_emergency else "warning"
                persist_key = (
                    "budget_warning_system_instruction_emergency"
                    if is_emergency
                    else "budget_warning_system_instruction"
                )

                pct = (
                    (actual_tokens / max_input_allowed * 100)
                    if max_input_allowed > 0
                    else 0.0
                )

                if is_emergency:
                    logging_util.warning(
                        f"🔨 SYSTEM_INSTRUCTION_COMPACTED: {actual_tokens:,}tk -> "
                        f"{allocated_tokens:,}tk (exceeded {SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD:,}tk threshold)"
                    )
                    ui_message = (
                        f"⚠️ System prompts were extremely large ({actual_tokens:,} tokens, "
                        f"{pct:.1f}% of budget) and required emergency compaction. "
                        f"Campaign settings or world lore should be significantly simplified "
                        f"to improve narrative quality and prevent content truncation."
                    )
                else:
                    logging_util.warning(
                        f"🔨 SYSTEM_INSTRUCTION_COMPACTED: {actual_tokens:,}tk -> "
                        f"{allocated_tokens:,}tk (exceeded budget, compacting to fit)"
                    )
                    ui_message = (
                        f"⚠️ System prompts were large ({actual_tokens:,} tokens, "
                        f"{pct:.1f}% of budget) and were compacted to fit. "
                        f"Consider simplifying campaign settings or world lore to improve "
                        f"narrative quality."
                    )

                warnings.append(
                    {
                        "component": "system_instruction",
                        "severity": severity,
                        "measured_tokens": actual_tokens,
                        "allocated_tokens": allocated_tokens,
                        "message": (
                            f"System instruction ({actual_tokens:,}tk) exceeded "
                            f"allocated budget ({allocated_tokens:,}tk) by {overage:,}tk. "
                            f"Compaction applied."
                        ),
                        "ui_message": ui_message,
                        "persist_key": persist_key,
                    }
                )

            elif component == "game_state":
                compacted_text = _compact_game_state(game_state_json, allocated_tokens)
                compacted_content[component] = compacted_text
                was_compacted = True
                compaction_ratio = allocated_tokens / actual_tokens
                logging_util.warning(
                    f"🔨 GAME_STATE_COMPACTED: {actual_tokens:,}tk -> {allocated_tokens:,}tk"
                )

            elif component == "core_memories":
                compacted_text = _compact_core_memories(core_memories, allocated_tokens)
                compacted_content[component] = compacted_text
                was_compacted = True
                compaction_ratio = allocated_tokens / actual_tokens
                logging_util.warning(
                    f"🔨 CORE_MEMORIES_COMPACTED: {actual_tokens:,}tk -> {allocated_tokens:,}tk"
                )

            elif component == "entity_tracking":
                # Entity tracking uses existing tiering - just cap the estimate
                compacted_content[component] = allocated_tokens
                was_compacted = True
                compaction_ratio = allocated_tokens / actual_tokens
                logging_util.warning(
                    f"🔨 ENTITY_TRACKING_CAPPED: {actual_tokens:,}tk -> {allocated_tokens:,}tk"
                )

            elif component == "story_context":
                # Story context compaction handled by _truncate_context() in llm_service.py
                # Here we just track if compaction would be needed for logging/warnings
                was_compacted = actual_tokens > allocated_tokens
                if was_compacted:
                    compaction_ratio = allocated_tokens / actual_tokens
                    reduction_tokens = actual_tokens - allocated_tokens

                    # Log error about story context reduction
                    logging_util.error(
                        f"📊 STORY_CONTEXT_COMPACTED: {actual_tokens:,}tk -> "
                        f"{allocated_tokens:,}tk (reduced by {reduction_tokens:,}tk)"
                    )

                    # Generate warning for UI
                    pct = (
                        (actual_tokens / max_input_allowed * 100)
                        if max_input_allowed > 0
                        else 0.0
                    )
                    warnings.append(
                        {
                            "component": "story_context",
                            "severity": "warning",
                            "measured_tokens": actual_tokens,
                            "allocated_tokens": allocated_tokens,
                            "message": (
                                f"Story context ({actual_tokens:,}tk) exceeded "
                                f"allocated budget ({allocated_tokens:,}tk). "
                                f"Reduced by {reduction_tokens:,}tk."
                            ),
                            "ui_message": (
                                f"⚠️ Story context was reduced by {reduction_tokens:,} tokens "
                                f"to fit the model budget. Older story history may be truncated."
                            ),
                            "persist_key": "budget_warning_story_context_compacted",
                        }
                    )

        budget_allocations[component] = BudgetAllocation(
            component=component,
            measured_tokens=actual_tokens,
            allocated_tokens=allocated_tokens,
            was_compacted=was_compacted,
            compaction_ratio=compaction_ratio,
        )

    result = RequestBudgetResult(
        max_input_allowed=max_input_allowed,
        allocations=budget_allocations,
        warnings=warnings,
        compacted_content=compacted_content,
    )

    logging_util.info(result.log_summary())
    return result


# ============================================================================
# COMPONENT-SPECIFIC COMPACTION FUNCTIONS
# ============================================================================


def _compact_system_instruction(system_instruction: str, max_tokens: int) -> str:
    """
    Emergency compaction for oversized system instructions (>100k tokens).

    Strategy: Preserve critical structure, truncate verbose sections.
    Only called when system_instruction > SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD.

    Args:
        system_instruction: Full system instruction text
        max_tokens: Target token budget

    Returns:
        Compacted system instruction text
    """
    # Convert token budget to character budget (4 chars per token)
    max_chars = max_tokens * 4

    if len(system_instruction) <= max_chars:
        return system_instruction

    # For emergency compaction, preserve beginning and end
    # Beginning has critical rules, end has recent context
    truncation_marker = (
        "\n\n[...SYSTEM INSTRUCTION TRUNCATED - CAMPAIGN SETTINGS TOO LARGE...]\n\n"
    )
    marker_len = len(truncation_marker)
    available = max_chars - marker_len
    if available <= 0:
        return truncation_marker[:max_chars]

    preserve_start = int(available * 0.6)  # 60% from start
    preserve_end = available - preserve_start  # remainder to end

    compacted = (
        system_instruction[:preserve_start]
        + truncation_marker
        + system_instruction[-preserve_end:]
    )

    logging_util.warning(
        f"🔨 SYSTEM_INSTRUCTION_EMERGENCY_COMPACT: "
        f"{len(system_instruction):,} chars -> {len(compacted):,} chars"
    )

    return compacted


def _compact_game_state(game_state_json: str, max_tokens: int) -> str:  # noqa: PLR0912
    """
    Compact game state JSON by removing low-priority fields.

    Priority tiers:
    1. CRITICAL: HP, location, combat state (always included)
    2. HIGH: Inventory, active quests, abilities (include if space)
    3. MEDIUM: World data, reputation (summarize if needed)
    4. LOW: Completed quests, history (drop first)

    Args:
        game_state_json: Full game state JSON string
        max_tokens: Target token budget

    Returns:
        Compacted game state JSON string
    """
    current_tokens = estimate_tokens(game_state_json)
    if current_tokens <= max_tokens:
        return game_state_json

    try:
        game_state = json.loads(game_state_json)
    except json.JSONDecodeError:
        # Can't parse - skip compaction and return original JSON
        # (truncating would produce invalid JSON which fails downstream parsing)
        logging_util.warning(
            "Game state JSON could not be parsed; skipping compaction and returning original."
        )
        return game_state_json
    if not isinstance(game_state, dict):
        # Not a dict - skip compaction and return original JSON
        logging_util.warning(
            f"Game state is not a dict (type={type(game_state).__name__}); "
            "skipping compaction and returning original."
        )
        return game_state_json

    compacted: dict[str, Any] = {}
    max_chars = max_tokens * 4

    # Preserve nested critical fields that are not top-level in GameState.
    nested_world_data = game_state.get("world_data")
    if isinstance(nested_world_data, dict):
        world_compact: dict[str, Any] = {}
        if "current_location_name" in nested_world_data:
            world_compact["current_location_name"] = nested_world_data.get(
                "current_location_name"
            )
        if "current_location" in nested_world_data:
            world_compact["current_location"] = nested_world_data.get(
                "current_location"
            )
        if (
            "current_location_name" not in world_compact
            and "location" in nested_world_data
        ):
            world_compact["current_location_name"] = nested_world_data.get("location")
        if world_compact:
            compacted["world_data"] = world_compact

    nested_combat_state = game_state.get("combat_state")
    if isinstance(nested_combat_state, dict):
        compacted["combat_state"] = nested_combat_state

    nested_player_data = game_state.get("player_character_data")
    if isinstance(nested_player_data, dict):
        compacted["player_character_data"] = nested_player_data

    # Always include CRITICAL fields
    for field in GAME_STATE_PRIORITY_CRITICAL:
        if field in game_state:
            compacted[field] = game_state[field]

    # Try adding HIGH priority fields
    for field in GAME_STATE_PRIORITY_HIGH:
        if field in game_state:
            test_compacted = compacted.copy()
            test_compacted[field] = game_state[field]
            test_json = json.dumps(test_compacted, separators=(",", ":"))
            if len(test_json) <= max_chars:
                compacted[field] = game_state[field]

    # Try adding MEDIUM priority fields (may truncate)
    for field in GAME_STATE_PRIORITY_MEDIUM:
        if field in game_state:
            test_compacted = compacted.copy()
            test_compacted[field] = game_state[field]
            test_json = json.dumps(test_compacted, separators=(",", ":"))
            if len(test_json) <= max_chars:
                compacted[field] = game_state[field]

    # LOW priority fields are skipped in compaction

    # Final serialization
    compacted_json = json.dumps(compacted, separators=(",", ":"))

    # If compaction still exceeds budget, return the compacted JSON anyway.
    # This is safer than returning the original (larger) payload.
    if len(compacted_json) > max_chars:
        logging_util.warning(
            f"Compacted game_state ({len(compacted_json)} chars) exceeds budget "
            f"({max_chars} chars). Returning compacted version (still over budget). "
            "Consider increasing budget or reducing game state complexity."
        )
        return compacted_json

    return compacted_json


def _compact_core_memories(core_memories: str, max_tokens: int) -> str:
    """
    Compact core memories by prioritizing recent and CRITICAL entries.

    Strategy:
    1. Keep all CRITICAL memories (must-remember facts)
    2. Keep recent memories (last 5-10 entries) verbatim
    3. Summarize or drop older memories if over budget

    Args:
        core_memories: Full core memories text
        max_tokens: Target token budget

    Returns:
        Compacted core memories text
    """
    current_tokens = estimate_tokens(core_memories)
    if current_tokens <= max_tokens:
        return core_memories

    max_chars = max_tokens * 4

    # Split into individual memory entries (assume newline-separated)
    memory_lines = [line for line in core_memories.split("\n") if line.strip()]

    if not memory_lines:
        return ""

    # Separate CRITICAL memories from others
    critical_memories = [line for line in memory_lines if "CRITICAL" in line.upper()]
    recent_memories = memory_lines[-5:]  # Last 5 entries

    # Build compacted memories
    compacted_parts = []

    # Always include CRITICAL memories
    for critical in critical_memories:
        if critical not in recent_memories:  # Avoid duplicates
            compacted_parts.append(critical)

    # Add recent memories
    compacted_parts.extend(recent_memories)

    # Join and check size
    compacted = "\n".join(compacted_parts)

    # If still over budget, further truncate recent memories
    if len(compacted) > max_chars:
        # Keep only last 3 recent + critical
        # FIX Issue 5: Avoid duplicates - filter out critical memories already in last 3
        last_3 = memory_lines[-3:]
        compacted_parts = critical_memories + [
            m for m in last_3 if m not in critical_memories
        ]
        compacted = "\n".join(compacted_parts)

    # Last resort: hard truncate
    if len(compacted) > max_chars:
        compacted = compacted[:max_chars]

    return compacted


# ============================================================================
# WARNING PERSISTENCE FUNCTIONS
# ============================================================================


def _filter_persisted_warnings(
    warnings: list[dict[str, Any]],
    game_state: Any,
) -> tuple[list[dict[str, Any]], list[str]]:
    """
    Filter budget warnings, suppressing those already shown this session.

    Warnings with a `persist_key` will only be shown once per session.
    After the first display, the persist_key is stored in game_state
    and subsequent warnings with the same key are suppressed.

    Args:
        warnings: List of warning dicts from _allocate_request_budget()
        game_state: GameState object (for reading/writing persisted keys)

    Returns:
        Tuple of (warnings_to_show, new_persist_keys_to_save)
        - warnings_to_show: Filtered list for UI display
        - new_persist_keys_to_save: Keys to add to game_state after response
    """
    if not warnings:
        return [], []

    # Get existing persisted warnings from game_state
    persisted_keys: set[str] = set()
    custom_state = getattr(game_state, "custom_campaign_state", None)
    if isinstance(custom_state, dict):
        budget_warnings_shown = custom_state.get("budget_warnings_shown", [])
        if isinstance(budget_warnings_shown, list):
            persisted_keys = set(budget_warnings_shown)

    # Filter warnings
    warnings_to_show: list[dict[str, Any]] = []
    new_persist_keys: list[str] = []

    for warning in warnings:
        persist_key = warning.get("persist_key")
        if persist_key:
            if persist_key in persisted_keys:
                # Already shown - skip
                logging_util.debug(
                    f"📊 BUDGET_WARNING_SUPPRESSED: {persist_key} (already shown)"
                )
                continue
            # New warning - show and remember
            new_persist_keys.append(persist_key)
            warnings_to_show.append(warning)
        else:
            # No persist_key - always show
            warnings_to_show.append(warning)

    return warnings_to_show, new_persist_keys


def _save_warning_persist_keys(
    game_state: Any,
    new_keys: list[str],
) -> None:
    """
    Save new warning persist keys to game_state for future suppression.

    Args:
        game_state: GameState object to update
        new_keys: List of persist_key values to add
    """
    if not new_keys:
        return

    if not hasattr(game_state, "custom_campaign_state"):
        return

    if not isinstance(game_state.custom_campaign_state, dict):
        game_state.custom_campaign_state = {}

    existing = game_state.custom_campaign_state.get("budget_warnings_shown", [])
    if not isinstance(existing, list):
        existing = []

    # Add new keys, avoiding duplicates
    updated = list(set(existing) | set(new_keys))
    game_state.custom_campaign_state["budget_warnings_shown"] = updated

    logging_util.info(
        f"📊 BUDGET_WARNINGS_PERSISTED: {new_keys} (total: {len(updated)})"
    )
