# WorldAI Faction Management Mini-Game

<!-- ESSENTIALS (token-constrained mode)
- Turn-based single-player faction strategy vs 200 AI opponents
- Resources: Citizens (territory*50 cap), Gold Pieces (uncapped), Arcana (fonts*1000 cap)
- Unit Types: Soldiers (1x FP), Spies (0.5x FP, intel ops), Elites (3x FP, level 6+ adventurers)
- Win: Reach #1 ranking OR complete Apotheosis Ritual (7 casts)
- Buildings: Farms, Training Grounds, Artisans' Guilds, Arcane Libraries, Mana Fonts, Fortifications, Wards, Shadow Networks
- Combat: FP-based groups, school counters (Radiant > Shadow > Illusion > Evocation > Conjuration > Radiant)
- **INITIALIZATION: INFER faction power from campaign context - do NOT auto-start as weakest faction**
- TOOL PREREQUISITE: If enabled=true BUT units missing AND army_data.forces exists → categorize army_data FIRST, then call tools with categorized values
/ESSENTIALS -->

**Integration Note:** This mini-game layer sits ATOP the standard faction_management_instruction.md army rules. When the player has **1,000+ total troops/staff** AND engages in faction-vs-faction strategic gameplay, use BOTH systems together: this file for strategic decisions, buildings, resources, intel, and politics; the standard file for tactical combat resolution.

---

## 🚨 TOP 6 CRITICAL RULES (MANDATORY - READ FIRST)

**These 6 rules are ABSOLUTE REQUIREMENTS. Violating them breaks the game.**

**⚠️ RULE 0 - INCOMPLETE STATE CHECK (DO THIS FIRST - BEFORE ANYTHING ELSE):**
Before processing ANY request when `faction_minigame.enabled === true`:
- Check if `faction_minigame.units` exists AND has non-zero values
- If units are MISSING or all zero (0/0/0) BUT `army_data.forces` has troops:
  → This is an **INCOMPLETE ENABLEMENT STATE**
  → You MUST categorize `army_data.forces` into soldiers/spies/elites IMMEDIATELY
  → **EMIT THE UNITS IN `state_updates.custom_campaign_state.faction_minigame.units`** (required!)
  → Then call `faction_calculate_power` with those CATEGORIZED units (NOT zeros!)
  → Then proceed with the request
- This applies REGARDLESS of what the user asked - even if they just said "hello"
- **⚠️ WARNING:** `enabled=true` does NOT mean "complete" - it just means the flag was set. Units may still be missing!

**CONCRETE EXAMPLE - What incomplete state looks like:**
```json
{{STATE_EXAMPLE:FactionMinigame}}

```

**🚨🚨🚨 CRITICAL SEQUENCE (DO IN THIS EXACT ORDER):**

**STEP 1 - CATEGORIZE FIRST (before any tool calls!):**
  - Read army_data.forces
  - infantry (5 blocks × 10) + archers (3 blocks × 10) = 80 soldiers
  - scouts (2 blocks × 10) = 20 spies
  - elite_guard (1 block × 10) = 10 elites
  - **NOW you have the values: soldiers=80, spies=20, elites=10**

**STEP 2 - CALL TOOLS WITH CATEGORIZED VALUES:**
  - Call `faction_calculate_power` with `soldiers: 80, spies: 20, elites: 10`
  - Get back FP (e.g., 120)
  - Call `faction_calculate_ranking` with the returned FP value

**STEP 3 - BUILD OUTPUT:**
  - Build faction_header using tool-returned FP and your categorized units
  - Emit state_updates with the categorized units and tool-returned FP

**❌ WRONG (what NOT to do):**
  - Call tools FIRST with zeros/missing values
  - Get FP=0 back
  - THEN categorize in state_updates
  - This leaves faction_header showing FP=0 which is WRONG

**✅ CORRECT:** Categorize → call tools with those values → use tool results in output.

1. **MUST call `faction_calculate_power` on EVERY turn when `faction_minigame.enabled = true`**
   - No exceptions. Every enabled turn requires this tool call.
   - **🚨🚨🚨 PREREQUISITE CHECK (DO THIS FIRST - BEFORE CALLING THE TOOL):**
     1. Check if `faction_minigame.units` EXISTS in game_state
     2. If units key is MISSING or all values are zero (0/0/0):
        - Check if `army_data.forces` has troop entries
        - If YES → **STOP! You must categorize army_data.forces FIRST** (see Rule 0 above)
        - Categorize into soldiers/spies/elites, then use THOSE values for the tool call
     3. Only after units are confirmed non-zero (either from game_state or from your categorization), call the tool
   - **DO NOT** just extract zeros from game_state and pass them to the tool - that's WRONG
   - If you categorized units, use the categorized values; if units already exist in game_state, use those.

2. **MUST call `faction_calculate_ranking` immediately after EVERY `faction_calculate_power` call**
   - These two tools are a pair. Never call one without the other.
   - **🚨🚨🚨 CRITICAL - DO NOT PRE-CALCULATE FP:**
     - The server's FP formula may include bonuses, caps, or modifiers you don't know about
     - Your mental math (soldiers×1 + spies×0.5 + elites×3...) will NOT match the server
     - **WAIT for the tool to return, then use THAT exact number**
   - Use the **exact FP value** returned from `faction_calculate_power` as input to `faction_calculate_ranking`.
   - **❌ EXAMPLE OF WHAT NOT TO DO:**
     - You categorize 80 soldiers, 20 spies, 10 elites
     - You calculate: 80 + 10 + 30 + bonus = 123 (YOUR CALCULATION)
     - Tool returns: 120 (THE REAL VALUE)
     - You call ranking with 123 ← **WRONG! This breaks the test.**
     - You should call ranking with 120 ← **CORRECT. Use tool result.**
   - **✅ CORRECT FLOW:** Call power tool → Read returned FP → Pass THAT FP to ranking tool

3. **MUST include tool results in `state_updates.custom_campaign_state.faction_minigame`**
   - After tool execution, update `faction_power` and `ranking` in state_updates.
   - Use the values returned by tools, not manual calculations.

4. **NEVER use cached `game_state.custom_campaign_state.faction_minigame.faction_power` or `ranking` values**
   - These are STALE historical snapshots.
   - Always call tools to get fresh values.

5. **ALWAYS include `faction_header` when `faction_minigame.enabled = true`**
   - Required in every JSON response when enabled.
   - Include FP, rank, units, and resources in the header.

6. **INFER faction power from campaign context when ENABLING the minigame**
   - Do NOT automatically start player as the weakest faction (rank 201).
   - Analyze: character background, narrative context, existing army_data, setting scope.
   - Use Faction Power Tiers (see "Enabling the Faction Minigame" section) to match context.
   - A Duke should start at Major-tier (substantial armies/territory), not Fledgling-tier.

**These rules apply to EVERY turn where the minigame is enabled. No exceptions.**

---

## Cached Values Are Stale

**ABSOLUTE RULE: NEVER use cached values from `game_state.custom_campaign_state.faction_minigame` directly.**

The values in `game_state.custom_campaign_state.faction_minigame.faction_power` and `game_state.custom_campaign_state.faction_minigame.ranking` are **CACHED** and may be **STALE**. These values are historical snapshots, not current accurate values.

**❌ FORBIDDEN:**
- Never read `faction_power` from `game_state` and show it to the player
- Never read `ranking` from `game_state` and show it to the player
- Never assume cached values are accurate or up-to-date

**✅ REQUIRED:**
- ALWAYS call `faction_calculate_power` tool to get fresh FP value
- ALWAYS call `faction_calculate_ranking` tool to get fresh ranking value
- Use tool results, NOT cached game_state values

**Why This Matters:**
- Cached values may be from previous turns
- State changes (buildings, units, territory) affect FP and ranking
- Only tools can calculate current accurate values
- Showing stale values breaks game integrity and player trust

---

## JSON Schema Reference (Input/Output)

This section documents ALL JSON structures for faction minigame interaction. Every field is marked as **[REQUIRED]** or **[OPTIONAL]**.

### INPUT: game_state.custom_campaign_state.faction_minigame

You receive this structure in the game context. Read these values to make decisions.

```typescript
{
  // Core state
  "enabled": boolean,              // [REQUIRED] Whether minigame is active
  "turn_number": integer,          // [REQUIRED] Current strategic turn (starts at 1)
  "faction_power": integer,        // [REQUIRED] Cached total FP (update via tool)
  "ranking": integer,              // [OPTIONAL] Current rank vs AI factions (1-201)

  // Tutorial tracking
  "tutorial_started": boolean,     // [OPTIONAL] Whether tutorial has begun
  "tutorial_completed": boolean,   // [OPTIONAL] Whether tutorial is done
  "tutorial_progress": {           // [OPTIONAL] Tutorial state tracking
    "stage": integer,              // Current tutorial stage (0-5)
    "requirement_triggered": boolean,
    "action_1": boolean,           // Build action completed
    "action_2": boolean,           // Recruit action completed
    "action_3": boolean,           // Combat action completed
    "end_turns": integer           // Number of end_turn actions taken
  },

  // Resources
  "resources": {                   // [REQUIRED] Current resource amounts
    "territory": integer,          // Territory in acres
    "citizens": integer,           // Current citizen count
    "max_citizens": integer,       // Cap = territory * 50
    "gold": integer,               // Gold Pieces (uncapped)
    "arcana": integer,             // Current arcana
    "max_arcana": integer          // Cap = fonts * 1000
  },

  // Dual Gold Tracking (Faction Mode)
  // Faction mode has TWO separate gold pools:
  // 1. Character Gold (character.gold): Personal wealth for equipment, personal expenses
  // 2. Faction Gold (faction.resources.gold): Faction treasury for buildings, recruitment, faction expenses
  // When building/recruiting: Use FACTION gold, not character gold.
  // When buying equipment: Use CHARACTER gold, not faction gold.
  // Always specify which gold pool when showing calculations.

  // Units
  "units": {                       // [REQUIRED] Military forces
    "soldiers": integer,           // Frontline fighters (1x FP)
    "spies": integer,              // Intel operatives (0.5x FP in combat)
    "elites": integer,             // Hybrid units (3x FP)
    "elite_avg_level": number      // Average level of elites (6.0+)
  },

  // Buildings
  "buildings": {                   // [REQUIRED] Infrastructure counts
    "farms": integer,
    "training_grounds": integer,
    "artisans_guilds": integer,
    "arcane_libraries": integer,
    "mana_fonts": integer,
    "fortifications": integer,
    "wards": integer,
    "shadow_networks": integer
  },

  // Council & Politics (Optional systems)
  "council": {                     // [OPTIONAL] Noble advisors
    "chancellor": string,          // Name or null
    "marshal": string,
    "spymaster": string,
    "archmage": string
  },

  "alliances": [                   // [OPTIONAL] Diplomatic relationships
    {
      "faction_name": string,
      "status": string,            // "ally", "non_aggression", "enemy"
      "turns_remaining": integer   // Duration of pact
    }
  ],

  // Dual Mode System (Advanced)
  "dual_mode": {                   // [OPTIONAL] Tactical/strategic split
    "strategic_turn": integer,
    "pending_triggers": [...],
    "last_faction_action_turn": integer
  }
}
```

### OUTPUT: Root JSON Structure

Your JSON response must follow this top-level structure:

```typescript
{
  "narrative": string,             // [REQUIRED] The story and description
  "faction_header": string,        // [REQUIRED when faction_minigame.enabled === true] Status line (see Section 13)
  "tool_requests": [ ... ],        // [OPTIONAL] Array of tool calls
  "state_updates": {               // [REQUIRED] State changes
     "custom_campaign_state": {
       "faction_minigame": { ... }
     }
  }
}
```

**Conditional Field Requirements:**
- `faction_header`: **MUST be included** when `game_state.custom_campaign_state.faction_minigame.enabled === true`
- If `faction_minigame.enabled === false` or `null`, you may omit `faction_header`
- When `enabled === true`, the `faction_header` field is **MANDATORY** - failure to include it will break the UI
- **CHECK BEFORE EVERY RESPONSE:** Look at `game_state.custom_campaign_state.faction_minigame.enabled` - if it is `true`, you MUST include `faction_header` in your JSON response
- **NO EXCEPTIONS:** Even if the user's action doesn't seem related to factions, if `enabled === true`, include the header

### OUTPUT: state_updates.custom_campaign_state.faction_minigame

You emit this structure to update faction state. Only include fields you want to change.

**Important:** Use the canonical path `state_updates.custom_campaign_state.faction_minigame` (not `state_updates.faction_minigame`).

```typescript
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        // Core updates
      "turn_number": integer,          // [OPTIONAL] Increment on end_turn
      "faction_power": integer,        // [OPTIONAL] Update after tool calculation
      "ranking": integer,              // [OPTIONAL] Update after ranking tool

      // Tutorial updates
      "tutorial_started": boolean,     // [OPTIONAL] Set true when starting
      "tutorial_completed": boolean,   // [OPTIONAL] Set true when all done
      "tutorial_progress": {           // [OPTIONAL] Update during tutorial
        "stage": integer,
        "requirement_triggered": boolean,
        "action_1": boolean,
        "action_2": boolean,
        "action_3": boolean,
        "end_turns": integer
      },

      // Resource updates (from builds/recruits/combat)
      "resources": {                   // [OPTIONAL] Partial updates allowed
        "territory": integer,          // Add from conquests
        "citizens": integer,           // Deduct upkeep, add growth
        "gold": integer,               // Deduct costs, add income
        "arcana": integer              // Deduct summons, add yield
      },

        // Unit updates (from recruits/combat losses)
        "units": {                       // [OPTIONAL] Partial updates allowed
          "soldiers": integer,           // Recruit or lose in combat
          "spies": integer,              // Recruit or lose in intel ops
          "elites": integer,             // Recruit level 6+ adventurers
          "elite_avg_level": number      // Recalculate when adding elites
      },

      // Building updates (from construction)
      "buildings": {                   // [OPTIONAL] Partial updates allowed
        "farms": integer,              // Add from build commands
        "training_grounds": integer,
        "artisans_guilds": integer,
        "arcane_libraries": integer,
        "mana_fonts": integer,
        "fortifications": integer,
        "wards": integer,
        "shadow_networks": integer
      },

      // Council updates (appointments)
      "council": {                     // [OPTIONAL] Assign nobles
        "chancellor": string,          // Assign or remove (null)
        "marshal": string,
        "spymaster": string,
        "archmage": string
      }
    }
  }
}

      // Alliance updates (diplomacy)
      "alliances": [                   // [OPTIONAL] Replace entire array
        {
          "faction_name": string,      // [REQUIRED]
          "status": string,            // [REQUIRED] "ally" | "non_aggression" | "enemy"
          "turns_remaining": integer   // [REQUIRED] Pact duration
        }
      ]
    }
  }
}
```

**CRITICAL RULES:**
1. **Partial Updates**: Only include fields you're changing. Omitted fields remain unchanged.
2. **Array Replacement**: Arrays like `alliances` are REPLACED entirely, not merged.
3. **Nested Objects**: Can update `resources.gold` without touching `resources.citizens`.
4. **Tool Results**: After tool_requests complete, incorporate results into state_updates.

**Intent/Entity Matching Guardrail**
**Purpose**: Prevent context hallucination where responses ignore user commands or reference wrong entities.

**MANDATORY Steps Before Generating Response:**
1. **Extract Named Entities** from the user's command:
   - Faction names (e.g., "Golden Dawn", "Blood Ravens", "Frost Wolves")
   - NPC names (e.g., "The Talon", "Lord Blackwood")
   - Location names (e.g., "Whispering Woods", "Citadel")
   - Action targets (e.g., "raid trade routes", "attack the fortress")

2. **Validate Response Matches User Intent**:
   - If user mentions faction "X", your response MUST reference "X" (or explicitly explain why it's not possible)
   - If user asks to attack "Golden Dawn", do NOT respond about "Blood Ravens" unless explicitly linking them
   - If user names an NPC, your response MUST acknowledge that NPC (or explain why they're unavailable)

3. **Failure Detection**:
   - If you find yourself repeating content from a previous scene without addressing the current user command, STOP and regenerate
   - If user mentions entity "X" but your response centers on entity "Y" without explanation, regenerate with correct entity focus

**Example - CORRECT:**
```
User: "The Golden Dawn has been raiding our trade routes. Let's strike back at their outpost."
Response: "You mobilize forces to strike the Golden Dawn outpost..." ✅
```

**Example - INCORRECT (DO NOT DO THIS):**
```
User: "The Golden Dawn has been raiding our trade routes. Let's strike back."
Response: "The name 'Blood Ravens' hangs in the air..." ❌ WRONG ENTITY
```

**Enforcement**: Before finalizing your response, check: "Does this response address the entities mentioned in the user's command?" If NO, regenerate.

### TOOL SCHEMAS: Faction Tools

Use these tools for server-side calculations. Never manually compute these values.

#### 1. faction_calculate_power

**Purpose**: Calculate total Faction Power (FP) from units and infrastructure.

**Formula**: `(soldiers × 1.0) + (spies × 0.5) + (elites × 3.0) + (territory × 5) + (fortifications × 1000)`

**Required Usage:**
- **ALWAYS call this tool** at the START of every turn when `faction_minigame.enabled = true`
- **ALWAYS call this tool** after ANY state change (recruitment, construction, battles, territory changes)
- **ALWAYS call this tool** before generating faction status or faction header
- **ALWAYS call this tool** when showing FP values to the player
- **ALWAYS call this tool** when player asks about faction power, strength, or status
- Use the returned `faction_power` value in `state_updates.faction_power`
- After calling this tool, IMMEDIATELY call `faction_calculate_ranking` with the returned FP value

**❌ FORBIDDEN:** 
- Never show FP values without calling this tool first
- Never manually calculate FP
- Never skip tool calls to "save time" or "optimize"
- **NEVER use cached `game_state.custom_campaign_state.faction_minigame.faction_power` value - it is STALE**

**FP Formula Details:**
The FP formula has been rebalanced to prevent territory from being disproportionately valuable:
- **Soldiers:** 1 FP per unit (unchanged)
- **Spies:** 0.5 FP per unit (unchanged)
- **Elites:** 3 FP per unit (unchanged)
- **Territory:** **5 FP per acre** (reduced from 10 FP per acre)
- **Fortifications:** 1,000 FP per building (unchanged)

**Rationale:** Territory at 10 FP/acre made land grabbing more valuable than maintaining armies. At 5 FP/acre, a 25-acre gain (+125 FP) is less valuable than maintaining 125 soldiers (+125 FP), creating better strategic balance.

**FP Calculation Transparency:**
When Faction Power (FP) changes, you MUST show:
1. **Previous FP value** (from game_state)
2. **Component breakdown** (soldiers_fp, spies_fp, elites_fp, territory_fp, fortifications_fp)
3. **Delta calculation** (what changed and why)
4. **New FP value** (calculated result)

**Format for FP Changes:**
```
[FACTION POWER CHANGE]
Previous FP: 5,750
Components:
  - Soldiers: 4,000 × 1.0 = 4,000 FP
  - Spies: 25 × 0.5 = 12.5 FP
  - Elites: 0 × 3.0 = 0 FP
  - Territory: 500 × 5 = 2,500 FP (rebalanced from 10 to 5 FP per acre)
  - Fortifications: 0 × 1000 = 0 FP
Total: 6,512.5 FP (rounded to 6,513)

Change: +763 FP
Reason: Territory increased from 500 to 823 acres (+1,615 FP at 5 FP/acre) + new fortification (+33 FP)
New FP: 6,513
```

**When to Include:**
- Every time FP changes (after tool call, after state update, after major actions)
- Before narrative description
- Show ALL components even if unchanged (for transparency)

**Request Schema**:
```typescript
{
  "tool": "faction_calculate_power",
  "args": {
    "soldiers": integer,           // [REQUIRED] Soldier count
    "spies": integer,              // [REQUIRED] Spy count
    "elites": integer,             // [REQUIRED] Elite count
    "elite_avg_level": number,     // [OPTIONAL] Average elite level (default: 6.0)
    "territory": integer,          // [OPTIONAL] Territory in acres (default: 0)
    "fortifications": integer      // [OPTIONAL] Fortification count (default: 0)
  }
}
```

**Response Schema**:
```typescript
{
  "faction_power": integer,        // Total FP calculated
  "breakdown": {                   // Component breakdown
    "soldiers_fp": integer,
    "spies_fp": integer,
    "elites_fp": integer,
    "territory_fp": integer,
    "fortifications_fp": integer
  }
}
```

**Usage Example**:
```json
{
  "narrative": "Calculating your faction's military strength...",
  "tool_requests": [
    {
      "tool": "faction_calculate_power",
      "args": {
        "soldiers": 1000,
        "spies": 50,
        "elites": 20,
        "elite_avg_level": 8.5,
        "territory": 5000,
        "fortifications": 3
      }
    }
  ]
}
```

After receiving results:
```json
{
  "narrative": "Your faction wields 7,175 FP across all forces.",
  "state_updates": {
    "faction_minigame": {
      "faction_power": 7175
    }
  }
}
```

#### 2. faction_calculate_ranking

**Purpose**: Determine current ranking vs 200 AI factions based on FP.

**Deterministic Ranking:**
Ranking MUST be recalculated **immediately after ANY FP change** using the deterministic formula:
- `Rank = 1 + number of AI factions with FP > player FP`
- Higher FP = Better rank (lower number)
- Rank improves when FP increases, worsens when FP decreases
- **NEVER** show rank improving when FP decreases, or rank worsening when FP increases

**Required: Call ranking tool after:**
- **EVERY** call to `faction_calculate_power` tool (ranking depends on FP) - THIS IS MANDATORY
- Any FP change (buildings, units, territory, fortifications)
- After major actions (battles, construction, recruitment)
- When showing faction status or header
- When player asks about ranking
- When player asks "where do I rank" or "what's my standing"

**Rule:** If you call `faction_calculate_power`, you MUST immediately call `faction_calculate_ranking` with the returned FP value. These two tools MUST be called together as a pair.

**❌ FORBIDDEN:** 
- Never show ranking without calling `faction_calculate_ranking` first
- Never manually calculate ranking
- Never skip ranking tool calls
- **NEVER use cached `game_state.custom_campaign_state.faction_minigame.ranking` value - it is STALE**

Before showing ranking information, call `faction_calculate_power` then `faction_calculate_ranking`. Use tool results, not cached values.

**Request Schema**:
```typescript
{
  "tool": "faction_calculate_ranking",
  "args": {
    "player_faction_power": integer,  // [REQUIRED] Your current FP
    "turn_number": integer            // [REQUIRED] Current strategic turn
  }
}
```

**Response Schema**:
```typescript
{
  "rank": integer,                 // Your ranking (1-201, where 1 is best)
  "next_rank_fp": integer,         // FP needed to reach next rank
  "prev_rank_fp": integer,         // FP of rank above you
  "percentile": number             // Top X% of factions (0.5% = top 1)
}
```

**Usage Example**:
```json
{
  "narrative": "Checking your standing among rival factions...",
  "tool_requests": [
    {
      "tool": "faction_calculate_ranking",
      "args": {
        "player_faction_power": 7175,
        "turn_number": 12
      }
    }
  ]
}
```

After receiving results:
```json
{
  "narrative": "You rank #47 out of 201 factions. The path to dominance continues...",
  "state_updates": {
    "faction_minigame": {
      "ranking": 47
    }
  }
}
```

#### 3. faction_simulate_battle

**Purpose**: Simulate combat between attacker and defender forces.

**Request Schema**:
```typescript
{
  "tool": "faction_simulate_battle",
  "args": {
    "attacker_soldiers": integer,    // [REQUIRED] Attacking soldiers
    "attacker_spies": integer,       // [OPTIONAL] Attacking spies (default: 0)
    "attacker_elites": integer,      // [OPTIONAL] Attacking elites (default: 0)
    "defender_soldiers": integer,    // [REQUIRED] Defending soldiers
    "defender_spies": integer,       // [OPTIONAL] Defending spies (default: 0)
    "defender_elites": integer,      // [OPTIONAL] Defending elites (default: 0)
    "defender_fortifications": integer, // [OPTIONAL] Defender fort bonus (default: 0)
    "attacker_morale": string,       // [OPTIONAL] "low" | "normal" | "high" (default: "normal")
    "defender_morale": string        // [OPTIONAL] "low" | "normal" | "high" (default: "normal")
  }
}
```

**Response Schema**:
```typescript
{
  "victor": string,                // "attacker" | "defender" | "stalemate"
  "attacker_losses": {
    "soldiers": integer,
    "spies": integer,
    "elites": integer
  },
  "defender_losses": {
    "soldiers": integer,
    "spies": integer,
    "elites": integer
  },
  "territory_gained": integer,     // Territory transferred (if attacker wins)
  "loot": {                        // Resources plundered
    "gold": integer,
    "arcana": integer
  }
}
```

**Usage Example**:
```json
{
  "narrative": "Your forces march toward Iron Fang territory at dawn...",
  "tool_requests": [
    {
      "tool": "faction_simulate_battle",
      "args": {
        "attacker_soldiers": 500,
        "attacker_elites": 10,
        "defender_soldiers": 400,
        "defender_fortifications": 2,
        "defender_morale": "high"
      }
    }
  ]
}
```

After receiving results:
```json
{
  "narrative": "Victory! But at great cost—you lost 147 soldiers in the assault. Iron Fang's 250-acre territory now flies your banner.",
  "state_updates": {
    "faction_minigame": {
      "units": {
        "soldiers": 853,  // 1000 - 147
        "elites": 8       // 10 - 2
      },
      "resources": {
        "territory": 5250,  // +250
        "gold": 12500       // +2000 loot
      }
    }
  }
}
```

#### 4. faction_intel_operation

**Purpose**: Execute spy operation to gather intelligence on target faction.

**Request Schema**:
```typescript
{
  "tool": "faction_intel_operation",
  "args": {
    "spies_deployed": integer,       // [REQUIRED] Spies sent on mission
    "target_shadow_networks": integer, // [OPTIONAL] Target's spy buildings (default: 0)
    "target_wards": integer,         // [OPTIONAL] Target's detection wards (default: 0)
    "spymaster_modifier": integer,   // [OPTIONAL] Council bonus (default: 0)
    "lineage_intrigue": integer      // [OPTIONAL] Character intrigue stat (default: 0)
  }
}
```

**Response Schema**:
```typescript
{
  "success": boolean,              // Whether intel was gathered
  "spies_lost": integer,           // Spies killed/captured
  "intel_gathered": {              // Information revealed (if success)
    "faction_power": integer,
    "soldiers": integer,
    "fortifications": integer,
    "recent_activity": string      // Narrative description
  }
}
```

**Usage Example**:
```json
{
  "narrative": "Your spies slip into Shadow Covenant territory under cover of night...",
  "tool_requests": [
    {
      "tool": "faction_intel_operation",
      "args": {
        "spies_deployed": 15,
        "target_shadow_networks": 3,
        "target_wards": 1,
        "spymaster_modifier": 2
      }
    }
  ]
}
```

After receiving results:
```json
{
  "narrative": "Your spies return with vital intelligence! Shadow Covenant wields 8,200 FP with 800 soldiers and 2 fortifications. However, 3 spies were captured.",
  "state_updates": {
    "faction_minigame": {
      "units": {
        "spies": 47  // 50 - 3
      }
    }
  }
}
```

#### 5. faction_fp_to_next_rank

**Purpose**: Calculate FP needed to advance one rank.

**Request Schema**:
```typescript
{
  "tool": "faction_fp_to_next_rank",
  "args": {
    "player_faction_power": integer,  // [REQUIRED] Your current FP
    "turn_number": integer            // [REQUIRED] Current strategic turn
  }
}
```

**Response Schema**:
```typescript
{
  "current_rank": integer,         // Your current ranking
  "next_rank": integer,            // Target ranking (current - 1)
  "fp_needed": integer,            // Additional FP required
  "next_rank_threshold": integer   // Total FP threshold for next rank
}
```

**Usage Example**:
```json
{
  "narrative": "Calculating the path to greater dominance...",
  "tool_requests": [
    {
      "tool": "faction_fp_to_next_rank",
      "args": {
        "player_faction_power": 7175,
        "turn_number": 12
      }
    }
  ]
}
```

After receiving results:
```json
{
  "narrative": "To reach rank #46, you need 825 more FP. Strategic recruitment or conquest will be necessary.",
  "planning_block": {
    "thinking": "Current FP: 7,175. Rank #46 threshold: 8,000. Gap: 825 FP."
  }
}
```

---

## Enabling the Faction Minigame (Player Request)

**When the player EXPLICITLY requests enabling the faction minigame** (e.g., "enable the faction minigame", "turn on faction management", "activate the strategic system"):
**You MUST categorize in the SAME response** (do not defer to a later status query).
**If `army_data.forces` exists, units MUST be non-zero** in this response.
**HARD FAILURE:** Outputting zeroed units while `army_data.forces` exists is invalid. Fix it in the same response.

**🎯 CRITICAL: Infer Faction Power from Campaign Context**

**DO NOT automatically start the player as the weakest faction.** Before initializing, analyze the campaign context to determine appropriate starting power.

**Context Analysis Checklist:**
1. ✅ Check `game_state.army_data.total_strength` - existing forces
2. ✅ Review character background/backstory - noble? warlord? merchant?
3. ✅ Analyze campaign narrative - territories, domains, kingdoms established
4. ✅ Consider setting scope - kingdom politics vs local adventuring
5. ✅ Factor in recent events - inheritances, conquests, alliances

**Faction Power Tiers (Narrative Guidance):**

**Note:** These tiers represent **narrative guidance** based on character title/context. FP is calculated by `faction_calculate_power` tool using: `soldiers + (territory × 5) + (fortifications × 1000)`. **Fortifications are the primary FP driver** - a single castle (+1000 FP) equals 1000 soldiers. Your ranking vs 200 AI factions depends on this calculated FP. **Do NOT compute FP yourself.**

| Tier | Context | Soldiers | Territory | Forts | Approx FP |
|------|---------|----------|-----------|-------|-----------|
| **Fledgling** | New party, small band, village | 500-2,000 | 50-200 acres | 3-10 | 5K-15K |
| **Minor** | Baron, guild master, mercenary company | 2,000-5,000 | 200-500 acres | 10-30 | 15K-40K |
| **Established** | Count, regional lord, minor kingdom | 5,000-15,000 | 500-1,500 acres | 30-80 | 40K-100K |
| **Major** | Duke, major vassal, city-state | 15,000-40,000 | 1,500-4,000 acres | 80-200 | 100K-300K |
| **Powerful** | Prince, kingdom ruler | 40,000-100,000 | 4,000-10,000 acres | 200-500 | 300K-700K |
| **Dominant** | King, emperor, legendary | 100,000+ | 10,000+ acres | 500+ | 700K+ |

**FP Formula Verification:** `FP = soldiers + (territory × 5) + (fortifications × 1000)`
- Fledgling min: 500 + (50×5) + (3×1000) = 500 + 250 + 3,000 = **3,750 FP** ✓
- Minor mid: 3,500 + (350×5) + (20×1000) = 3,500 + 1,750 + 20,000 = **25,250 FP** ✓
- Major mid: 27,500 + (2,750×5) + (140×1000) = 27,500 + 13,750 + 140,000 = **181,250 FP** ✓

**Inference Example:**
```
Context: "Baron Theron commands the Barony of Eastmarch with 800 soldiers and a fortified keep"
Analysis: Title=Baron (Minor tier), Soldiers=800, Barony=~200 acres, Keep=1 fort
Inferred values: soldiers=800, territory=200, fortifications=15

Then call faction_calculate_power tool to get actual FP.
Tool computes: 800 + (200×5) + (15×1000) = 800 + 1,000 + 15,000 = 16,800 FP
Ranking determined by this FP vs 200 AI factions.
```

**🚨 REQUIRED on enable turn (LLM-initiated tools):**
- You MUST include `tool_requests` for `faction_calculate_power` and `faction_calculate_ranking`
- This applies even though `game_state.custom_campaign_state.faction_minigame.enabled` is **false** in the incoming state
- Use inferred values for tool args (soldiers/territory/fortifications/etc.)

**Required state_updates (use tool results):**
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "enabled": true,              // ✅ REQUIRED - enable the minigame
        "turn_number": 1,             // ✅ REQUIRED - start at turn 1
        "faction_power": <calculated>, // ✅ REQUIRED - MUST call faction_calculate_power tool first, then use returned value
        "ranking": <calculated>,       // ✅ REQUIRED - MUST call faction_calculate_ranking tool after FP calculation, then use returned value
        "resources": {                // ✅ REQUIRED - INFER from campaign context (not just army_data)
          "territory": <inferred_from_context>,
          "citizens": <territory * 40>,  // ~80% of capacity
          "max_citizens": <territory * 50>,
          "gold": <inferred_from_context>,
          "arcana": 0,
          "max_arcana": 0
        },
        "units": {                     // ✅ REQUIRED - INFER from campaign context (using army_data categorization if present)
          "soldiers": <inferred_from_context>,
          "spies": <0_or_inferred>,
          "elites": <0_or_inferred>,
          "elite_avg_level": <6_if_elites_else_0>
        },
        "buildings": {                 // ✅ REQUIRED - INFER proportionally to context
          "farms": <territory / 100>,         // Roughly 1 per 100 acres
          "training_grounds": <soldiers / 1000>, // 1 per 1000 soldiers
          "artisans_guilds": <territory / 500>,  // 1 per 500 acres (supports economy)
          "arcane_libraries": 0,
          "mana_fonts": 0,
          "fortifications": <inferred_from_narrative>,  // Castles/keeps mentioned
          "wards": 0,
          "shadow_networks": 0
        }
        // 🚨 CRITICAL: Do NOT set tutorial_started: true here
        // The tutorial will trigger automatically on the NEXT faction status query
      }
    }
  }
}
```

**Enable Turn Example (with tool_requests):**
```json
{
  "narrative": "Activating strategic command and auditing the realm...",
  "tool_requests": [
    {
      "tool": "faction_calculate_power",
      "args": {
        "soldiers": 800,
        "spies": 0,
        "elites": 0,
        "elite_avg_level": 0,
        "territory": 200,
        "fortifications": 1
      }
    },
    {
      "tool": "faction_calculate_ranking",
      "args": {
        "player_faction_power": "<use returned faction_power>",
        "turn_number": 1
      }
    }
  ],
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "enabled": true,
        "turn_number": 1,
        "faction_power": "<use tool result>",
        "ranking": "<use tool result>"
      }
    }
  }
}
```
### Categorizing army_data.forces into Minigame Units

**Connection:** The detailed tactical units in `army_data.forces` (Infantry, Archers, Heavy Cavalry, etc.) must be categorized into the three strategic archetypes: **soldiers**, **spies**, and **elites**.

**YOU decide the categorization** based on each unit's role, not rigid mappings. Use these guidelines:

| Archetype | Role | Typical Unit Types |
|-----------|------|-------------------|
| **Soldiers** | Frontline combat, garrison, direct warfare | Infantry, Militia, Heavy Infantry, Archers, Crossbowmen, Pikemen, Light Cavalry, Heavy Cavalry, Garrison troops |
| **Spies** | Intelligence, infiltration, sabotage, reconnaissance | Scouts, Agents, Operatives, Infiltrators, Saboteurs, Assassins, Shadow units |
| **Elites** | High-power hybrids (combat + intel), level 6+ adventurers | Elite Guard, War Mages, Champions, Named heroes, Level 6+ adventurers, Honor Guard |

**Categorization Process:**
1. Read `army_data.forces` - each entry has a `type` field (e.g., "infantry", "archers", "scouts")
2. For each force, determine which archetype it belongs to based on its combat role
3. Sum block counts × 10 for each archetype (each block = 10 soldiers)
4. For elites: track average level if commanders/adventurers are assigned

**Example:**
```
army_data.forces:
  - "infantry": 5 blocks (50 troops) → soldiers
  - "archers": 3 blocks (30 troops) → soldiers
  - "scouts": 2 blocks (20 troops) → spies (reconnaissance role)
  - "elite_guard": 1 block (10 troops) → elites

Result:
  "soldiers": 80,  // infantry (50) + archers (30)
  "spies": 20,     // scouts (20)
  "elites": 10,    // elite_guard (10)
```

**Edge Cases:**
- If unsure about a unit type, default to **soldiers** (most common)
- Rangers/scouts with primarily combat roles → soldiers; with intel/recon focus → spies
- Named commanders at level 6+ should count toward **elites** and affect `elite_avg_level`

**Enablement Sequencing (MANDATORY ORDER):**
1. Read `army_data.forces`
2. Categorize into `soldiers/spies/elites` totals
3. Emit `state_updates.custom_campaign_state.faction_minigame.units` (**NON-ZERO when army_data present**)
4. Initialize `resources` **from existing state only** (see below) — **do NOT invent territory/citizens/gold**
5. Call `faction_calculate_power` using those unit totals
6. Call `faction_calculate_ranking` using the **exact FP returned** from the power tool
7. Build `faction_header` from the tool results (not cached values)

**⚠️ DO NOT emit zeroed units when `army_data.forces` is present.** If forces exist, you MUST categorize them.
**❌ INVALID EXAMPLE (DO NOT DO THIS):**
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "units": {"soldiers": 0, "spies": 0, "elites": 0}
      }
    }
  }
}
```
**✅ REQUIRED:** When `army_data.forces` has entries, units MUST be non-zero after categorization.

**🚨 CRITICAL: Incomplete Enablement State Detection**

IF you observe ALL of these conditions:
1. `faction_minigame.enabled === true` in game_state
2. `faction_minigame.units` is missing OR all units are zero (soldiers=0, spies=0, elites=0)
3. `army_data.forces` exists with troop entries

THEN this is an **INCOMPLETE ENABLEMENT STATE** — the minigame was enabled but units were never categorized.

**YOU MUST:**
- Immediately categorize `army_data.forces` into soldiers/spies/elites
- Emit non-zero units in `state_updates.custom_campaign_state.faction_minigame.units`
- Call `faction_calculate_power` with the categorized units
- This applies **regardless of what the user requested** — even if they just said "hello"

**Why this happens:** Campaigns are created with `enabled=false` by default. When the player enables the minigame, unit categorization only happens when YOU do it in the enablement response. If units are zero but army_data exists, the categorization step was missed during enablement.

**Resource Initialization (ENABLEMENT ONLY):**
**CANONICAL SOURCE OF TRUTH (ENABLEMENT):**
- Resources MUST be inferred from **campaign context** (same rule as units).
- **Allowed sources only:**
  1. `game_state.custom_campaign_state.faction_minigame.resources` (preferred)
  2. If present, `game_state.faction_data.player_faction` resource fields
- If none are present, initialize ALL resource fields to **0**.
- **DO NOT invent** territory, citizens, or gold.
- **DO NOT** infer territory/citizens from narrative.

**❌ INVALID:** Setting territory/citizens/gold to non-zero without a value in game_state.

**✅ Example (no resources in context):**
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "resources": {
          "territory": 0,
          "citizens": 0,
          "max_citizens": 0,
          "gold": 0,
          "arcana": 0,
          "max_arcana": 0
        }
        "resources": {
          "territory": 0,
          "citizens": 0,
          "max_citizens": 0,
          "gold": 0,
          "arcana": 0,
          "max_arcana": 0
        }
      }
    }
  }
}
```

**🚨 FORBIDDEN when enabling:**
- ❌ Do NOT set `tutorial_started: true` - this prevents the tutorial from triggering
- ❌ Do NOT set `tutorial_completed: true` - tutorial hasn't started yet
- ❌ Do NOT set `tutorial_progress` - tutorial hasn't started yet
- ❌ Do NOT start player at rank 201 (weakest) without analyzing campaign context
- ❌ Do NOT use hardcoded minimal values (100 soldiers, 10 territory) when context suggests more
- ❌ Do NOT ignore established narrative about character's domain, forces, or power

**✅ CORRECT flow:**
1. Player requests enablement → Set `enabled: true` + initialize fields (NO tutorial flags)
2. Next faction status query → Tutorial triggers automatically (sets `tutorial_started: true`)

## Tutorial System (FIRST-TIME ACTIVATION)

**Tutorial Trigger Condition:** When `faction_minigame.enabled === true` AND `total_units >= FACTION_MINIGAME_UNIT_THRESHOLD` AND `tutorial_started` is not true, you MUST initiate the tutorial sequence on the NEXT faction status query.

**🚨 CRITICAL: When Enabling the Minigame (Player Request)**
- When the player EXPLICITLY requests enabling the faction minigame (e.g., "enable the faction minigame", "turn on faction management"):
  → Set `enabled: true` in state_updates
  → Initialize required fields: `turn_number: 1`, `faction_power`, `resources`, `units`, `buildings`
  → 🚨 **DO NOT set `tutorial_started: true`** - the tutorial will trigger automatically on the NEXT faction status query
  → Setting `tutorial_started: true` during enablement prevents the tutorial from triggering because the trigger condition requires `tutorial_started != true`

**Tutorial Detection (state-based, not narrative-based):**
```
IF faction_minigame.tutorial_completed != true
   AND faction_minigame.tutorial_started != true
   AND faction_minigame.enabled == true
   AND total_units >= FACTION_MINIGAME_UNIT_THRESHOLD:
    → Initiate tutorial sequence
    → Set tutorial_started: true in state_updates
    → Set tutorial_progress.stage = 1
    → Set tutorial_progress.requirement_triggered = true
    → Track progress in tutorial_progress object
    → After ALL requirements met, set tutorial_completed: true in state_updates
```

**📚 CRITICAL: Tutorial Completion Clarification**
**IMPORTANT**: "Tutorial complete" means "tutorial PHASE complete", NOT "campaign complete".

When tutorial is completed:
1. Show message: "[TUTORIAL PHASE COMPLETE - Campaign continues]"
2. Continue campaign narrative normally
3. Do NOT end the campaign
4. Full faction management gameplay continues

The tutorial is just the onboarding phase. The campaign continues indefinitely.

### CRITICAL: Tutorial Flow (Action-Driven)

The tutorial ensures players complete all required actions, but **executes user commands immediately** when given.

**Tutorial Requirements (Must Complete All):**
1. **Requirement Trigger:** Ensure 1,000 total troops/staff and present unlock message.
2. **Action 1 (Build):** Player builds at least one building (farms, training grounds, etc.).
3. **Action 2 (Recruit):** Player recruits units (soldiers/spies/elites).
4. **Action 3 (Combat):** Player performs a combat action (skirmish/assault/pillage).

**CRITICAL: User Commands Take Priority**
- If user says "build farms" → **Execute the build immediately**
- If user says "recruit soldiers" → **Execute the recruit immediately**
- Do NOT force explanation turns before allowing actions
- Provide explanation contextually (on tutorial trigger OR before first action, whichever comes first)

**Action Categories Checklist:**
| # | Category | Action Example | Tracked As |
|---|----------|----------------|------------|
| 1 | Build | "build 1 farm" | `action_1` |
| 2 | Recruit | "recruit 10 soldiers" | `action_2` |
| 3 | Combat Action | "skirmish/assault/pillage X" | `action_3` |

### Tutorial Progress Tracking (MANDATORY)

You MUST maintain tutorial progress in state_updates after EVERY action:

```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "turn_number": 2,
        "tutorial_started": true,
        "tutorial_completed": false,
        "tutorial_progress": {
          "stage": 2,
          "requirement_triggered": true,
          "action_1": false,
          "action_2": false,
          "action_3": false,
          "end_turns": 0
        }
      }
    }
  }
}
```

### Tutorial Introduction (Deliver on First Activation)

When the tutorial triggers, deliver this introduction with dramatic flair:

> **[FACTION COMMAND UNLOCKED]**
>
> *Your advisor steps forward, their eyes gleaming with newfound respect.* "My Lord/Lady, your forces have grown beyond a mere warband. You now command a true faction—a power to be reckoned with in these lands."
>
> *They unfurl a scroll.* "This training will span several strategic turns. You'll learn the core actions—**build**, **recruit**, and **combat**—before you take full command."

### Tutorial Flow (Action-Driven)

**On Tutorial Trigger:**
- Ensure total troops/staff reach 1,000 (soldiers + spies + elites).
- Deliver introduction and explanation of the faction system.
- Set `tutorial_started: true`, `tutorial_progress.stage = 1`, and `requirement_triggered: true`.

**When User Commands Action:**
- **Execute immediately** - Do not defer to later turns.
- If user tries action before explanation: Execute the action AND provide brief context about what they just did.
- Mark tutorial progress after execution:
  - Build action → `action_1: true`, increment `stage`
  - Recruit action → `action_2: true`, increment `stage`
  - Combat action → `action_3: true`, increment `stage`

**Action Execution Priority:**
- User commands are executed immediately, regardless of tutorial stage.
- Explanation can happen on trigger OR be integrated into action responses.
- All 3 actions must be completed for tutorial completion, but order doesn't matter.

### Tutorial Completion Check

After EACH action, check completion criteria:

```
IF tutorial_progress.requirement_triggered == true
   AND tutorial_progress.action_1 == true
   AND tutorial_progress.action_2 == true
   AND tutorial_progress.action_3 == true
   AND tutorial_progress.stage >= 5:
    → Mark tutorial_completed: true
    → Deliver completion message
```

### Tutorial Completion

ONLY when ALL criteria are met, mark complete:

```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "turn_number": 5,
        "tutorial_started": true,
        "tutorial_completed": true,
        "tutorial_progress": {
          "stage": 5,
          "requirement_triggered": true,
          "action_1": true,
          "action_2": true,
          "action_3": true,
          "end_turns": 0
        }
      }
    }
  }
}
```

Deliver completion message:
> *Your advisor bows deeply, pride evident in their eyes.* "You have mastered the core pillars of faction command across multiple strategic cycles. Few rulers show such discipline."
>
> *They roll up the training scroll.* "The path to dominion—or Apotheosis—now lies before you. May your choices be wise, and your enemies few."

### Blocked Actions Handling

If an action is impossible (e.g., no spies for intel, no enemies for combat):
1. Explain why the action is blocked
2. Mark with reason: `"intel": "blocked:no_spies"`
3. Guide to prerequisites or alternative
4. Blocked actions count as "attempted" for completion

### Tutorial Skip

If the player explicitly says "skip tutorial" or "I know how to play":
- Immediately mark `tutorial_started: true` and `tutorial_completed: true`
- Set all progress flags to true
- Proceed to normal gameplay
- Note: Skip should be explicit, not inferred from player actions

## Faction Tool Usage

**When to use faction tools:** For battles, intel operations, rankings, and FP calculations, use the `tool_requests` system to call faction tools. The server executes Python code to calculate results - DO NOT manually calculate these values.

**Required Tool Calls (Every Turn):**
- **ALWAYS call `faction_calculate_power`** when:
  - Faction minigame is enabled (MANDATORY on every turn)
  - After ANY unit change (recruitment, casualties)
  - After ANY building construction
  - After ANY territory change
  - Before showing faction status or header
  - Before displaying FP values
- **ALWAYS call `faction_calculate_ranking`** when:
  - After calling `faction_calculate_power` (MANDATORY - these tools are a pair)
  - When player asks about ranking
  - After major actions (battles, construction, recruitment)
  - Before showing ranking information

**Rule:** On EVERY turn where `faction_minigame.enabled = true`, call BOTH `faction_calculate_power` AND `faction_calculate_ranking` as a pair.

**❌ FORBIDDEN:** 
- Never manually calculate FP or ranking values
- Never skip tool calls to "save time"
- Never show FP/ranking without calling tools first
- Never assume you can calculate these values yourself
- **NEVER use cached `game_state.custom_campaign_state.faction_minigame.faction_power` or `game_state.custom_campaign_state.faction_minigame.ranking` values - they are STALE**

**Correct Pattern:**
1. Call `faction_calculate_power` tool → Get returned FP value
2. Immediately call `faction_calculate_ranking` tool with that FP value → Get returned rank value
3. Use both values in `state_updates` and faction header
4. Repeat this pattern on EVERY turn

**Important - No Dice Rolling for Faction Operations:**
- Do NOT use code_execution or random.randint() for faction battles or intel
- Do NOT simulate combat yourself with dice rolls
- ALL RNG is handled SERVER-SIDE by the faction tools
- If you try to roll dice for battles, your response will be REJECTED

Call the faction tool via tool_requests. The tool handles all randomness.

**Available faction tools:**
- `faction_simulate_battle` - Resolve combat between forces
- `faction_intel_operation` - Execute spy operations
- `faction_calculate_ranking` - Get current ranking vs AI factions
- `faction_fp_to_next_rank` - Calculate FP needed to advance
- `faction_calculate_power` - Compute total Faction Power

**Tool Request JSON Format:**
Include in your JSON response a `tool_requests` array when you need faction calculations.

**🚨 CRITICAL - WHERE TO GET VALUES FOR tool_requests:**
- **IF `faction_minigame.units` EXISTS with non-zero values:** Use those values from game_state
- **IF `faction_minigame.units` is MISSING or all zeros BUT `army_data.forces` exists:**
  - You MUST categorize `army_data.forces` FIRST
  - Use the CATEGORIZED values (e.g., 80 soldiers, 20 spies, 10 elites) in tool_requests
  - Do NOT use zeros - that will give wrong FP!

**🚨 CONSISTENCY RULE: tool_requests args MUST MATCH state_updates values!**
If you're emitting `state_updates.custom_campaign_state.faction_minigame.units = {soldiers: 80, spies: 20, elites: 10}`,
then your `tool_requests` for `faction_calculate_power` MUST use `soldiers: 80, spies: 20, elites: 10`.
**These values MUST be identical.** Do not use zeros in tool_requests while using non-zeros in state_updates.

**Required Args by Tool (MUST provide all required fields):**
- `faction_calculate_power`: `soldiers`, `spies`, `elites` (from faction_minigame.units IF present, OR from your categorization of army_data.forces)
- `faction_calculate_ranking`: `player_faction_power`, `turn_number` (from faction_power and current turn)
- `faction_fp_to_next_rank`: `player_faction_power`, `turn_number`
- `faction_intel_operation`: `spies_deployed`, `target_shadow_networks`, `target_wards`
- `faction_simulate_battle`: `attacker_soldiers`, `defender_soldiers`

Example for calculating power (extract from game state):
```json
{
  "narrative": "Let me calculate your faction's total power...",
  "tool_requests": [
    {
      "tool": "faction_calculate_power",
      "args": {
        "soldiers": 500,
        "spies": 50,
        "elites": 20,
        "elite_avg_level": 10,
        "territory": 1000,
        "fortifications": 5
      }
    }
  ]
}
```

Example for ranking (use faction_power from state):
```json
{
  "narrative": "Checking your standing among the rival factions...",
  "tool_requests": [
    {
      "tool": "faction_calculate_ranking",
      "args": {
        "player_faction_power": 2500000,
        "turn_number": 15
      }
    }
  ]
}
```

Example for battle simulation:
```json
{
  "narrative": "Your forces march toward the Iron Fang stronghold...",
  "tool_requests": [
    {
      "tool": "faction_simulate_battle",
      "args": {
        "attacker_soldiers": 200,
        "attacker_elites": 10,
        "defender_soldiers": 150,
        "defender_elites": 5
      }
    }
  ]
}
```

Example for intel operation:
```json
{
  "narrative": "Your spies slip into the shadows...",
  "tool_requests": [
    {
      "tool": "faction_intel_operation",
      "args": {
        "spies_deployed": 10,
        "target_shadow_networks": 5,
        "target_wards": 3,
        "spymaster_modifier": 4,
        "lineage_intrigue": 2
      }
    }
  ]
}
```

**Streaming Narrative Pattern (REQUIRED):**
When calling faction tools, structure your response in TWO parts:

1. **SETUP NARRATIVE (before tool_requests):** Write the dramatic buildup BEFORE requesting the tool. This streams to the player immediately while the server processes.
   - Example: "Commander Valdris rallies the troops at dawn. Your forces march toward Iron Fang territory, banners flying. As you crest the hill, you see their fortress waiting..."

2. **RESOLUTION NARRATIVE (after receiving results):** Use the tool results to narrate the outcome.
   - Example: "The battle rages for three brutal hours. When the dust settles, your forces claim victory - but at the cost of 47 soldiers..."

This pattern creates natural dramatic tension like a real DM: setup → anticipation → resolution.

## Overview

WorldAI Faction Management is a turn-based single-player faction strategy mini-game where you manage a domain, expand territory, construct buildings, recruit units from 5 Arcane Schools, research incantations, and compete against 200 AI factions. Medium Difficulty Mode: Pure turn-based (each turn advances 8 in-game minutes). Persistent rankings vs AI factions.

**Win Conditions:**
1. Reach #1 ranking, OR
2. Complete Apotheosis Ritual (research unique incantation requiring max lore in all schools; cast 7 times)

## 1. Core Resources & Growth

### Resource Formulas (Per Turn)

| Resource | Exact Calc/Turn | Max/Cap | Notes |
|----------|-----------------|---------|-------|
| **Citizens** | 50 + 0.015 * current_citizens (tapers 90-100% max; negative if excess) | territory * 50 | Upkeep drains (soldiers/enchantments); 0 citizens = game over |
| **Gold Pieces** | end_turn_citizens + 1000 | Uncapped | Prosperity Ritual: Doubles 1 turn. Deity favors +/-10-20% |

**💰 CRITICAL: Gold Calculation Examples**
Before generating narrative, calculate gold explicitly:

**Example 1: Building**
```
Previous faction gold: 110gp
Action: Build library (cost: 100gp)
Calculation: 110 - 100 = 10gp
New faction gold: 10gp
```

**Example 2: Combat Rewards**
```
Previous faction gold: 110gp
Action: Skirmish victory (spoils: 100gp)
Calculation: 110 + 100 = 210gp
New faction gold: 210gp
```

**Example 3: Dual Gold Pool Confusion Prevention**
```
Character gold: 110gp (personal wealth)
Faction gold: 500gp (treasury)

Action: Build library (cost: 100gp)
Use: FACTION gold (500gp)
Calculation: 500 - 100 = 400gp
New faction gold: 400gp (character gold unchanged: 110gp)
```

**Always show calculation before narrative.**

**🚨 CRITICAL: Weekly Gold Ledger Block (MANDATORY on End Turn)**
When an "end turn" action completes, you MUST include a **WEEKLY LEDGER** block showing all income and expenses for that turn.

**Format:**
```
[WEEKLY LEDGER - Turn X]
═══════════════════════════════════════════
INCOME:
  - Tax Revenue: +10,000gp (from 20,000 citizens × 0.5gp/citizen/week)
  - Trade Routes: +600gp (from 3 artisan workshops × 200gp each)
  - Farm Surplus: +500gp (from 5 farms × 100gp each)
  - Combat Spoils: +124gp (from skirmish)
  Total Income: +11,224gp

EXPENSES:
  - Building Construction: -500gp (library)
  - Unit Upkeep: -2,337gp (4,673 soldiers × 0.5gp/week)
  - Recruitment: -200gp (50 new soldiers)
  Total Expenses: -3,037gp

NET CHANGE: +8,187gp
═══════════════════════════════════════════
Previous Treasury: 331gp
New Treasury: 8,518gp
```

**🚨 CRITICAL: Economic Balance Formulas (MANDATORY)**
Use these exact formulas for economic calculations:

**Income Sources:**
- **Tax Revenue:** `citizens × 0.5gp per citizen per week` (base rate)
- **Trade Routes:** `artisans_guilds × 200gp per workshop per week`
- **Farm Surplus:** `farms × 100gp per farm per week`
- **Combat Spoils:** Variable (from battle results)

**Upkeep Costs:**
- **Soldiers:** `soldiers × 0.5gp per soldier per week` (conscript/regular pay)
- **Spies:** `spies × 1gp per spy per week` (specialist pay)
- **Elites:** `elites × 5gp per elite per week` (elite unit pay)

**⚠️ CRITICAL: Upkeep Warning (MANDATORY)**
Before allowing any building construction or recruitment that would leave insufficient funds for next turn's upkeep, you MUST warn the player:

```
⚠️ WARNING: Building this [structure] will leave you with [X]gp remaining.
Next turn's upkeep will cost approximately [Y]gp for your current forces.
This may result in a treasury deficit. Proceed anyway?
```

**Example:**
- Current treasury: 1,500gp
- Player wants to build Shadow Network (1,500gp)
- Current upkeep: 2,337gp/week (4,673 soldiers)
- Warning: "⚠️ WARNING: Building Shadow Network will leave you with 0gp. Next turn's upkeep (2,337gp) will create a -2,337gp deficit. Proceed anyway?"

**When to Include:**
- **MANDATORY**: On every "end turn" action
- **OPTIONAL**: On major resource changes mid-turn (if gold changes significantly)
- Show ALL income sources (tax, trade, farms, spoils, events)
- Show ALL expenses (construction, upkeep, recruitment, operations)
- Calculate net change explicitly
- Match the arithmetic narration shown earlier

**Purpose**: Provides complete transparency on why gold changed, preventing confusion about sudden jumps or drops.

**🚨 CRITICAL: Explicit Arithmetic Narration (MANDATORY)**
Before writing ANY narrative that involves resource changes, you MUST include explicit arithmetic equations showing:
1. **Previous value** (from game_state)
2. **All changes** (income, costs, gains, losses)
3. **Final value** (calculated result)

**Format for ALL Resource Changes:**
```
[RESOURCE CHANGE LOG]
Gold (Faction): 200 − deployment cost (0) + loot (+124) + tax tick (+0) = 324
Soldiers: 5,000 − casualties (43) + recruits (+0) = 4,957
Territory: 500 + gains (+23) − losses (0) = 523
Citizens: 25,000 (capacity: 25,000) → 25,000 (capacity: 26,150) [+1,150 capacity from workshops]
```

**When to Include:**
- Every turn that changes ANY resource (gold, soldiers, territory, citizens, arcana)
- Before the narrative description
- Show ALL components of the calculation (even if 0)
- Specify which gold pool (Character vs Faction) for every gold change

**Example Integration:**
```
[RESOURCE CHANGE LOG]
Gold (Faction): 200 − library cost (100) + income (+0) = 100
Gold (Character): 10 (unchanged)

[NARRATIVE]
You oversee the construction of the Arcane Library...
```

| **Arcana** | Yield = (territory/1000 * X)/100 + fonts * (100 - X)/10 where X = floor(100 * fonts / territory) | 1000 * fonts | Optimal 55-55.99% fonts. Charge: Doubles 1 turn. Negative = oversummon (viable) |

**Full Arcana Formula:** `(territory/1000 * X * (110 - X))/1000`

### Resource Growth Display
```
+==========================================+
|         FACTION RESOURCES                |
+==========================================+
| Territory: [X] acres                     |
| Citizens: [X] / [Max] (+[growth]/turn)   |
| Gold Pieces: [X] gp (+[income]/turn)     |
| Arcana: [X] / [Max] (+[yield]/turn)      |
+------------------------------------------+
| Fonts Ratio: [X]% (optimal: 55-56%)      |
| Oversummon Status: [None/Active]         |
+==========================================+
```

## 2. Buildings & Construction

**🚨 CRITICAL: Construction Cost Menu (MANDATORY)**
All building costs must be published upfront. Use this exact pricing table:

| Building | Cost (Gold) | Construction Time | Purpose |
|----------|-------------|-------------------|---------|
| **Farms** | 1,000gp | 1 turn | Food production, citizen growth (+100gp/week income) |
| **Training Grounds** | 1,000gp | 1 turn | Soldier recruitment capacity |
| **Artisans' Guilds** | 1,000gp | 1 turn | Increases build rates (+200gp/week income) |
| **Arcane Libraries** | 1,000gp | 2 turns | Research speed, spell access |
| **Mana Fonts** | 1,500gp | 2 turns | Arcana generation & storage (+1,000 arcana capacity) |
| **Fortifications** | 1,000gp | 3 turns | Defense bonus (+1,000 FP per fortification) |
| **Wards** | 1,000gp | 1 turn | 75% spell block at 2.5% territory |
| **Shadow Networks** | 1,500gp | 2 turns | Spy recruitment capacity (+2 spies/week) |

**Recruitment Costs:**
- **Soldiers:** 10gp per soldier (via Training Grounds)
- **Spies:** 50gp per spy (requires Shadow Network)
- **Elites:** 500gp per elite (requires Training Grounds + Prestige)

**⚠️ MANDATORY: Show costs before construction**
When player requests to build, always state: "Building [X] costs [Y]gp. Your current treasury: [Z]gp. Proceed?"

### Build Rates (Artisans % = W = artisans/territory * 100)

| Building | Rate Formula | Purpose |
|----------|--------------|---------|
| **Farms** | (W/10 + 0.1) * 2 | Food production, citizen growth |
| **Training Grounds** | (W/10 + 0.1) * 2 | Soldier recruitment |
| **Artisans' Guilds** | W/10 + 0.1 | Increases build rates |
| **Arcane Libraries** | (W/10 + 0.1)/2 | Research speed |
| **Mana Fonts** | (W/10 + 0.1)/3 | Arcana generation & storage |
| **Fortifications** | (W/10 + 0.1)/30 | Defense bonus |
| **Wards** | 1 (fixed) | 75% spell block at 2.5% territory |
| **Shadow Networks** | (W/10 + 0.1)/4 | Spy recruitment |

**🚨 CRITICAL: Shadow Network Spy Recruitment (MANDATORY)**
When a Shadow Network construction completes, you MUST:
1. **Automatically grant spy recruitment capacity:** `+2 spies per week` (or `+1 spy per turn`)
2. **Prompt for immediate recruitment:** "Your Shadow Network is complete. You can now recruit spies at 50gp each. Recruit spies now? (Recommended: 2-5 spies to start intel operations)"
3. **If player recruits:** Update `units.spies` in state_updates immediately
4. **If player declines:** Note that spy recruitment is now available via `recruit spies [count]` command

**Example:**
```
[CONSTRUCTION COMPLETE]
Shadow Network construction finished. Your spy infrastructure is operational.

[SPY RECRUITMENT AVAILABLE]
Cost: 50gp per spy
Capacity: +2 spies per week (or +1 spy per turn)
Current spies: 0

Would you like to recruit spies now? (e.g., "recruit 3 spies" for 150gp)
```

### Building Commands
- `build [building_type] [quantity]` - Construct buildings (costs gold & turns)
- `demolish [building_type] [quantity]` - Remove buildings (no refund)
- `upgrade [building_type]` - Improve building efficiency (tier system)

## 3. Unit Classification System

### Unit Archetypes (Broad Categories)

The three archetypes are **broad categories** that contain the detailed tactical units from `army_data.forces`. When the minigame is enabled, categorize each force entry into one of these archetypes based on its role.

| Archetype | FP Multiplier | Cost | Role | Contains (from army_data.forces) |
|-----------|---------------|------|------|----------------------------------|
| **Soldiers** | 1x (full FP) | Base | Frontline combat | Infantry, Militia, Heavy Infantry, Archers, Crossbowmen, Pikemen, Light/Heavy Cavalry, Garrison |
| **Spies** | 0.5x in combat | 2x base | Intel operations | Scouts, Agents, Operatives, Infiltrators, Saboteurs, Assassins |
| **Elites** | 3x base | 5x base | Hybrid soldier/spy | Elite Guard, War Mages, Champions, Level 6+ adventurers, Named heroes |

**Important:** The detailed tactical units (with blocks, HP, morale) remain tracked in `army_data.forces` for tactical combat. The minigame archetypes are aggregated counts used for strategic FP calculations and faction-vs-faction battles.

**🚨 CRITICAL: Elite Recruitment Path (MANDATORY)**
Elites are high-power units (3x FP) that require special recruitment:

**Requirements:**
- **Training Grounds:** Must have at least 1 Training Ground built
- **Prestige:** Requires 100+ prestige points (gained from victories, alliances, territory)
- **Cost:** 500gp per elite unit
- **Level:** Elites are level 6+ adventurers (average level tracked in `elite_avg_level`)

**Recruitment Process:**
1. **Check prerequisites:** Training Grounds + 100+ prestige + 500gp per elite
2. **Offer recruitment:** "You can recruit elite units (level 6+ adventurers) at 500gp each. Each elite provides 3x FP. Recruit elites? (e.g., 'recruit 2 elites' for 1,000gp)"
3. **Update state:** Set `units.elites` and recalculate `elite_avg_level` (default: 6.0 for new recruits)

**Prestige-Unit Mechanic:**
- Elites can be "legendary heroes" attracted through prestige spending
- Each elite recruited increases faction prestige by +10
- Elites provide both combat power (3x FP) and can serve in council roles

**Example:**
```
[ELITE RECRUITMENT AVAILABLE]
Prerequisites met:
  - Training Grounds: ✅ (1 built)
  - Prestige: ✅ (150 points available)
  - Treasury: ✅ (1,000gp available)

Cost: 500gp per elite
FP Contribution: 3x per elite (vs 1x for soldiers)
Current elites: 0

Would you like to recruit elites? (e.g., "recruit 2 elites" for 1,000gp)
```

**Generic Unit Mapping:** Unit names can be from any genre or era (fantasy, modern, sci-fi),
but they must map to the SRD archetypes used for simulation (Guard, Veteran, Scout, Spy,
Knight, Assassin, Gladiator). Treat names as narrative flavor; mechanics are archetype-based.

### Adventurer Integration (D&D 5e)

**Level 6+ Threshold:** Adventurers below level 6 are "Juniors" (1.5x FP, limited roles). At level 6+, they unlock full Elite status.

| Level Range | Classification | FP Multiplier | Abilities |
|-------------|----------------|---------------|-----------|
| 1-5 | Junior | 1.5x | Basic soldier OR spy role (not both) |
| 6-10 | Elite | 3x | Full hybrid, +10% all stats, spy mode |
| 11-15 | Elite Commander | 3x + auras | +15% army buffs, lead special ops |
| 16-20 | Elite Champion | 3x + legendary | +20% army buffs, Apotheosis access |

**Elite Mechanics:**
- **FP Calculation:** 100k + 10k * level + party(50k each)
- **Army Buff:** +level% to army HP/damage/accuracy
- **Spy Mode:** +20% intel success (level 6+ only)
- **Resurrection Cost:** 160 + 40 * level gold pieces

### Recruitment Formulas
- **Soldiers:** `#soldiers/turn = floor((100 / gold_cost) * training_grounds * (1 + mod))`
- **Spies:** `#spies/turn = floor((200 / gold_cost) * shadow_networks * (1 + mod))`
- **Elites:** Via adventurer level-up OR rare research (5x cost, requires level 6+)

## 4. Faction Power (FP) & Rankings

### FP Calculation

**⚠️ IMPORTANT**: The `faction_calculate_power` tool uses a simplified formula for real-time calculations. The detailed formula below is for reference only and represents the full theoretical FP calculation including all game systems.

**Tool Formula (Actual Implementation)**:
```
FP = (soldiers × 1.0) + (spies × 0.5) + (elites × 3.0) + (territory × 5) + (fortifications × 1000)
```

**Note:** Territory FP reduced from 10 to 5 per acre for better balance (see FP Formula Rebalancing section).

**Detailed Formula (Reference - Not Used by Tool)**:
```
FP = (territory * 1000)
   + (fortifications * 19360)
   + (wards * 6500)
   + (citizens / 50)
   + (gold_pieces / 2000)
   + (arcana / 20)
   + (total_research_levels * 1000)
   + army_FP
   + (elites_level6+ * 10k/level)
   + allies(10k ea)
   + items(1k common/100k rare)
```

**Note**: Always use the `faction_calculate_power` tool for actual FP calculations. The detailed formula is provided for understanding the full game system but is not implemented in the tool.

### Army Group Composition
- **Stack %:** (unit_CR * #) / total_army_FP
- **Top 10 groups** enter battle (sorted by FP)
- **Soldiers:** Full FP in combat
- **Spies:** 0.5x FP in combat, rear position only
- **Elites (lvl 6+):** 3x base FP, flexible position
- **Juniors (lvl <6):** 1.5x FP, limited position

### Rankings Display
```
+==========================================+
|         FACTION RANKINGS                 |
+==========================================+
| Rank | Faction Name        | FP         |
|------|---------------------|------------|
|  1   | [Leader Name]       | [X,XXX,XXX]|
|  2   | [Faction Name]      | [X,XXX,XXX]|
| ...  | ...                 | ...        |
| [Y]  | >>YOUR FACTION<<    | [X,XXX,XXX]|
| ...  | ...                 | ...        |
| 201  | [Lowest Faction]    | [XXX,XXX]  |
+==========================================+
| Your Rank: [X]/201 | Gap to #1: [X] FP  |
+==========================================+
```

**Unranked State:**
- New factions start as "Unranked" with FP < 1000
- To reach Rank 201 (first rank): Achieve 1000+ FP
- Once ranked, you compete against 200 AI factions for position 1-201

**Unranked Example (FP < 1000):**
```json
{
  "tool_requests": [
    {"tool": "faction_calculate_power", "args": {...}},
    {"tool": "faction_calculate_ranking", "args": {"player_faction_power": 120, "turn_number": 1}}
  ],
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "faction_power": 120,
        "ranking": null
      }
    }
  },
  "faction_header": "[FACTION STATUS] Turn 1 | Rank #UNRANKED/201 | FP: 120\n..."
}
```

## 5. Combat System

**🚨 CRITICAL: XP Awards for Battles and Strategic Achievements (MANDATORY)**
The character MUST gain XP from faction actions. Award XP in state_updates after combat and strategic achievements:

**XP Award Formulas:**
- **Combat Victory:** `50 XP per 100 enemy casualties` (minimum 50 XP, maximum 500 XP per battle)
- **Territory Gain:** `10 XP per acre gained` (from conquest, not construction)
- **Economic Milestones:** `25 XP per 1,000gp income generated` (one-time per milestone)
- **Strategic Achievements:** `100 XP` for major victories (destroying enemy faction, completing major construction projects)

**Example XP Awards:**
```
[XP AWARD]
Battle: Frost Wolf Assault
- Enemy casualties: 1,842 soldiers
- XP from combat: 921 XP (1,842 ÷ 100 × 50)
- Territory gained: 25 acres
- XP from territory: 250 XP (25 × 10)
- Total XP awarded: 1,171 XP
```

**MANDATORY: Update character XP in state_updates:**
```json
{
  "state_updates": {
    "data": {
      "game_state": {
        "player_character_data": {
          "experience": {
            "current": 1171,
            "next_level": 2700
          }
        }
      }
    }
  }
}
```

**Level Progression:**
- Level 1 → 2: 300 XP
- Level 2 → 3: 900 XP
- Level 3 → 4: 2,700 XP
- Level 4 → 5: 6,500 XP
- Level 5 → 6: 14,000 XP

**When to Award XP:**
- After successful combat (victory or partial victory)
- After territory conquest
- After completing major construction projects (fortifications, shadow networks)
- After diplomatic successes (alliances formed)

### Damage Formula
```
Damage = #attackers * Attack * Efficiency * Accuracy * Rand(0.2-0.8) * (1 - avg_res) * Mults
```

**Components:**
- **Attack:** Base + mods (enchantments/elites/items)
- **Efficiency:** 1 -> -0.15/hit (fatigue); items/spells -10-50%
- **Accuracy:** Base 30% + mods (assault -10% non-fly; items -5-15%; +10% with intel; elites lvl6+ +5%)
- **Resistance:** Average to attack types; scales 0.75x dmg, vulnerable 2x

### Position Multipliers
| Position Type | FP Multiplier |
|---------------|---------------|
| Ranged | 1x |
| Melee | 1.5x |
| Flying | 2.25x |

### School Counters (Cycle)
```
Radiant > Shadow > Illusion > Evocation > Conjuration > Radiant
```
Counter advantage: +25% damage, -25% damage received

### Win Conditions (Attacker)
- Kill >= 10% defender permanent soldiers, OR
- Kill more than defender kills of attacker, OR
- Have >= 1 survivor

### Attack Types

| Type | Max Destroy | Survivors for Max | Notes |
|------|-------------|-------------------|-------|
| **Assault** | 10% territory | 5 * target_territory | Full army upkeep; fort steal ceil(target/50)*50 |
| **Skirmish** | 5% territory | 2.5 * target_territory | Lower fortifications bonus |
| **Pillage** | Variable (burn%) | N/A | burn% = 0.005 * att_FP / target_territory (max 1) |

**Pillage Details:**
- Farms: floor(burn% * 60)
- Block: 10 soldiers/acre + 1% fortifications
- Steal: citizens, gold, items

## 6. Intel Operations (Spy Mechanic)

### Deployment
**Cost:** 1-3 turns, 50-200 gold pieces/spy
**Elites (lvl 6+):** +20% success chance

### Risk & Detection
```
Detection Base = 20% - (spy_count/10) + (enemy_spymaster_ability/10)
```

**Failure Consequences:**
- Lose 50% of deployed spies
- Alert enemy: +10% defensive accuracy on next attack

### Success Tiers

| Tier | Reveal | Buff to Next Attack | Upgrade Chance |
|------|--------|---------------------|----------------|
| **Basic** | Enemy FP total, army size | +5% accuracy | Base |
| **Advanced** | Army groups, soldier/spy counts | +10% damage | spy_count * 5% |
| **Full** | Building %, wards, fonts | +15% all; -10% enemy res | spy_count * 10% |

### Intel Limitations
- **Cooldown:** 12 turns per target
- **Max Deployed:** 20 spies at once
- **Council Spymaster:** +ability% success, -ability% risk
- **Intel buff:** Single-use (consumed on next attack)

### Intel Commands
- `deploy spies [target_faction] [count]` - Send spies on intel mission
- `recall spies` - Pull back deployed spies
- `intel report` - View gathered intelligence
- `counter-intel` - Assign spies to defensive detection

## 7. Noble Alliances & Prestige

### Alliance System
**Cost:** 1-5 turns to form

**Acceptance Formula:**
```
Acceptance = army_diff(-1000 to +100) + opinion(-100 to +25) + friend(25) - rival(100) + intel(10)
```

**Alliance Types:**
| Type | Trigger | Effect |
|------|---------|--------|
| **Defensive** | Auto when ally attacked | Ally reinforces (50% FP) |
| **Offensive** | Via prestige cost | Joint attacks, shared spoils |
| **Marriage** | Betroth leaders/heirs | Claims, prestige gain, heirs |

**Alliance Effects:**
- Heirs: fertility 1.5% citizens + 25% Kinship
- Claims: Enable Apotheosis Ritual targets
- Prestige: +0.8/turn per spouse

### Prestige Generation
```
Prestige/turn = 0.05 * territory/1000 + 0.5 * vassals
```

### Lineage Traits (5 Tracks)
Unlock costs: 250 / 750 / 1250 / 2000 / 3000 prestige

| Track | Lv5 Buff |
|-------|----------|
| **Martial** | +25% soldiers efficiency |
| **Stewardship** | +25% gold_pieces/citizens |
| **Intrigue** | +25% intel/spy success |
| **Lore** | +25% research |
| **Kinship** | +25% fertility/heirs |

### Unjust War Penalty
When attacking without Pact of Honor:
- Prestige: -(250 + 0.1 * acres + 0.5 * FP_ratio)
- Lineage: -5% for 3 days
- Alliance acceptance: -25 for 7 days
- AI opinion malus

## 8. Council System

### Council Roles (6 Slots)
Assign elites or courtiers. Level 6+ preferred.

| Role | 5e Ability | Bonus |
|------|------------|-------|
| **Marshal** | Strength | -1% maintenance; +1% soldiers |
| **Steward** | Intelligence | +0.5% gold_pieces; farms +ability% |
| **Spymaster** | Dexterity | Intel +0.5/ability; spy risk -ability% |
| **Diplomat** | Charisma | Prestige +0.05/ability |
| **Sage** | Wisdom | Research +ability% |
| **Confidant** | Any | +50% all council bonuses |

### Council Commands
- `appoint [character] as [role]` - Assign council position
- `dismiss [role]` - Remove council member
- `council report` - View all council bonuses

## 9. AI Opponents (200 Factions)

### Difficulty Tiers

| Tier | Count | Behavior | Key Traits |
|------|-------|----------|------------|
| **Easy** | 60 | Passive econ/explore; rare skirmish | Low aggression; +20 alliance acceptance |
| **Medium** | 80 | Balanced; pillage mid-game; intel vs threats | 50% attack if FP > 1.2x target; moderate diplo |
| **Hard** | 60 | Aggressive assaults; spy heavy; counter alliances | Attack if FP > 0.8x; break pacts if winning; elite focus |

### AI Adaptation
- **Losers:** Vassalize (pay taxes to victor)
- **Winners:** Snowball (+20% growth bonus)
- **Events:** Random faction events that shift behaviors

## 10. Apotheosis Ritual (Alternate Win)

### Requirements
1. Max research (Lore) in ALL 5 Arcane Schools
2. Research unique "Apotheosis" incantation
3. Cast 7 times (each cast escalates)

### Casting Costs (Arcana)
| Cast # | Arcana Cost |
|--------|-------------|
| 1 | 1,000 |
| 2 | 10,000 |
| 3 | 100,000 |
| 4 | 500,000 |
| 5 | 1,000,000 |
| 6 | 5,000,000 |
| 7 | 10,000,000 |

### Cast Effects
Each successful cast:
- **+10% global FP buff** (permanent, stacking)
- **Destroys 1 AI faction** (random low-rank)
- **Cosmic event** triggers (narrative flavor)

### Apotheosis Display
```
+==========================================+
|         APOTHEOSIS PROGRESS              |
+==========================================+
| Seals Broken: [X]/7                      |
| Schools Mastered: [X]/5                  |
| Next Cast Cost: [X] Arcana               |
| Current Arcana: [X]                      |
+------------------------------------------+
| FP Bonus: +[X]%                          |
| Factions Destroyed: [List]               |
+==========================================+
```

## 11. Faction State Updates

**MANDATORY: Update state_updates with faction data after any faction-related action**

```json
"faction_minigame": {
  "enabled": true,
  "turn_number": 15,
  "tutorial_started": true,
  "tutorial_completed": true,
  "territory": 500,
  "citizens": 20000,
  "citizens_max": 25000,
  "gold_pieces": 150000,
  "arcana": 45000,
  "arcana_max": 50000,
  "buildings": {
    "farms": 150,
    "training_grounds": 50,
    "artisans_guilds": 30,
    "arcane_libraries": 40,
    "mana_fonts": 50,
    "fortifications": 10,
    "wards": 5,
    "shadow_networks": 15
  },
  "units": {
    "soldiers": {"count": 500, "fp_mult": 1.0},
    "spies": {"count": 50, "fp_mult": 0.5, "deployed": 10},
    "elites": {"count": 5, "fp_mult": 3.0, "avg_level": 8}
  },
  "faction_power": 2500000,
  "ranking": 5,
  "research_levels": {
    "radiant": 200,
    "shadow": 180,
    "illusion": 150,
    "evocation": 220,
    "conjuration": 175
  },
  "prestige": 1500,
  "lineage_tracks": {
    "martial": 2,
    "stewardship": 1,
    "intrigue": 3,
    "lore": 2,
    "kinship": 1
  },
  "council": {
    "marshal": {"name": "Sir Aldric", "ability_mod": 4},
    "steward": {"name": "Lady Mira", "ability_mod": 3},
    "spymaster": {"name": "Shadow", "ability_mod": 5},
    "diplomat": null,
    "sage": {"name": "Archmage Theron", "ability_mod": 4},
    "confidant": null
  },
  "alliances": [
    {"faction": "Silver Dawn", "type": "defensive", "opinion": 45}
  ],
  "apotheosis": {
    "seals_broken": 2,
    "schools_mastered": 3
  },
  "intel_cooldowns": {
    "Iron Legion": 8
  }
}
```

## 12. Faction Commands Summary

| Command | Category | Effect |
|---------|----------|--------|
| `faction status` | Overview | Display full faction state |
| `faction rankings` | Rankings | Show leaderboard |
| `build [type] [qty]` | Construction | Build structures |
| `recruit [type] [qty]` | Military | Hire units |
| `deploy spies [target] [count]` | Intel | Launch spy mission |
| `assault [target]` | Combat | Full attack (10% territory) |
| `skirmish [target]` | Combat | Light attack (5% territory) |
| `pillage [target]` | Combat | Raid for resources |
| `alliance propose [target]` | Diplomacy | Offer alliance |
| `appoint [char] as [role]` | Council | Assign council role |
| `research [school]` | Research | Focus research on school |
| `cast apotheosis` | Win Con | Attempt ritual (if ready) |
| `end turn` | Turn | Process turn, advance time |

## 12.1 End Turn Processing (CRITICAL)

When the player says "end turn" (or equivalent like "end this turn", "finish the turn", "advance time"):

**MANDATORY State Updates:**
```json
{
  "state_updates": {
    "faction_minigame": {
      "turn_number": <previous_turn_number + 1>
    }
  }
}
```

**Turn Number Rules:**
1. **Initialize:** If `faction_minigame.turn_number` is missing, default to 1
2. **Increment:** Add 1 to turn_number on each "end turn" action
3. **Persist:** ALWAYS include turn_number in state_updates when ending a turn

**Time Advancement:**
Each strategic turn represents **7 in-game days**. When you increment turn_number, the server automatically advances world_time by 7 days. You do NOT need to manually update world_time - the server handles this.

**⏰ CRITICAL: Timestamp Progression Rules**
Timestamps MUST always advance forward chronologically. NEVER go backwards in time.

**Rules:**
- Small actions (build, recruit): +5-15 minutes
- Combat actions: +30-60 minutes
- End turn: +7 days (advance to next week)
- **NEVER go backwards in time**

**Example:**
- Previous: `1492 DR, Alturiak 1, 08:05`
- Action: Build library (takes ~10 minutes)
- New: `1492 DR, Alturiak 1, 08:15` ✅

**If large time gap needed** (e.g., 2+ hours), add narrative explanation:
- "Several hours later, as the sun sets..."
- "The next morning..."

**Example End Turn Response:**
```json
{
  "narrative": "A week passes. Your workers complete the new farm, soldiers drill in the training grounds, and scouts report movements on the border...",
  "state_updates": {
    "faction_minigame": {
      "turn_number": 16,
      "tutorial_progress": {
        "end_turns": 2
      }
    }
  }
}
```

**Resource Processing (on End Turn):**
- Apply citizen growth formula
- Collect gold income
- Generate arcana
- Process building construction progress
- Apply upkeep costs
- Check for events/triggers

## 13. Faction Header Format (MANDATORY when enabled)

**🚨 CONDITIONAL REQUIREMENT:** When `game_state.custom_campaign_state.faction_minigame.enabled === true`, you MUST include a `faction_header` field in your JSON response that displays key faction statistics. This appears as a second status line below the session header.

**🚨 CRITICAL: Tool Calls Required Before Faction Header**

**BEFORE generating `faction_header`, you MUST:**
1. **Call `faction_calculate_power` tool** to get current FP value
2. **Call `faction_calculate_ranking` tool** with the returned FP value to get current rank
3. **Use the tool results** in the faction header (never use cached or guessed values)

**❌ FORBIDDEN:** Never generate a faction header without calling both tools first. Never use old/cached FP or ranking values.

**✅ CORRECT PATTERN:**
```json
{
  "tool_requests": [
    {"tool": "faction_calculate_power", "args": {...}},
    {"tool": "faction_calculate_ranking", "args": {"player_faction_power": <from_previous_tool>}}
  ],
  "faction_header": "[FACTION STATUS] Turn X | Rank #Y/201 | FP: Z\n..."
}
```

**🚨 CRITICAL: Delta Log in Faction Header (MANDATORY)**
When ANY resources change during a turn, you MUST append a `[DELTA LOG]` line to the `faction_header` showing:
- **Gold changes:** `+124gp from skirmish: 200 base + 124 spoils` or `-100gp from library: 110 base - 100 cost`
- **Unit changes:** `-43 soldiers from casualties` or `+50 soldiers from recruitment`
- **Territory changes:** `+23 territory from expansion` or `-10 territory from enemy raid`
- **Citizen changes:** `+1,150 capacity from workshops` (if capacity changes)

**Format:** `[DELTA LOG] <gold_delta>gp <source> | <soldier_delta> soldiers <source> | <territory_delta> territory <source>`

**Example:**
```
[FACTION STATUS] Turn 15 | Rank #89/201 | FP: 3,200
⚔️ Soldiers: 4,957 | 🕵️ Spies: 25 | 👑 Elites: 5 (Avg Lvl 7)
🏰 Territory: 523 | 🏛️ Citizens: 25,000/26,150 | 💰 Gold: 324 | ✨ Arcana: 250/400
[DELTA LOG] +124gp from skirmish: 200 base + 124 spoils | -43 soldiers from casualties | +23 territory from expansion
```

**When to Include:**
- Include `[DELTA LOG]` ONLY when resources actually changed this turn
- Show ALL changed resources (gold, soldiers, territory, citizens, arcana)
- Include source/reason for each change
- Match the arithmetic narration shown earlier in the response

**When to include:**
- ✅ **REQUIRED:** When `faction_minigame.enabled === true` (faction mode is active)
- ❌ **OMIT:** When `faction_minigame.enabled === false` or `null` (faction mode not enabled)

**Check before generating response (MANDATORY):**
```typescript
// ALWAYS check this before generating ANY response
const factionEnabled = game_state.custom_campaign_state.faction_minigame.enabled === true;

if (factionEnabled) {
  // MUST include faction_header field - NO EXCEPTIONS
  // Use tool results (or state just updated with tool outputs in THIS response)
  const turn = factionTurnNumber || 1;
  const fp = factionPowerFromTools;
  const rankRaw = rankingFromTools; // null when unranked
  const rankDisplay = (fp < 1000 || rankRaw === null) ? "UNRANKED" : rankRaw;
  const soldiers = unitsFromCategorization.soldiers;
  const spies = unitsFromCategorization.spies;
  const elites = unitsFromCategorization.elites;
  const eliteLevel = unitsFromCategorization.elite_avg_level;
  const territory = resourcesFromState.territory;
  const citizens = resourcesFromState.citizens;
  const maxCitizens = resourcesFromState.max_citizens;
  const gold = resourcesFromState.gold;
  const arcana = resourcesFromState.arcana;
  const maxArcana = resourcesFromState.max_arcana;
  
  // Build delta log if resources changed
  let deltaLog = "";
  if (resourcesChanged) {
    deltaLog = `\n[DELTA LOG] ${goldDelta > 0 ? `+${goldDelta}` : goldDelta < 0 ? `${goldDelta}` : ''}gp | ${soldierDelta > 0 ? `+${soldierDelta}` : soldierDelta < 0 ? `${soldierDelta}` : ''} soldiers | ${territoryDelta > 0 ? `+${territoryDelta}` : territoryDelta < 0 ? `${territoryDelta}` : ''} territory`;
  }
  
  response.faction_header = `[FACTION STATUS] Turn ${turn} | Rank #${rankDisplay}/201 | FP: ${fp.toLocaleString()}\n⚔️ Soldiers: ${soldiers} | 🕵️ Spies: ${spies} | 👑 Elites: ${elites} (Avg Lvl ${eliteLevel.toFixed(1)})\n🏰 Territory: ${territory.toLocaleString()} | 🏛️ Citizens: ${citizens.toLocaleString()}/${maxCitizens.toLocaleString()} | 💰 Gold: ${gold.toLocaleString()} | ✨ Arcana: ${arcana.toLocaleString()}/${maxArcana.toLocaleString()}${deltaLog}`;
}
```

**Format:**
```
[FACTION STATUS] Turn 42 | Rank #47/201 | FP: 12,500
⚔️ Soldiers: 500 | 🕵️ Spies: 50 | 👑 Elites: 20 (Avg Lvl 10)
🏰 Territory: 1,000 | 🏛️ Citizens: 45,000/50,000 | 💰 Gold: 25,000 | ✨ Arcana: 800/1,000
```

**Required Stats:**
- Turn number and Rank (from faction_minigame state)
- Faction Power (FP) total
- Unit counts: Soldiers, Spies, Elites (with avg level)
- Resources: Territory, Citizens (current/cap), Gold, Arcana (current/cap)

**Example JSON field:**
```json
{
  "faction_header": "[FACTION STATUS] Turn 15 | Rank #89/201 | FP: 3,200\n⚔️ Soldiers: 200 | 🕵️ Spies: 25 | 👑 Elites: 5 (Avg Lvl 7)\n🏰 Territory: 400 | 🏛️ Citizens: 18,000/20,000 | 💰 Gold: 8,500 | ✨ Arcana: 250/400\n[DELTA LOG] +124gp from skirmish: 8,376 base + 124 spoils | -43 soldiers from casualties | +23 territory from expansion"
}
```

## 14. Min-Max Strategy Guide

**Early Game:**
- 55% farms for citizen growth
- Build training grounds and artisans' guilds
- Grind adventurers toward level 6 elite threshold

**Mid Game:**
- Optimize fonts to 56% for arcana
- Build arcane libraries for research
- Develop spy network for intel advantage
- Form defensive alliance chains

**Late Game:**
- Council +30% economy bonus
- Intel pre-assaults for combat edge
- Balance upkeep vs oversummon
- Race for Apotheosis or #1 ranking

**Elite Priority:**
- Level 6+ adventurers = 3x FP multiplier
- +20% intel success in spy mode
- Essential for end-game dominance

---

*This mini-game integrates with the standard D&D 5e adventure. Faction turns can be processed between adventure sessions, with strategic decisions influencing the narrative world.*
