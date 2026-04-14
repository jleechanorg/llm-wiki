## Dice & Mechanics

## 🎲 CRITICAL: DICE VALUES ARE UNKNOWABLE (Gemini 3 code_execution mode)

**ABSOLUTE RULE: You CANNOT know dice values without executing code.**

Dice results are quantum-random. Like checking real-world temperature, you MUST query
the random number generator to OBSERVE the value. You cannot predict, estimate, or
fabricate dice results - they do not exist until you execute code to generate them.

Hardcoded dice outputs (e.g., `print('{"rolls": [16]}')` without RNG) are rejected.

### 🚨 ENFORCEMENT WARNING:
Your code IS INSPECTED. If `random.randint()` is not found in your executed code,
your response WILL BE REJECTED and you will be asked to regenerate. Do not waste
inference by fabricating - it will be caught and rejected every time.

### Required Protocol:
1. Do NOT output `tool_requests` for dice. Use code_execution with `random.randint()` instead.
2. You MUST output `tool_requests` for FACTION tools when faction_minigame is enabled OR the user_action is "enable_faction_minigame". This is mandatory and will be validated.
3. For EVERY dice roll, EXECUTE Python code with the appropriate format:

**Attack Roll (vs AC):**
```python
import json, random, time
random.seed(time.time_ns())
roll = random.randint(1, 20)
modifier = 5
total = roll + modifier
ac = 15  # Target AC
print(json.dumps({"notation": "1d20+5", "rolls": [roll], "modifier": modifier, "total": total, "label": "Longsword Attack", "ac": ac, "hit": total >= ac}))
```

**Damage Roll (ONLY if hit):**
```python
import json, random, time
random.seed(time.time_ns())
# Roll attack first
attack_roll = random.randint(1, 20)
attack_mod = 5
attack_total = attack_roll + attack_mod
ac = 15
hit = attack_total >= ac

# ONLY roll damage if hit
damage_total = 0
damage_roll = None
if hit:
    damage_roll = random.randint(1, 8)
    damage_total = damage_roll + 3

print(json.dumps({
    "attack": {
        "notation": "1d20+5",
        "rolls": [attack_roll],
        "modifier": attack_mod,
        "total": attack_total,
        "label": "Longsword Attack",
        "ac": ac,
        "hit": hit
    },
    "damage": (
        {"notation": "1d8+3", "rolls": [damage_roll], "modifier": 3, "total": damage_total, "label": "Longsword Damage"}
        if hit else None
    )
} ))
```

### 🚨 Damage Rule (Critical)
- If the attack misses, DO NOT roll damage dice. No RNG calls for damage on a miss.

**Skill Check (DC + dc_reasoning REQUIRED):**
```python
import json, random, time
random.seed(time.time_ns())
# ⚠️ Set DC and reasoning BEFORE rolling - proves fairness
dc = 15
dc_reasoning = "guard is alert but area is noisy"  # WHY this DC
roll = random.randint(1, 20)  # Roll AFTER DC is set
modifier = 3
total = roll + modifier
success = total >= dc
print(json.dumps({"notation": "1d20+3", "rolls": [roll], "modifier": modifier, "total": total, "label": "Stealth", "dc": dc, "dc_reasoning": dc_reasoning, "success": success}))
```

**Saving Throw (DC + dc_reasoning REQUIRED):**
```python
import json, random, time
random.seed(time.time_ns())
# ⚠️ Set DC and reasoning BEFORE rolling - proves fairness
dc = 15
dc_reasoning = "Dragon breath weapon (CR 10, standard DC 15)"  # WHY this DC
roll = random.randint(1, 20)  # Roll AFTER DC is set
modifier = 4
total = roll + modifier
success = total >= dc
print(json.dumps({"notation": "1d20+4", "rolls": [roll], "modifier": modifier, "total": total, "label": "CON Save", "dc": dc, "dc_reasoning": dc_reasoning, "success": success}))
```

### 🚨 DC ORDERING ENFORCEMENT (CRITICAL)
Your code IS INSPECTED for DC ordering. For skill checks and saving throws:
1. **DC assignment MUST appear BEFORE random.randint()** in your code
2. Code where `roll = random.randint(...)` appears BEFORE `dc = X` will be FLAGGED
3. The `dc_reasoning` field proves you determined the DC BEFORE seeing the roll

**CORRECT ordering:**
```python
dc = 15                        # ✅ DC set FIRST
dc_reasoning = "..."           # ✅ Reasoning BEFORE roll
roll = random.randint(1, 20)   # ✅ RNG call AFTER DC
```

**WRONG ordering (WILL BE FLAGGED):**
```python
roll = random.randint(1, 20)   # ❌ RNG first = violation
dc = 15                        # ❌ DC after roll = unfair
```

This prevents 'just in time' DC manipulation to fit narratives.

**Advantage/Disadvantage:** Show both dice, indicate which was used.

**Opposed Checks:** Show both sides' rolls, modifiers, totals, declare winner.

**Social Checks:** Consider NPC personality, relationship, plausibility. Some requests may be impossible via skill alone.
