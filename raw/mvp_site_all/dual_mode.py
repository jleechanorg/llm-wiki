"""Dual-Mode Campaign System: D&D + Faction Integration.

This module implements Phase 1 of the dual-mode system:
- Time tracking (personal adventures vs strategic turns)
- Mode switching (/faction, /adventure)
- Attention triggers (crises, reminders)
- Reminder injection for LLM context

Time Scales:
- Personal Mode: Minutes/hours (combat, exploration, dialogue)
- Strategic Mode: Days/weeks (1 turn = 7 in-game days)

See beads worktree_world_faction-hfl for full design.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Any


class CampaignMode(Enum):
    """Current campaign focus mode."""

    ADVENTURE = "adventure"
    FACTION = "faction"


class TriggerUrgency(Enum):
    """Urgency level for attention triggers."""

    LOW = "low"  # Can be ignored safely
    MEDIUM = "medium"  # Should address soon
    HIGH = "high"  # Needs attention this session
    CRITICAL = "critical"  # Interrupts adventure immediately


class TriggerType(Enum):
    """Types of attention triggers."""

    # Strategic -> Personal (crisis events)
    SIEGE = "siege"
    ASSASSINATION = "assassination"
    ENEMY_CHALLENGE = "enemy_challenge"
    DISCOVERY = "discovery"

    # Personal -> Strategic (neglect warnings)
    NEGLECT_REMINDER = "neglect_reminder"
    NEGLECT_WARNING = "neglect_warning"
    ENEMY_APPROACHING = "enemy_approaching"
    TREASURY_CRITICAL = "treasury_critical"
    MORALE_CRITICAL = "morale_critical"

    # Opportunities
    ALLIANCE_OFFER = "alliance_offer"
    TRADE_PROPOSAL = "trade_proposal"
    BUILDING_COMPLETE = "building_complete"
    RESEARCH_COMPLETE = "research_complete"


@dataclass
class Trigger:
    """An attention trigger requiring player response."""

    id: str
    type: TriggerType
    urgency: TriggerUrgency
    message: str
    created_turn: int
    expires_turn: int | None = None
    data: dict[str, Any] = field(default_factory=dict)

    def is_expired(self, current_turn: int) -> bool:
        """Check if trigger has expired."""
        if self.expires_turn is None:
            return False
        return current_turn > self.expires_turn

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for state storage."""
        return {
            "id": self.id,
            "type": self.type.value,
            "urgency": self.urgency.value,
            "message": self.message,
            "created_turn": self.created_turn,
            "expires_turn": self.expires_turn,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Trigger:
        """Create from dictionary."""
        return cls(
            id=data["id"],
            type=TriggerType(data["type"]),
            urgency=TriggerUrgency(data["urgency"]),
            message=data["message"],
            created_turn=data["created_turn"],
            expires_turn=data.get("expires_turn"),
            data=data.get("data", {}),
        )


@dataclass
class DualModeState:
    """State for dual-mode campaign tracking."""

    current_mode: CampaignMode = CampaignMode.ADVENTURE
    strategic_turn: int = 1
    last_faction_order_turn: int = 1
    accumulated_personal_time: timedelta = field(default_factory=lambda: timedelta())
    pending_triggers: list[Trigger] = field(default_factory=list)
    dismissed_trigger_ids: set[str] = field(default_factory=set)
    adventure_checkpoint: dict[str, Any] = field(default_factory=dict)

    # Configuration
    neglect_reminder_threshold: int = 3  # Turns before reminder
    neglect_warning_threshold: int = 5  # Turns before warning
    turn_duration_days: int = 7  # Days per strategic turn

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for state storage."""
        return {
            "current_mode": self.current_mode.value,
            "strategic_turn": self.strategic_turn,
            "last_faction_order_turn": self.last_faction_order_turn,
            "accumulated_personal_time_seconds": self.accumulated_personal_time.total_seconds(),
            "pending_triggers": [t.to_dict() for t in self.pending_triggers],
            "dismissed_trigger_ids": list(self.dismissed_trigger_ids),
            "adventure_checkpoint": self.adventure_checkpoint,
            "neglect_reminder_threshold": self.neglect_reminder_threshold,
            "neglect_warning_threshold": self.neglect_warning_threshold,
            "turn_duration_days": self.turn_duration_days,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DualModeState:
        """Create from dictionary."""
        state = cls(
            current_mode=CampaignMode(data.get("current_mode", "adventure")),
            strategic_turn=data.get("strategic_turn", 1),
            last_faction_order_turn=data.get("last_faction_order_turn", 1),
            accumulated_personal_time=timedelta(
                seconds=data.get("accumulated_personal_time_seconds", 0)
            ),
            dismissed_trigger_ids=set(data.get("dismissed_trigger_ids", [])),
            adventure_checkpoint=data.get("adventure_checkpoint", {}),
            neglect_reminder_threshold=data.get("neglect_reminder_threshold", 3),
            neglect_warning_threshold=data.get("neglect_warning_threshold", 5),
            turn_duration_days=data.get("turn_duration_days", 7),
        )

        # Restore triggers
        for trigger_data in data.get("pending_triggers", []):
            state.pending_triggers.append(Trigger.from_dict(trigger_data))

        return state


class DualModeManager:
    """Manages dual-mode campaign state and triggers."""

    def __init__(self, state: DualModeState | None = None):
        self.state = state or DualModeState()

    @classmethod
    def from_game_state(cls, game_state: dict[str, Any]) -> DualModeManager:
        """Create manager from game state."""
        dual_mode_data = game_state.get("dual_mode", {})
        if dual_mode_data:
            state = DualModeState.from_dict(dual_mode_data)
        else:
            state = DualModeState()
        return cls(state)

    def to_game_state(self) -> dict[str, Any]:
        """Export state for game_state storage."""
        return {"dual_mode": self.state.to_dict()}

    # === Mode Switching ===

    def switch_to_faction(self) -> str:
        """Switch to faction management mode."""
        if self.state.current_mode == CampaignMode.FACTION:
            return "Already in faction management mode."

        # Save adventure checkpoint
        self.state.adventure_checkpoint = {
            "switched_at_turn": self.state.strategic_turn,
            "mode": "faction",
        }

        self.state.current_mode = CampaignMode.FACTION
        return f"Switched to faction management. Strategic Turn: {self.state.strategic_turn}"

    def switch_to_adventure(self) -> str:
        """Switch to personal adventure mode."""
        if self.state.current_mode == CampaignMode.ADVENTURE:
            return "Already in adventure mode."

        self.state.current_mode = CampaignMode.ADVENTURE
        return "Switched to adventure mode. Your realm continues in the background."

    # === Time Management ===

    def add_personal_time(self, hours: float) -> bool:
        """Add personal adventure time. Returns True if strategic turn advances."""
        self.state.accumulated_personal_time += timedelta(hours=hours)

        # Check if we should advance strategic turn
        days_accumulated = self.state.accumulated_personal_time.total_seconds() / 86400
        if days_accumulated >= self.state.turn_duration_days:
            self.state.accumulated_personal_time -= timedelta(
                days=self.state.turn_duration_days
            )
            self.advance_strategic_turn()
            return True

        return False

    def advance_strategic_turn(self) -> int:
        """Advance the strategic turn counter."""
        self.state.strategic_turn += 1

        # Check for neglect triggers
        self._evaluate_neglect_triggers()

        # Clean up expired triggers
        self._cleanup_expired_triggers()

        return self.state.strategic_turn

    def record_faction_action(self) -> None:
        """Record that player took a faction action this turn."""
        self.state.last_faction_order_turn = self.state.strategic_turn

        # Clear neglect triggers
        self.state.pending_triggers = [
            t
            for t in self.state.pending_triggers
            if t.type not in (TriggerType.NEGLECT_REMINDER, TriggerType.NEGLECT_WARNING)
        ]

    def long_rest(self) -> dict[str, Any]:
        """Process a long rest (8 hours). Always advances turn."""
        # Long rest = 8 hours = always check for turn advance
        turn_advanced = self.add_personal_time(8.0)

        # Force turn advance on long rest if not already
        if not turn_advanced:
            self.advance_strategic_turn()
            turn_advanced = True

        return {
            "turn_advanced": turn_advanced,
            "new_turn": self.state.strategic_turn,
            "pending_triggers": len(self.state.pending_triggers),
        }

    # === Trigger Management ===

    def add_trigger(
        self,
        trigger_type: TriggerType,
        urgency: TriggerUrgency,
        message: str,
        expires_in_turns: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Trigger:
        """Add a new attention trigger."""
        trigger_id = f"{trigger_type.value}_{uuid.uuid4().hex[:8]}"

        expires_turn = None
        if expires_in_turns is not None:
            expires_turn = self.state.strategic_turn + expires_in_turns

        trigger = Trigger(
            id=trigger_id,
            type=trigger_type,
            urgency=urgency,
            message=message,
            created_turn=self.state.strategic_turn,
            expires_turn=expires_turn,
            data=data or {},
        )

        self.state.pending_triggers.append(trigger)
        return trigger

    def dismiss_trigger(self, trigger_id: str) -> bool:
        """Dismiss a trigger so it won't remind again."""
        for trigger in self.state.pending_triggers:
            if trigger.id == trigger_id:
                self.state.pending_triggers.remove(trigger)
                self.state.dismissed_trigger_ids.add(trigger_id)
                return True
        return False

    def get_triggers_by_urgency(
        self, min_urgency: TriggerUrgency = TriggerUrgency.LOW
    ) -> list[Trigger]:
        """Get triggers at or above a minimum urgency level."""
        urgency_order = [
            TriggerUrgency.LOW,
            TriggerUrgency.MEDIUM,
            TriggerUrgency.HIGH,
            TriggerUrgency.CRITICAL,
        ]
        min_index = urgency_order.index(min_urgency)

        return [
            t
            for t in self.state.pending_triggers
            if urgency_order.index(t.urgency) >= min_index
        ]

    def has_critical_triggers(self) -> bool:
        """Check if any critical triggers are pending."""
        return any(
            t.urgency == TriggerUrgency.CRITICAL for t in self.state.pending_triggers
        )

    def _evaluate_neglect_triggers(self) -> None:
        """Check for faction neglect and add triggers if needed."""
        turns_since_action = (
            self.state.strategic_turn - self.state.last_faction_order_turn
        )

        # Only add if not already present
        existing_types = {t.type for t in self.state.pending_triggers}

        if turns_since_action >= self.state.neglect_warning_threshold:
            if TriggerType.NEGLECT_WARNING not in existing_types:
                self.add_trigger(
                    TriggerType.NEGLECT_WARNING,
                    TriggerUrgency.HIGH,
                    f"Your realm has been without orders for {turns_since_action} turns. "
                    "Morale is dropping and your council is concerned.",
                )
        elif turns_since_action >= self.state.neglect_reminder_threshold:
            if TriggerType.NEGLECT_REMINDER not in existing_types:
                self.add_trigger(
                    TriggerType.NEGLECT_REMINDER,
                    TriggerUrgency.MEDIUM,
                    f"Your steward requests guidance. {turns_since_action} turns since last orders.",
                )

    def _cleanup_expired_triggers(self) -> None:
        """Remove expired triggers."""
        self.state.pending_triggers = [
            t
            for t in self.state.pending_triggers
            if not t.is_expired(self.state.strategic_turn)
        ]

    # === LLM Context Building ===

    def build_reminder_block(self) -> str:
        """Build reminder text for LLM context injection."""
        if not self.state.pending_triggers:
            return ""

        # Get critical triggers first
        critical = self.get_triggers_by_urgency(TriggerUrgency.CRITICAL)
        if critical:
            t = critical[0]
            return (
                f"\n⚠️ URGENT FACTION ALERT ⚠️\n"
                f"{t.message}\n"
                f"[Type /faction to respond, or continue adventuring]\n"
            )

        # High urgency
        high = self.get_triggers_by_urgency(TriggerUrgency.HIGH)
        if high:
            return f"\n(Your steward has urgent news: {high[0].message})\n"

        # Medium/low - subtle narrative hint
        if self.state.pending_triggers:
            return "\n(A messenger awaits with news from your realm...)\n"

        return ""

    def build_status_display(self) -> str:
        """Build status display for /status command."""
        mode_icon = "🎭" if self.state.current_mode == CampaignMode.ADVENTURE else "🏰"
        mode_name = self.state.current_mode.value.capitalize()

        turns_since = self.state.strategic_turn - self.state.last_faction_order_turn

        lines = [
            "┌─ REALM STATUS ─────────────────────────────────┐",
            f"│ Turn {self.state.strategic_turn} | {turns_since} turns since last faction orders",
            "│",
        ]

        # Attention items
        if self.state.pending_triggers:
            critical = len(
                [
                    t
                    for t in self.state.pending_triggers
                    if t.urgency == TriggerUrgency.CRITICAL
                ]
            )
            high = len(
                [
                    t
                    for t in self.state.pending_triggers
                    if t.urgency == TriggerUrgency.HIGH
                ]
            )
            other = len(self.state.pending_triggers) - critical - high

            lines.append(
                f"│ ⚠️ ATTENTION ({critical} critical, {high} high, {other} other):"
            )

            for trigger in sorted(
                self.state.pending_triggers,
                key=lambda t: ["low", "medium", "high", "critical"].index(
                    t.urgency.value
                ),
                reverse=True,
            )[:3]:  # Show top 3
                icon = {"critical": "🔴", "high": "🟡", "medium": "🟢", "low": "⚪"}[
                    trigger.urgency.value
                ]
                lines.append(f"│   {icon} {trigger.message[:45]}...")

            lines.append("│")

        lines.append(f"│ {mode_icon} Currently: {mode_name} mode")
        lines.append("└────────────────────────────────────────────────┘")

        return "\n".join(lines)

    # === Faction State Evaluation ===

    def evaluate_faction_state(self, faction_state: dict[str, Any]) -> list[Trigger]:
        """Evaluate faction state and generate triggers for crises."""
        new_triggers: list[Trigger] = []

        # Treasury critical
        gold = faction_state.get("gold_pieces", 0)
        if gold < 5000:
            existing = any(
                t.type == TriggerType.TREASURY_CRITICAL
                for t in self.state.pending_triggers
            )
            if not existing:
                trigger = self.add_trigger(
                    TriggerType.TREASURY_CRITICAL,
                    TriggerUrgency.HIGH,
                    f"Treasury critical: only {gold} gold remains. Economic crisis brewing.",
                )
                new_triggers.append(trigger)

        # More evaluations can be added here...

        return new_triggers
