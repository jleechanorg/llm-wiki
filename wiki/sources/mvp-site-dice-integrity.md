---
title: "mvp_site — Dice Integrity and Fabrication Detection"
type: source
tags: [worldarchitect-ai, dice, integrity, fabrication-detection, llm-authenticity, narrative-dice]
date: 2026-04-14
source_file: raw/mvp_site_all/dice_integrity.py
---

## Summary

Detects when an LLM fabricates dice rolls — writing dice notation into narrative text without actually executing the dice tool. Uses regex pattern matching on narrative text to find dice notation, then cross-references with structured response and code execution evidence. This is the primary mechanism for [[DiceAuthenticity]] enforcement.

## Key Claims

### Detection Patterns
| Pattern | Example | Detection Rule |
|---------|--------|--------------|
| `[dice:...]` tag | `[dice:1d20+5=17]` | Always detected |
| Dice notation | `1d20+5`, `4d6` | Always detected |
| "rolls a 15" | "She rolls a 15" | Only if context window contains attack/hit/damage/save/skill/check/initiative/AC/DC |

### Fabrication Decision
Fabrication = `has_dice_in_narrative AND NOT code_execution_used`
- If narrative contains dice but `code_execution_used=False` → **fabricated**
- If dice tool was actually called → legitimate

### Pattern Regexes
```python
DICE_ROLL_PATTERN = r"\b\d*d\d+(?:\s*[+\-]\s*\d+)?\b"
NARRATIVE_DICE_CONTEXT_PATTERN = r"\b(attack|hit|damage|save|saving throw|skill|check|initiative|ac|dc)\b"
```

### Scan Limits
- Narrative dice scan capped at 5000 characters (`_NARRATIVE_DICE_SCAN_MAX_CHARS`)
- Prevents performance issues on very long responses

## Connections

- [[DiceAuthenticity]] — the core principle this enforces
- [[mvp-site-dice]] — the dice tool this integrates with
- [[DiceRollDebugRegression]] — frontend gating bug that bypasses this
- [[mvp-site-action-resolution-utils]] — audit event extraction for dice
