---
title: "Dice Values Are Unknowable — Code Execution Protocol"
type: source
tags: [dice, code-execution, verification, gemini, random]
source_file: "raw/dice-values-unknowable-code-execution-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Critical protocol requiring dice values to be obtained via code execution in Gemini 3 code_execution mode. Dice results are quantum-random and cannot be predicted, estimated, or fabricated — code must execute `random.randint()` to generate values. Responses without RNG calls are rejected upon inspection.

## Key Claims
- **Unknowable Rule**: Dice values are un-knowable without code execution — like checking real-world temperature, must query the RNG to observe the value
- **Code Inspection**: Responses are inspected for `random.randint()`; absence triggers rejection
- **DC Ordering**: DC must be assigned BEFORE `random.randint()` call for skill checks and saving throws — reversed ordering is flagged as unfair
- **Damage on Hit**: Damage dice only rolled if attack hits — no RNG calls on miss

## Key Quotes
> "Your code IS INSPECTED. If `random.randint()` is not found in your executed code, your response WILL BE REJECTED"

> "DC assignment MUST appear BEFORE random.randint() in your code"

> "If the attack misses, DO NOT roll damage dice. No RNG calls for damage on a miss."

## Protocol Formats

### Attack Roll
```python
import json, random, time
random.seed(time.time_ns())
roll = random.randint(1, 20)
modifier = 5
total = roll + modifier
ac = 15  # Target AC
print(json.dumps({"notation": "1d20+5", "rolls": [roll], "modifier": modifier, "total": total, "label": "Longsword Attack", "ac": ac, "hit": total >= ac}))
```

### Damage Roll (Only if Hit)
```python
import json, random, time
random.seed(time.time_ns())
attack_roll = random.randint(1, 20)
attack_mod = 5
attack_total = attack_roll + attack_mod
ac = 15
hit = attack_total >= ac

damage_total = 0
damage_roll = None
if hit:
    damage_roll = random.randint(1, 8)
    damage_total = damage_roll + 3
```

### Skill Check (DC + Reasoning)
```python
import json, random, time
random.seed(time.time_ns())
dc = 15
dc_reasoning = "guard is alert but area is noisy"
roll = random.randint(1, 20)
modifier = 3
total = roll + modifier
success = total >= dc
```

### Saving Throw (DC + Reasoning)
```python
import json, random, time
random.seed(time.time_ns())
dc = 15
dc_reasoning = "Dragon breath weapon (CR 10, standard DC 15)"
roll = random.randint(1, 20)
modifier = 4
total = roll + modifier
success = total >= dc
```

## DC Ordering Enforcement
**CORRECT:**
```python
dc = 15                        # DC set FIRST
dc_reasoning = "..."           # Reasoning BEFORE roll
roll = random.randint(1, 20)   # RNG call AFTER DC
```

**WRONG (flagged):**
```python
roll = random.randint(1, 20)   # RNG first = violation
dc = 15                        # DC after roll = unfair
```

## Additional Rules
- **Advantage/Disadvantage**: Show both dice, indicate which was used
- **Opposed Checks**: Show both sides' rolls, declare winner
- **Social Checks**: Consider NPC personality, relationship, plausibility
