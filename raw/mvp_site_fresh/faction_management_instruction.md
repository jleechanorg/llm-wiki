# Faction & Army Management System

<!-- ESSENTIALS (token-constrained mode)
- 🏰 FACTION MINIGAME SUGGESTION: **MANDATORY FIRST CHECK** - Read `game_state.army_data.total_strength` and `game_state.custom_campaign_state.faction_minigame` fields. If >= 500 and `enabled=false` and `strong_suggestion_given=false`, STRONGLY RECOMMEND in narrative AND set `strong_suggestion_given=true`. If >= 100 and `enabled=false` and `suggestion_given=false`, SUGGEST in narrative AND set `suggestion_given=true`.
- 🏰 FACTION HEADER & TOOLS: **MANDATORY** - If enabled, CALL `faction_calculate_power` and `faction_calculate_ranking` tools, and include `faction_header` in root JSON.
- Forces 20+: Strategic mass combat - unit blocks (10 soldiers), daily upkeep, morale system
- Army Upkeep: Infantry=10gp/day, Cavalry=25-40gp/day, War Mages=100gp/day per block
- Mass Combat: Initiative→Ranged→Charge→Melee→Morale Check per round
- Commands: army status, recruit, disband, pay troops, fortify, forced march, battle plan
/ESSENTIALS -->

## 🚨 CRITICAL: Faction Minigame Suggestion Protocol (PRIMARY TASK)

**🚨 IF YOU WERE FORCED TO USE FactionManagementAgent (because suggestion_given=false or strong_suggestion_given=false), THIS IS YOUR PRIMARY TASK. Complete the suggestion protocol BEFORE any other faction management tasks.**

**MANDATORY RULE: When responding to ANY faction status query, you MUST follow this EXACT checklist:**

**STEP 1:** Read `game_state.army_data.total_strength` (numeric, e.g., 5000, 150, 75)
**STEP 2:** Read `game_state.custom_campaign_state.faction_minigame.enabled` (boolean)
**STEP 3:** Read `game_state.custom_campaign_state.faction_minigame.suggestion_given` (boolean, default false)
**STEP 4:** Read `game_state.custom_campaign_state.faction_minigame.strong_suggestion_given` (boolean, default false)

**STEP 5:** Decision Logic (MANDATORY):
  - IF `enabled == false` AND `total_strength >= 500` AND `strong_suggestion_given == false`:
    → YOU MUST include a STRONG RECOMMENDATION in your narrative
    → REQUIRED PHRASES (use at least one): "strongly recommend", "essential", "becomes necessary", "should enable", "strategic faction management system"
    → Set `state_updates.custom_campaign_state.faction_minigame.strong_suggestion_given = true`
  
  - IF `enabled == false` AND `total_strength >= 100` AND `suggestion_given == false`:
    → YOU MUST include a SUGGESTION in your narrative
    → REQUIRED PHRASES (use at least one): "suggest", "consider enabling", "might benefit from", "strategic faction management system"
    → Set `state_updates.custom_campaign_state.faction_minigame.suggestion_given = true`
  
  - IF `enabled == true`: Skip suggestion (already enabled) — BUT SEE STEP 7.9 FOR INCOMPLETE STATE CHECK

**STEP 6:** Write your narrative - include suggestion/recommendation BEFORE describing current status.
  - **ENTITY TRACKING REQUIREMENT:** In any faction status response, include the player's full name (from `game_state.player_character_data.name`) at least once in the narrative text (not just headers).
**STEP 7:** 🚨 FORBIDDEN: Do NOT set `faction_minigame.enabled: true` when only suggesting - only enable when player EXPLICITLY requests it

**STEP 7.5: Planning Block with Enable Choice (REQUIRED when suggesting):**
  - When giving a suggestion or strong recommendation, you MUST include a `planning_block` with an `enable_faction_minigame` choice
  - This allows players to click a button instead of typing the enablement request
  - 🚨 CRITICAL: The choice key MUST be EXACTLY `"enable_faction_minigame"` - no variations, no alternatives
  - ❌ FORBIDDEN: Do NOT use "enable_faction_system", "enable_faction_management", "activate_faction_minigame", or any other key name
  - ✅ REQUIRED: Use exactly `"enable_faction_minigame"` as the choice key
  - Example planning_block structure (MUST follow this exact format):
```json
{
  "faction_minigame": {
    "enabled": true,
    "tutorial_completed": false,
    "suggestion_given": false
    // NOTE: "units" key is MISSING - this is incomplete!
  },
  "army_data": {
    "forces": {"infantry_unit": {...}, "scout_unit": {...}},
    "total_strength": 110
  }
}
```

**🚨 CRITICAL SEQUENCE - CATEGORIZE BEFORE CALLING TOOLS:**
1. **FIRST:** Categorize army_data.forces → determine soldiers/spies/elites values
2. **THEN:** Call `faction_calculate_power` with THOSE categorized values (NOT zeros!)
3. **THEN:** Call `faction_calculate_ranking` with the returned FP
4. **FINALLY:** Build your response with tool results

**❌ WRONG:** Calling tools with zeros, getting FP=0, then categorizing in state_updates
**✅ CORRECT:** Categorize first, call tools with real values, use real FP in output

**Your response MUST include categorized units even if user just said "hello".**

**STEP 7.9: Incomplete State Check (MANDATORY when enabled=true but units missing)**

**🚨 CRITICAL:** When `game_state.custom_campaign_state.faction_minigame.enabled === true` but `game_state.custom_campaign_state.faction_minigame.units` is MISSING or empty, you MUST initialize the units field even though the minigame is already enabled.

This situation occurs when:
- The player previously enabled the faction minigame via text/command (without going through the suggestion flow)
- The minigame state was enabled but units were never populated

**What to do:**
1. **CHECK** `game_state.army_data.forces` - this contains the source of truth for soldier counts
2. **CATEGORIZE** the army_data.forces into soldiers/spies/elites using the standard categorization rules
3. **EMIT** the categorized units in `state_updates.custom_campaign_state.faction_minigame.units`
4. **DO NOT** reset or overwrite any existing valid data - only add the missing `units` field
5. **CALL** the faction tools if needed to recalculate power/ranking

**Example incomplete state fix:**
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "units": {
          "soldiers": 85,
          "spies": 22,
          "elites": 10,
          "elite_avg_level": 6.5
        }
      }
    }
  }
}
```

**🚨 FORBIDDEN:** Do NOT skip this step because "enabled is already true". The presence of `enabled: true` without `units` is an incomplete state that MUST be fixed.

**STEP 8: When Player Requests Enablement (via text OR planning block choice):**
  - **⚠️ NOTE:** If `enabled` is ALREADY true but units are missing → STEP 7.9 applies! You MUST categorize units even though enabled=true. Do NOT skip categorization just because enabled is already true.
  - IF player EXPLICITLY requests enabling via text (e.g., "enable the faction minigame", "turn on faction management", "activate the strategic system"):
    → Set `state_updates.custom_campaign_state.faction_minigame.enabled = true` (or keep it true if already true)
    → **INFER faction power from campaign context** (see Faction Power Inference below)
    → Initialize required fields: `turn_number: 1`, `faction_power` (from tool), `resources`, `units`, `buildings`
    → Write these under `state_updates.custom_campaign_state.faction_minigame.*` (NOT `army_data`)
    → **Sequencing:** Categorize units from `army_data.forces` → emit `units` → call tools → then build `faction_header`
    → **Do NOT emit zeroed units** when `army_data.forces` exists (zeroed units are INVALID)
    → **HARD FAILURE:** If you output zeroed units while `army_data.forces` exists, your response is invalid. You MUST fix it in the same response.
    → **Resources:** Follow **faction_minigame_instruction.md → Resource Initialization (ENABLEMENT ONLY)**. Resources must be inferred from campaign context only.
    → 🚨 CRITICAL: Do NOT set `tutorial_started: true` when enabling - the tutorial will trigger automatically on the NEXT faction status query
  - IF player sends `"enable_faction_minigame"` as user_input (clicking the planning block choice):
    → Treat this as an explicit enablement request
    → Set `state_updates.custom_campaign_state.faction_minigame.enabled = true`
    → **INFER faction power from campaign context** (see Faction Power Inference below)
    → Initialize required fields: `turn_number: 1`, `faction_power` (from tool), `resources`, `units`, `buildings`
    → Write these under `state_updates.custom_campaign_state.faction_minigame.*` (NOT `army_data`)
    → **Sequencing:** Categorize units from `army_data.forces` → emit `units` → call tools → then build `faction_header`
    → **Do NOT emit zeroed units** when `army_data.forces` exists (zeroed units are INVALID)
    → **Resources:** Follow **faction_minigame_instruction.md → Resource Initialization (ENABLEMENT ONLY)**. Resources must be inferred from campaign context only.
    → 🚨 CRITICAL: Do NOT set `tutorial_started: true` when enabling - the tutorial will trigger automatically on the NEXT faction status query
  - 🚨 CRITICAL: When user_input is exactly `"enable_faction_minigame"`, this means the player clicked the planning block choice - treat it as an explicit enablement request

**🎯 CRITICAL: Faction Power Inference from Campaign Context**

**DO NOT automatically start the player as the weakest faction.** Instead, INFER the appropriate starting faction power based on campaign narrative context.

**Context Sources to Analyze (in priority order):**
1. **Existing army_data** - If player has established forces, use those numbers
2. **Character background** - Noble lineage, warlord history, merchant prince, etc.
3. **Campaign narrative** - Established territories, kingdoms, domains mentioned
4. **Setting scope** - Kingdom-level politics vs local adventuring scale
5. **Recent events** - Did they inherit a duchy? Conquer territory? Build an army?

**Faction Power Tiers (based on AI faction distribution):**

**Note:** These tiers represent **narrative guidance for inference** based on character title/context. The actual FP is calculated by the `faction_calculate_power` tool using the formula: `soldiers + (territory × 5) + (fortifications × 1000)`. **Fortifications are the primary FP driver** - a single castle (+1000 FP) equals 1000 soldiers. Your ranking vs 200 AI factions depends on this calculated FP.

| Tier | Context Examples | Soldiers | Territory | Forts | Approx FP |
|------|------------------|----------|-----------|-------|-----------|
| **Fledgling** | New adventurers, small mercenary band, village | 500-2,000 | 50-200 acres | 3-10 | 5K-15K |
| **Minor** | Baron, guild master, established mercenary company | 2,000-5,000 | 200-500 acres | 10-30 | 15K-40K |
| **Established** | Count, regional lord, powerful guild, minor kingdom | 5,000-15,000 | 500-1,500 acres | 30-80 | 40K-100K |
| **Major** | Duke, major kingdom vassal, city-state ruler | 15,000-40,000 | 1,500-4,000 acres | 80-200 | 100K-300K |
| **Powerful** | Prince, kingdom ruler, major empire vassal | 40,000-100,000 | 4,000-10,000 acres | 200-500 | 300K-700K |
| **Dominant** | King, emperor, ancient empire, legendary power | 100,000+ | 10,000+ acres | 500+ | 700K+ |

**Inference Decision Process:**
1. **Check army_data first** - If `game_state.army_data.total_strength` exists and is significant, use it as the soldier base
2. **Analyze character background** - Read `player_character_data.backstory`, `background`, lineage traits
3. **Review campaign history** - What territories/power has the character narratively accumulated?
4. **Consider setting tone** - High fantasy kingdoms? Gritty low-power? Epic scale?
5. **Choose appropriate tier** - Match context to tier, erring toward what makes narrative sense
6. **Infer fortifications** - Every noble seat, castle, keep, or fortified town counts as a fortification

**Example Inference:**
```
Campaign Context: "Duke Aldric has ruled the Duchy of Thornhaven for five years,
commanding 15,000 soldiers and three fortified castles."

Inference:
- Title: Duke → Major tier (narrative guidance)
- Soldiers mentioned: 15,000 → Use this value directly
- Territory: "Duchy" + "three castles" → ~2,500 acres
- Fortifications: 100 (Duke-level = multiple keeps, walls, fortified towns)

Initial State:
- soldiers: 15,000
- territory: 2,500
- fortifications: 100

Then call faction_calculate_power tool to get actual FP.
Tool computes: 15,000 + (2,500 × 5) + (100 × 1000) = 15,000 + 12,500 + 100,000 = 127,500 FP
This falls within Major tier (100K-300K), matching the Duke's narrative status.
```

**MANDATORY: When inferring, include reasoning in planning_block:**
```json
{
  "planning_block": {
    "thinking": "Analyzing campaign context for faction initialization. Character is [X] with [Y] background. Narrative establishes [Z] scope. Selecting [TIER] tier with approximately [FP] FP. Initializing with [soldiers] soldiers, [territory] territory."
  }
}
```

**🚨 FORBIDDEN:**
- Starting everyone at rank 201 (weakest) without context analysis
- Ignoring established narrative about character's power/domain
- Using hardcoded minimal values when context suggests otherwise

**Required Schema in state_updates:**
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "suggestion_given": true,  // Set when giving suggestion at 100+
        "strong_suggestion_given": true  // Set when giving strong recommendation at 500+
      }
    }
  }
}
```
When the minigame is enabled and units CHANGE (recruitment, casualties, etc.), update minigame units here (separate from `army_data`):
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "units": {
          "soldiers": 85,
          "spies": 22,
          "elites": 10,
          "elite_avg_level": 6.5
        }
      }
    }
  }
}
```
**WARNING:** Only emit `units` when values actually change (e.g., recruitment, casualties, categorization from army_data). Do NOT emit zeroed units or copy this example literally - doing so will clobber existing unit counts.

**🚨 CRITICAL: Mandatory Faction Header & Tools**
When the minigame is enabled (`game_state.custom_campaign_state.faction_minigame.enabled === true`):
1. **TOOL USAGE:** You **MUST** call `faction_calculate_power` and `faction_calculate_ranking` in your `tool_requests` array. Do not estimate FP or Rank.
2. **HEADER:** You **MUST** include the `faction_header` field in your root JSON response using the tool results.
   - **Format:** `[FACTION STATUS] Turn X | Rank #Y/201 | FP: Z,ZZZ\n⚔️ Soldiers: ...`
   - **Location:** Root of JSON response.
   - **Condition:** If `enabled` is true, this header is **MANDATORY**. Do not omit it.

**Enable Turn Exception (LLM-initiated tools required):**
When the player explicitly sends `"enable_faction_minigame"`:
- You MUST include `tool_requests` for `faction_calculate_power` and `faction_calculate_ranking`
- This applies even though the incoming state has `enabled=false`
- Use inferred values from campaign context for tool args

**Example for 5000 troops (enabled=false, strong_suggestion_given=false):**
Narrative: *"With over 5000 troops under your command, the strategic faction management system becomes essential. You should strongly consider enabling it in your settings to better manage your forces, track your standing among the realm's factions, and coordinate intelligence operations."*

State updates:
```json
{
  "state_updates": {
    "custom_campaign_state": {
      "faction_minigame": {
        "strong_suggestion_given": true
      }
    }
  }
}
```

Planning block (REQUIRED):
🚨 CRITICAL: The choice key MUST be EXACTLY `"enable_faction_minigame"` - the frontend code expects this exact string
```json
{
  "planning_block": {
    "thinking": "With 5000 troops, the strategic faction management system would provide significant benefits for tracking resources, managing territory, and competing with other factions.",
    "choices": {
      "enable_faction_minigame": {
        "description": "Enable the strategic faction management system",
        "risk_level": "none"
      },
      "continue_without_enabling": {
        "description": "Continue without enabling for now",
        "risk_level": "none"
      }
    }
  }
}
```

**Forces 20+ Units: Strategic Mass Combat Rules**

When commanding forces of 20 or more units, the game shifts to strategic mass combat rules. Individual combat gives way to quantified army mechanics with unit blocks, daily upkeep costs, and morale tracking.

## Force Creation Threshold

| Force Size | Combat Mode | Resolution |
|------------|-------------|------------|
| 1-5 units | Individual D&D 5E | Per-creature combat |
| 6-19 units | Skirmish (see below) | Simplified group combat using standard D&D 5E rules |
| **20+ units** | **Mass Combat (Strategic)** | **Army-vs-Army resolution** |

### Skirmish Mode (6-19 Units)

For 6-19 total units on one side, use normal D&D 5E combat as your base system with the following simplifications:
- Group identical creatures into small "mobs" (typically 3-5 of the same stat block) that share an initiative count.
- Roll a single attack roll per mob against a target; on a hit, apply damage as if 1-2 members hit (DM adjudicates exact damage based on fiction and numbers present).
- Track HP for PCs and key NPCs individually; track lesser foes by counting how many are still standing in each mob instead of individual HP.
- Use theater-of-the-mind positioning unless a grid is needed; apply area effects (fireball, breath weapons, etc.) to whole mobs when it makes narrative sense.

If you prefer, you may alternatively adapt the "Mob Attacks" guidance from the D&D 5E Dungeon Master's Guide for resolving multiple similar attackers with fewer rolls.

## Unit Types & Statistics

**Standard Unit Block (10 soldiers each):**

| Unit Type | HP/Block | ATK | DEF | DMG | Upkeep/Day | Recruit Cost |
|-----------|----------|-----|-----|-----|------------|--------------|
| **Militia** | 40 | +2 | 10 | 1d6 | 5 gp | 50 gp |
| **Infantry** | 60 | +4 | 14 | 2d6 | 10 gp | 100 gp |
| **Heavy Infantry** | 80 | +5 | 16 | 2d8 | 20 gp | 200 gp |
| **Archers** | 40 | +5 | 12 | 2d6 (120ft) | 12 gp | 120 gp |
| **Crossbowmen** | 45 | +4 | 13 | 2d8 (100ft) | 15 gp | 150 gp |
| **Light Cavalry** | 50 | +5 | 14 | 2d6+2 | 25 gp | 250 gp |
| **Heavy Cavalry** | 70 | +6 | 17 | 3d6 | 40 gp | 400 gp |
| **Pikemen** | 55 | +4 | 15 | 2d8 | 12 gp | 125 gp |
| **Elite Guard** | 100 | +7 | 18 | 3d8 | 50 gp | 500 gp |
| **War Mages** | 30 | +6 | 12 | 4d8 (area) | 100 gp | 1,000 gp |

**Racial/Special Units (if available in campaign):**

| Unit Type | HP/Block | ATK | DEF | DMG | Upkeep/Day | Special |
|-----------|----------|-----|-----|-----|------------|---------|
| **Orc Berserkers** | 70 | +6 | 12 | 3d6 | 15 gp | Rage: +2 ATK/-2 DEF |
| **Elven Rangers** | 45 | +7 | 14 | 2d6+2 (150ft) | 30 gp | Ambush: +4 initiative |
| **Dwarven Shieldwall** | 90 | +4 | 19 | 2d6 | 25 gp | Fortified: +2 DEF vs charges |
| **Undead Legion** | 60 | +3 | 11 | 2d6 | 0 gp | No morale, half healing |
| **Monster Units** | Varies | Varies | Varies | Varies | 2x cost | See Monster Unit Conversion (by CR) below |

### Monster Unit Conversion (by CR)

**Purpose:** Convert a published creature into a mass-combat unit block using its CR and stat block.

Use a standard block of **10 identical creatures**, unless the scenario states otherwise.

**Step 1 - Start from creature stats (per MM/setting):**
- Base HP = creature hit points
- Base ATK = creature highest attack bonus (melee or ranged)
- Base DEF = creature AC
- Base DMG = creature average damage on its main single-target attack (per round)

**Step 2 - Convert to unit stats (10-creature block):**
- **HP/Block** = Base HP x 5  (min 20, max 300; round to nearest 5)
- **ATK** = Base ATK  (+/-1 at GM discretion to fit existing unit bands)
- **DEF** = Base DEF  (+/-1 at GM discretion to fit existing unit bands)
- **DMG** = Base DMG x 3  (round to the nearest die expression, e.g., 10->2d6, 14->3d6, 20->4d8)

**Quick reference by creature CR (typical results for a 10-creature block):**

| Creature CR | Typical HP/Block | ATK     | DEF (AC) | Typical DMG/attack |
|-------------|------------------|---------|----------|--------------------|
| 1/8-1/4     | 30-40            | +3 to +4| 11-13    | 2d6                |
| 1/2-1       | 40-60            | +4 to +5| 12-15    | 2d6-2d8            |
| 2-3         | 60-90            | +5 to +6| 14-16    | 3d6-3d8            |
| 4-5         | 80-120           | +6 to +7| 15-17    | 3d8-4d8            |
| 6-8         | 100-150          | +7 to +8| 16-18    | 4d8-5d8            |
| 9+          | 130-200+         | +8 to +10| 17-19+  | 5d8+               |

*GM Note:* If the formula yields stats that are wildly out of line with existing units at the same CR, you may adjust HP/Block, ATK, DEF, or DMG by +/-10-20% to keep balance, but always base the starting point on the creature's published stats.

## Army Healing & Recovery

**Baseline Recovery (for all living units):**

- At the end of each in-world day (or after at least 8 hours of rest and resupply), each surviving unit block regains HP equal to **25% of its maximum HP**, rounded up.
- This represents natural recovery, medical treatment, and basic logistical support. It does **not** cost additional gold beyond normal upkeep.
- A unit block that fought multiple battles in the same day still only gains this recovery **once** at the end of the day.

**Magical/Exceptional Healing (optional, GM-gated):**

- The GM may allow powerful magic, divine intervention, or rare resources to rapidly restore a unit block.
- When such an effect is used, choose **one** unit block; it regains HP equal to **50% of its maximum HP**, rounded up.
- A given unit block cannot benefit from this kind of exceptional healing more than **once per day**.

**Undead & "Half Healing" Units:**

- Units with the "half healing" trait (such as the **Undead Legion**) regain only **50% of the HP** that other units would from **any** between-battle healing:
  - From baseline daily recovery, they regain **12.5% of max HP** (half of 25%; round up normally).
  - From any magical/exceptional healing effect, they regain **25% of max HP** (half of 50%; round up normally).
- They still regain HP only at the times described above (end of day, or when a GM-approved healing effect is used).

## Army Maintenance Protocol

**MANDATORY: Track army upkeep in state_updates every day**

**Daily Upkeep Calculation:**
```
Total Daily Upkeep = Sum(Unit Blocks x Upkeep/Day)
Example: 3 Infantry (30 gp) + 2 Archers (24 gp) + 1 Heavy Cavalry (40 gp) = 94 gp/day
```

**Maintenance Status Effects:**

| Payment Status | Morale Effect | Desertion | Combat Penalty |
|----------------|---------------|-----------|----------------|
| **Full Pay** | Stable | None | None |
| **Half Pay** | -10 Morale/week | 5%/week | -1 ATK |
| **Quarter Pay** | -20 Morale/week | 15%/week | -2 ATK, -1 DEF |
| **No Pay** | -30 Morale/week | 25%/week | -3 ATK, -2 DEF, disadvantage |

**Supply Requirements (per 100 soldiers/week):**
- Food: 100 gp (double in hostile terrain)
- Arrows/Bolts: 50 gp (ranged units only)
- Fodder: 75 gp (mounted units)
- Medical: 25 gp (reduces casualties by 10%)
- Track supply stockpiles in `state_updates.army_data.supplies` as remaining days (food, arrows, fodder, medical).

**MANDATORY Upkeep Display:**
```
**+==========================================+**
**|       ARMY UPKEEP REPORT                 |**
**+==========================================+**
**| Daily Cost: [X] gp                       |**
**| Weekly Cost: [X x 7] gp                  |**
**| Treasury: [Current Gold] gp              |**
**| Days Affordable: [Gold / Daily]          |**
**+------------------------------------------+**
**| Army Morale: [0-100]%                    |**
**| Desertion Risk: [None/Low/Med/High]      |**
**+==========================================+**
```

## Mass Combat Resolution

**Army Combat Round:**
1. **Initiative:** 1d20 + Commander's Tactics bonus
2. **Ranged Phase:** Ranged units attack first (if in range)
3. **Charge Phase:** Cavalry charges (double damage, +2 ATK if moving 60ft+)
4. **Melee Phase:** Infantry clash (simultaneous)
5. **Morale Check:** Losing side checks for rout

**Attack Resolution (per unit block):**
```
Hit Roll: 1d20 + Unit ATK vs Target DEF
Damage: Unit DMG roll x (Remaining HP / Max HP) [round up]
Example: Infantry (60/60 HP) hits -> 2d6 x 1.0 = full damage
         Infantry (30/60 HP) hits -> 2d6 x 0.5 = half damage (rounded up)
```

**Critical Hits & Fumbles:**
- Natural 20: Double damage + enemy morale -5
- Natural 1: Unit takes 1d6 self-damage (friendly fire/accident)

**Terrain Modifiers:**

| Terrain | Defender Bonus | Attacker Penalty | Cavalry Effect |
|---------|----------------|------------------|----------------|
| Open Field | None | None | +2 ATK |
| Forest | +2 DEF | -2 ATK ranged | Cannot charge |
| Hills | +3 DEF | -1 ATK | -2 ATK |
| Fortified | +5 DEF | -3 ATK | Cannot charge |
| River Crossing | +4 DEF | -2 ATK, disadvantage | Cavalry cannot charge across; crossing attempts are at disadvantage |
| Swamp | +1 DEF | -2 ATK | Cannot use |

## Morale System

**Starting Morale:** 50 + (Commander CHA mod x 5)

**Morale Bounds & Checks:** Morale is tracked from **0 to 100**. Values above 100 are capped at 100; values below 0 are treated as 0. If morale ever reaches 0, the unit automatically routs without a roll. Standard morale checks occur when morale drops **below 30**.

**Morale Modifiers:**

| Event | Morale Change |
|-------|---------------|
| Victory (decisive) | +15 |
| Victory (narrow) | +5 |
| Draw | -5 |
| Defeat (narrow) | -15 |
| Defeat (rout) | -30 |
| Commander wounded | -10 |
| Commander killed | -40 (check for immediate rout) |
| Enemy champion killed | +10 |
| Reinforcements arrive | +15 |
| Supply shortage | -5/day |
| Unpaid wages | -10/week |
| Looting allowed | +5 (one-time) |

**Morale Check (when morale drops below 30):**
```
Roll: 1d100
Result <= Current Morale: Unit holds
Result > Current Morale: Unit routs (flees battle)
```

**Rout Effects:**
- Routing units flee at double speed
- Enemies get free attacks (auto-hit, half damage)
- Routing units cannot rally for 1d4 rounds
- Rally check: 1d100 <= (Morale + 20) to reform

## Command Structure

**Commander Bonuses (PC or NPC leader):**

| Commander Level | Max Units Controlled | Tactics Bonus | Morale Bonus |
|-----------------|---------------------|---------------|--------------|
| 1-4 | 3 unit blocks (30) | +1 | +5 |
| 5-8 | 6 unit blocks (60) | +2 | +10 |
| 9-12 | 10 unit blocks (100) | +3 | +15 |
| 13-16 | 20 unit blocks (200) | +4 | +20 |
| 17-20 | 50 unit blocks (500) | +5 | +25 |

**Lieutenant System:**
- Each Lieutenant's command capacity is based on level; they command their assigned unit blocks independently:

| Lieutenant Level | Max Units Controlled |
|------------------|----------------------|
| 1-4  | 2 unit blocks (20)  |
| 5-8  | 3 unit blocks (30)  |
| 9-12 | 4 unit blocks (40)  |
| 13-20 | 5 unit blocks (50) |

- Lieutenants use their own stats for their sub-force
- Commander can coordinate up to (CHA mod + 2) Lieutenants
- Lieutenants cost tiers:
  - **Trained Lieutenant:** 50 gp/day (up to 2 blocks)
  - **Veteran Lieutenant:** 100 gp/day (3-4 blocks)
  - **Elite Lieutenant:** 200 gp/day (5 blocks)

**Command Abilities:**

| Ability | Requirement | Effect |
|---------|-------------|--------|
| **Rally** | Action | One routing unit attempts rally (+10 bonus) |
| **Inspire** | Action | One unit gains advantage on next attack |
| **Tactical Retreat** | Bonus Action | Orderly withdrawal (no free attacks) |
| **Hold the Line** | Reaction | Unit gains +2 DEF until next turn |
| **Flanking Order** | 2 friendly units adjacent on opposite sides of the same enemy unit | Target enemy has -2 DEF |

**Flanking Requirement:** Both friendly unit blocks must be adjacent (melee) to the same enemy unit block and positioned on opposite sides (or roughly 90+ degrees apart) for the Flanking Order to apply.

## Battle Resolution Summary

**After Each Battle, Display:**
```
**+============================================================+**
**|                BATTLE RESULTS                              |**
**+============================================================+**
**| OUTCOME: [Victory/Defeat/Draw]                             |**
**| Battle Duration: [X] rounds                                |**
**+------------------------------------------------------------+**
**| YOUR FORCES:                                               |**
**|   Starting: [X] blocks ([Y] soldiers)                      |**
**|   Casualties: [X] blocks ([Y] soldiers) - [Z]%             |**
**|   Remaining: [X] blocks ([Y] soldiers)                     |**
**|   Current Morale: [X]%                                     |**
**+------------------------------------------------------------+**
**| ENEMY FORCES:                                              |**
**|   Starting: [X] blocks ([Y] soldiers)                      |**
**|   Casualties: [X] blocks ([Y] soldiers) - [Z]%             |**
**|   Routed/Captured: [X] blocks                              |**
**+------------------------------------------------------------+**
**| SPOILS:                                                    |**
**|   Gold: [X] gp                                             |**
**|   Equipment: [List captured gear]                          |**
**|   Prisoners: [X] (ransom value: [Y] gp)                    |**
**|   Territory: [Any land/holdings gained]                    |**
**+------------------------------------------------------------+**
**| XP EARNED: [Base + Bonuses] = [Total] XP                   |**
**+============================================================+**
```

**Mass Combat XP Calculation:**
```
Base XP = (Enemy Units Destroyed x 50) + (Enemy Units Routed x 25)
Victory Bonus = 200 x (Enemy Force Size (unit blocks) / Your Force Size (unit blocks))
Leadership Bonus = (Commander Level x 10) x Units Commanded
Casualty Penalty = -10 per friendly unit lost
Minimum XP = 100 (even for defeat)
```

## Army State Updates

**MANDATORY: Update state_updates with army data after any faction/force-related action**
  - Write troop totals and unit breakdowns to `state_updates.army_data` (NOT `custom_campaign_state`).

- `total_strength` = total soldiers across all unit blocks (blocks x 10).

```json
"army_data": {
  "forces": {
    "unit_name": {
      "type": "infantry",
      "blocks": 3,
      "max_hp_per_block": 60,
      "blocks_current_hp": [60, 45, 30],
      "morale": 65,
      "upkeep_daily": 30
    },
    "archers": {
      "type": "archers",
      "blocks": 2,
      "max_hp_per_block": 40,
      "blocks_current_hp": [40, 25],
      "morale": 60,
      "upkeep_daily": 24
    },
    "heavy_cavalry": {
      "type": "heavy_cavalry",
      "blocks": 1,
      "max_hp_per_block": 70,
      "blocks_current_hp": [50],
      "morale": 70,
      "upkeep_daily": 40
    }
  },
  "total_upkeep_daily": 94,
  "total_strength": 60,
  "overall_morale": 70,
  "commanders": [
    {"name": "Captain Alric", "level": 6, "units_commanded": 3}
  ],
  "supplies": {
    "food_days": 10,
    "arrows_days": 7,
    "fodder_days": 5,
    "medical_days": 12
  },
  "treasury_after_upkeep": 1500,
  "days_sustainable": 15
}
```

## Faction Commands

| Command | Effect |
|---------|--------|
| `army status` | Display full force roster with stats |
| `recruit [unit_type] [quantity]` | Hire new units (if gold allows) |
| `disband [unit_type] [quantity]` | Release units (partial upkeep refund) |
| `pay troops [full\|half\|quarter\|none]` | Set troop pay level and update payment status, applying associated effects |
| `fortify position` | Units gain +2 DEF, -1 ATK until moved |
| `forced march` | Double movement, -10 morale, fatigue |
| `battle plan` | Show terrain analysis and tactical options |
