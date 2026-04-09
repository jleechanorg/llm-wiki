# AUTO-GENERATED from game_state.schema.json
# DO NOT EDIT MANUALLY - regenerate with scripts/generate_typeddict.py

from typing import Any, NotRequired, Required, TypedDict

class StatsDict(TypedDict, total=False):
    """Allows additional properties for legacy/test data compatibility"""
    charisma: NotRequired[int]  # Force of personality, bard/warlock/sorcerer spellcasting ...
    constitution: NotRequired[int]  # Endurance, hit points, concentration saves (unbounded for...
    dexterity: NotRequired[int]  # Agility, ranged attacks, AC, initiative (unbounded for ep...
    intelligence: NotRequired[int]  # Reasoning, memory, wizard spellcasting (unbounded for epi...
    strength: NotRequired[int]  # Physical power, melee attack/damage modifier (unbounded f...
    wisdom: NotRequired[int]  # Perception, insight, cleric/druid spellcasting (unbounded...

class HealthStatusDict(TypedDict, total=False):
    """Character health tracking including temporary HP and conditions"""
    conditions: NotRequired[list[str]]  # Active conditions (poisoned, stunned, etc.)
    death_saves: NotRequired[dict[str, Any]]  # Death saving throw tracking when at 0 HP
    hp: Required[int]  # Current hit points
    hp_max: Required[int]  # Maximum hit points
    temp_hp: NotRequired[int]  # Temporary hit points (absorbed first)

EntityTypeDict = str

EntityStatusDict = Any

VisibilityDict = str

class LocationDict(TypedDict, total=False):
    """A game location that can contain entities"""
    aliases: NotRequired[list[str]]
    connected_locations: NotRequired[list[str]]  # Entity IDs of connected locations
    description: NotRequired[str]  # Narrative description of this location
    display_name: Required[str]
    entities_present: NotRequired[list[str]]  # Entity IDs of entities currently here
    entity_id: Required[str]
    entity_type: NotRequired[Any]  # Always 'loc' for locations
    environmental_effects: NotRequired[list[str]]  # Active environmental effects (darkness, difficult terrain)

class FactionUnitsDict(TypedDict, total=False):
    """Military units in the faction minigame"""
    elite_avg_level: NotRequired[float]  # Average level of elite unit adventurers
    elites: NotRequired[int]  # Elite units: 3x FP each, require level 6+ adventurers
    soldiers: NotRequired[int]  # Basic units: 1x Faction Power each
    spies: NotRequired[int]  # Intel units: 0.5x FP each, enable intel operations

class FactionResourcesDict(TypedDict, total=False):
    """Resources tracked in faction minigame"""
    gold: NotRequired[int]  # Gold pieces for recruitment and operations
    territory: NotRequired[int]  # Controlled territory points

class CompanionArcDict(TypedDict, total=False):
    arc_type: NotRequired[str]
    callbacks: NotRequired[list[dict[str, Any]]]
    history: NotRequired[list[Any]]
    phase: NotRequired[str]

class GodModeDirectiveDict(TypedDict, total=False):
    """A player-defined rule for god mode (narrative control)"""
    added: NotRequired[str]  # ISO timestamp when rule was added
    rule: Required[str]  # The directive text

class ArcMilestoneDict(TypedDict, total=False):
    """Tracks completion of a narrative arc milestone"""
    completed_at: NotRequired[str]  # When this milestone was achieved
    notes: NotRequired[str]  # Optional notes about how it was achieved
    phase: NotRequired[str]
    progress: NotRequired[int]  # Progress percentage (0-100)
    status: Required[str]
    updated_at: NotRequired[str]  # ISO timestamp of last update

class ChapterDataDict(TypedDict, total=False):
    """Campaign chapter/progression tracking"""
    bonus_content: NotRequired[list[str]]  # Unlocked bonus content identifiers
    chapter_metadata: NotRequired[dict[str, Any]]  # Per-chapter metadata (title, themes, etc.)
    current_chapter: NotRequired[int]  # Current chapter number

CampaignTierDict = str

class CombatantStateDict(TypedDict, total=False):
    """Per-combatant state during combat"""
    concentration_spell: NotRequired[str]  # Name of spell being concentrated on, if any
    has_acted: NotRequired[bool]  # Whether this combatant has acted this round
    hp_current: NotRequired[int]  # Current hit points
    hp_max: NotRequired[int]  # Maximum hit points
    reactions_used: NotRequired[int]  # Reactions used this round
    role: NotRequired[str]  # Specific role or description
    status: NotRequired[list[str]]  # Active conditions/status effects
    type: NotRequired[str]  # Role in combat (enemy, ally, companion, pc, unknown)

class LegacyInitiativeEntryDict(TypedDict, total=False):
    """Legacy initiative entry shape (warn-only)."""
    initiative: NotRequired[int]
    name: NotRequired[str]
    type: NotRequired[str]

class EncounterStateDict(TypedDict, total=False):
    """Non-combat encounter tracking state"""
    encounter_active: NotRequired[bool]
    encounter_completed: NotRequired[bool]
    encounter_summary: NotRequired[None | dict[str, Any]]
    encounter_type: NotRequired[str]
    rewards_processed: NotRequired[bool]

class RewardsPendingDict(TypedDict, total=False):
    """Pending rewards awaiting distribution"""
    gold: NotRequired[int]
    items: NotRequired[list[dict[str, Any]]]
    level_up_available: NotRequired[bool]
    new_level: NotRequired[int]
    processed: NotRequired[bool]
    source: NotRequired[str]
    source_id: NotRequired[str]
    xp: NotRequired[int]

class WorldEventDict(TypedDict, total=False):
    action: NotRequired[str]
    actor: NotRequired[str]
    discovered_turn: NotRequired[int]
    discovery_condition: NotRequired[str]
    event_type: NotRequired[str]
    location: NotRequired[str]
    outcome: NotRequired[str]
    player_aware: NotRequired[bool]
    player_impact: NotRequired[str]
    status: NotRequired[str]

class WorldTimeDict(TypedDict, total=False):
    """In-game world time tracking"""
    day: NotRequired[int]  # Day of month
    hour: NotRequired[int]  # Hour of day (0-23)
    microsecond: NotRequired[int]  # Microseconds (0-999999) for precise time tracking in Thin...
    minute: NotRequired[int]
    month: NotRequired[int | str]
    second: NotRequired[int]
    time_of_day: NotRequired[str]  # Narrative time of day descriptor (accepts both lowercase ...
    year: NotRequired[int]  # Year in campaign calendar

class SocialHPChallengeDict(TypedDict, total=False):
    """Progress tracking for social persuasion encounters"""
    cooldown_remaining: NotRequired[int]
    cooldown_until_hour: NotRequired[int]
    npc_id: NotRequired[str]
    npc_name: NotRequired[str]
    npc_tier: NotRequired[str]
    objective: NotRequired[str]
    request_severity: NotRequired[str]
    resistance_shown: NotRequired[str]
    roll_dc: NotRequired[int]
    roll_result: NotRequired[int]
    skill_used: NotRequired[str]
    social_hp: NotRequired[int]
    social_hp_damage: NotRequired[int]
    social_hp_max: NotRequired[int]
    status: NotRequired[str]
    successes: NotRequired[int]
    successes_needed: NotRequired[int]

class ActionResolutionRollDict(TypedDict, total=False):
    """Canonical roll payload for action_resolution.mechanics.rolls."""
    dc: NotRequired[int]
    dc_category: NotRequired[str]
    dc_reasoning: NotRequired[str]
    die_type: NotRequired[str]
    margin: NotRequired[int]
    modifier: NotRequired[int]
    notation: Required[str]
    outcome: NotRequired[str]
    purpose: NotRequired[str]
    result: Required[int]
    success: Required[bool]
    total: NotRequired[int]

class PlanningChoiceDict(TypedDict, total=False):
    """A specific course of action available to the player"""
    confidence: NotRequired[str]  # Probability of success
    cons: NotRequired[list[str]]  # List of potential risks or downsides
    description: Required[str]  # Detailed explanation of what this choice entails
    freeze_time: NotRequired[bool]  # If true, selecting this choice freezes in-game time advan...
    id: Required[str]  # Machine-readable identifier for this choice (e.g., 'explo...
    pros: NotRequired[list[str]]  # List of potential advantages
    risk_level: Required[str]  # Danger level associated with this choice
    switch_to_story_mode: NotRequired[bool]  # If true, selecting this switches UI to character/story mode
    text: Required[str]  # Display name/title for the choice

class PlanningChoiceLegacyDict(TypedDict, total=False):
    """Legacy planning choice without embedded id (use map key as id)."""
    confidence: NotRequired[str]  # Probability of success
    cons: NotRequired[list[str]]  # List of potential risks or downsides
    description: Required[str]  # Detailed explanation of what this choice entails
    freeze_time: NotRequired[bool]  # If true, selecting this choice freezes in-game time advan...
    pros: NotRequired[list[str]]  # List of potential advantages
    risk_level: Required[str]  # Danger level associated with this choice
    switch_to_story_mode: NotRequired[bool]  # If true, selecting this switches UI to character/story mode
    text: Required[str]  # Display name/title for the choice

CharacterDict = TypedDict('CharacterDict', {
        'active_effects': NotRequired[list[str]],
        'age': NotRequired[int],
        'aliases': NotRequired[list[str]],
        'alignment': NotRequired[str],
        'attributes': NotRequired[dict[str, Any]],
        'background': NotRequired[str],
        'base_attributes': NotRequired[dict[str, Any]],
        'class': NotRequired[str],
        'class_name': NotRequired[str],
        'combat_stats': NotRequired[dict[str, Any]],
        'core_memories': NotRequired[list[str]],
        'current_location': NotRequired[str],
        'death_saves': NotRequired[dict[str, Any]],
        'display_name': NotRequired[str],
        'entity_id': NotRequired[str],
        'entity_type': NotRequired[EntityTypeDict],
        'equipment': NotRequired[dict[str, Any]],
        'equipped_items': NotRequired[dict[str, Any]],
        'gender': NotRequired[str],
        'health': NotRequired[HealthStatusDict],
        'hp_current': NotRequired[int],
        'hp_max': NotRequired[int],
        'inventory': NotRequired[list[dict[str, Any]]],
        'knowledge': NotRequired[list[str]],
        'level': NotRequired[int],
        'mbti': NotRequired[str],
        'name': NotRequired[str],
        'proficiency_bonus': NotRequired[int],
        'race': NotRequired[str],
        'recent_decisions': NotRequired[list[str]],
        'relationships': NotRequired[dict[str, Any]],
        'resources': NotRequired[dict[str, Any]],
        'spells_known': NotRequired[list[dict[str, Any]]],
        'stats': NotRequired[StatsDict],
        'status': NotRequired[EntityStatusDict],
        'status_conditions': NotRequired[list[str]],
        'string_id': NotRequired[str],
        'visibility': NotRequired[VisibilityDict],
        'xp': NotRequired[int],
}, total=False)
CharacterDict.__doc__ = 'Base character model for PCs and NPCs'

class FactionMinigameDict(TypedDict, total=False):
    """Turn-based faction strategy mini-game state. Allows players to manage their faction's military and political power."""
    buildings: NotRequired[dict[str, Any]]
    enabled: NotRequired[bool]  # Whether faction minigame is active for this campaign
    faction_power: NotRequired[float]  # Total faction power score
    ranking: NotRequired[int]  # Faction ranking among all factions (1 = strongest)
    resources: NotRequired[FactionResourcesDict]
    turn_number: NotRequired[int]  # Current faction turn (advances with in-game time)
    tutorial_completed: NotRequired[bool]  # Whether player has completed faction tutorial
    units: NotRequired[FactionUnitsDict]

class CombatStateDict(TypedDict, total=False):
    """Combat encounter tracking state"""
    active_combatant: NotRequired[str]  # Entity ID of combatant whose turn it is
    combat_phase: NotRequired[str]  # Current phase of combat
    combat_summary: NotRequired[None | dict[str, Any]]  # Summary of combat for narrative generation
    combatants: NotRequired[dict[str, Any]]  # Entity ID -> CombatantState mapping
    in_combat: NotRequired[bool]  # Whether combat is currently active
    initiative_order: NotRequired[list[Any]]  # Ordered list of characters by initiative (supports entity...
    participants: NotRequired[list[str]]
    rewards_processed: NotRequired[bool]  # Administrative flag indicating combat rewards were alread...
    round: NotRequired[int]  # Legacy alias for round_number
    round_number: NotRequired[int]  # Current combat round (1-indexed when in combat)

class WorldDataDict(TypedDict, total=False):
    """World state and location tracking"""
    current_location: NotRequired[dict[str, Any] | str]  # Party's current location (string ID or legacy object format)
    current_location_name: NotRequired[str]  # Legacy/display location name
    location: NotRequired[LocationDict | str]  # Legacy world_data.location field
    locations: NotRequired[dict[str, Any]]  # Location ID -> Location mapping
    weather: NotRequired[str]  # Current weather conditions
    world_events: NotRequired[list[WorldEventDict]]  # Active world-level events
    world_time: NotRequired[WorldTimeDict]

class ActionResolutionDict(TypedDict, total=False):
    """Mechanical audit trail for player actions"""
    audit_flags: Required[list[str]]
    interpreted_as: NotRequired[str]
    mechanics: NotRequired[dict[str, Any]]
    narrative_outcome: NotRequired[str]
    player_input: NotRequired[str]
    reinterpreted: Required[bool]

class PlanningBlockDict(TypedDict, total=False):
    """Structured planning and decision-making block (Think Mode)"""
    choice_id: NotRequired[str]  # Short identifier for the chosen choice
    choices: Required[Any]  # Planning choices as an ordered list or an id-keyed map.
    chosen_choice: NotRequired[str]  # Detailed explanation of the chosen path
    context: NotRequired[str]  # Optional context or background information
    plan_quality: NotRequired[dict[str, Any]]  # Assessment of plan quality based on intelligence/wisdom c...
    thinking: Required[str]  # Internal monologue analyzing the situation

PlayerCharacterDict = Any

NPCDict = Any

class CustomCampaignStateDict(TypedDict, total=False):
    """Campaign-specific state beyond core D&D mechanics. This is the primary extension point for WorldArchitect-specific features."""
    active_constraints: NotRequired[list[str]]  # Player-defined OOC constraints (e.g., 'keep my backstory ...
    active_missions: NotRequired[list[dict[str, Any] | str]]  # Currently active mission tracking (supports legacy string...
    arc_milestones: NotRequired[dict[str, Any]]  # Narrative arc milestone tracking (milestone_id -> ArcMile...
    attribute_system: NotRequired[str]  # Which attribute system to use (standard, point_buy, etc.)
    budget_warnings_shown: NotRequired[list[str]]  # Persist keys for budget warnings already shown to user
    campaign_tier: NotRequired[CampaignTierDict]
    character_creation_completed: NotRequired[bool]  # Whether character creation has been completed
    character_creation_in_progress: NotRequired[bool]  # Whether character creation wizard is active
    character_creation_stage: NotRequired[str]  # Current character creation stage identifier
    companion_arcs: NotRequired[dict[str, Any]]  # Companion personal quest arc tracking
    core_memories: NotRequired[list[str]]  # Persistent core memory snippets used for context continuity.
    divine_potential: NotRequired[int]  # Divine potential points (used for divine tier upgrades)
    divine_upgrade_available: NotRequired[bool]  # Whether player can upgrade to divine tier
    faction_minigame: NotRequired[FactionMinigameDict]
    god_mode: NotRequired[dict[str, Any]]  # God mode template/context payload
    god_mode_directives: NotRequired[dict[str, Any] | list[Any]]  # Player-defined narrative control rules
    last_location: NotRequired[str]  # Last resolved location name from story mode used for cont...
    last_story_mode_sequence_id: NotRequired[int]  # Last persisted story-mode sequence id for state synchroni...
    level_up_cancelled: NotRequired[bool]  # Legacy marker that level-up flow was cancelled
    level_up_complete: NotRequired[bool]  # Legacy marker that level-up flow completed
    level_up_in_progress: NotRequired[bool]  # Whether level-up flow is actively in progress
    level_up_pending: NotRequired[bool]  # Legacy level-up pending flag used for routing
    multiverse_upgrade_available: NotRequired[bool]  # Whether player can upgrade to sovereign/multiverse tier
    next_companion_arc_turn: NotRequired[int]  # Turn number when next companion arc event triggers
    player_character_data_extras: NotRequired[dict[str, Any]]  # Non-canonical player_character_data fields migrated for b...
    progression: NotRequired[dict[str, Any]]  # Campaign progression tracking
    reputation: NotRequired[dict[str, Any]]  # Reputation and notoriety sub-state
    success_streak: NotRequired[int]  # Consecutive significant successes without major setbacks ...
    universe_control: NotRequired[int]  # Universe control points (used for sovereign tier)
    world_events: NotRequired[dict[str, Any]]  # Nested living-world event payload preserved under custom ...

class StoryEntryDict(TypedDict, total=False):
    """Canonical Firestore story document contract (backward-compatible)."""
    action_resolution: NotRequired[ActionResolutionDict]
    actor: Required[str]
    debug_info: NotRequired[dict[str, Any]]
    dice_rolls: NotRequired[list[dict[str, Any]]]
    directives: NotRequired[dict[str, Any]]
    god_mode_response: NotRequired[str]
    mode: NotRequired[str]
    narrative: NotRequired[str]
    part: Required[int]
    planning_block: NotRequired[PlanningBlockDict]
    resources: NotRequired[str]
    session_header: NotRequired[str]
    state_updates: NotRequired[dict[str, Any]]
    text: Required[str]
    timestamp: Required[Any]
    world_events: NotRequired[dict[str, Any]]

class GameStateDict(TypedDict, total=False):
    """Complete game state schema for WorldArchitect.AI tabletop RPG platform"""
    action_resolution: NotRequired[ActionResolutionDict]
    combat_state: NotRequired[CombatStateDict]  # Current combat encounter state
    complications: NotRequired[dict[str, Any]]  # Current scene/world complications payload
    custom_campaign_state: NotRequired[CustomCampaignStateDict]  # WorldArchitect-specific campaign state extensions
    debug_mode: NotRequired[bool]  # Whether debug information should be shown
    dual_mode: NotRequired[bool]  # Compatibility flag for dual mode handling
    encounter_state: NotRequired[EncounterStateDict]  # Non-combat encounter tracking
    faction_minigame: NotRequired[FactionMinigameDict]  # Legacy top-level alias for custom_campaign_state.faction_...
    faction_updates: NotRequired[dict[str, Any]]  # Living-world faction update payloads
    game_state: NotRequired[dict[str, Any]]  # Legacy nested game_state container for compatibility
    game_state_version: Required[int]  # Schema version for migration support
    item_registry: NotRequired[dict[str, Any]]  # Global item definitions
    last_living_world_time: NotRequired[None | WorldTimeDict]  # World time snapshot of last living world generation
    last_living_world_turn: NotRequired[int]  # Last player turn when living world events were generated
    last_state_update_timestamp: NotRequired[str]  # ISO timestamp of last state modification
    location: NotRequired[LocationDict | dict[str, Any]]  # Legacy top-level location container
    npc_agendas: NotRequired[dict[str, Any]]  # NPC goal and plan tracking
    npc_data: NotRequired[dict[str, Any]]  # NPC ID -> NPC mapping
    pending_instruction_hints: NotRequired[list[str]]  # Queued instruction hints for the LLM
    planning_block: NotRequired[PlanningBlockDict]
    player_character_data: NotRequired[None | PlayerCharacterDict]  # Primary player character (null during early initialization)
    player_turn: NotRequired[int]  # Total player turns taken in this campaign
    rewards_pending: NotRequired[RewardsPendingDict]  # Rewards awaiting distribution
    rumors: NotRequired[list[dict[str, Any]]]  # Rumor/event snippets surfaced to player
    scene_event: NotRequired[dict[str, Any]]  # Current scene-level living-world event
    session_id: Required[str]  # Unique session identifier for the current game session
    social_hp_challenge: NotRequired[None | SocialHPChallengeDict]
    time_events: NotRequired[dict[str, Any]]  # Living-world time-based event payloads
    time_pressure_warnings: NotRequired[dict[str, Any]]  # Active time pressure indicators
    time_sensitive_events: NotRequired[dict[str, Any]]  # Events that trigger at specific times/turns
    turn_number: Required[int]  # Current turn number in the campaign
    user_settings: NotRequired[None | dict[str, Any]]  # User preferences and settings
    world_data: NotRequired[WorldDataDict]  # World state, locations, time
    world_events: NotRequired[dict[str, Any]]  # Living-world event bundle persisted for story continuity
    world_resources: NotRequired[dict[str, Any]]  # World-level resource tracking
