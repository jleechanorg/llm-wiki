---
title: Dice Integrity
type: entity
tags: [anti-fabrication, dice, dnd, verification]
date: 2026-05-16
---

## Summary
Anti-fabrication system that enforces LLM never fabricates dice roll results. LLM requests rolls via code execution; Gemini sandbox resolves them; server validates. File: [dice_integrity.py](https://github.com/jleechanorg/worldarchitect.ai/blob/main/mvp_site/dice_integrity.py) (1,566 lines).

## Key Mechanism
1. LLM generates Python code: `import random; result = random.randint(1,20) + 5`
2. Gemini code-execution sandbox runs it
3. Structured response contains `action_resolution.mechanics.rolls[]`
4. `dice_integrity.py` validates: scans for narrative dice notation, `[dice:...]` tags, "rolls a 15" patterns
5. Warns on fabrication — never hard-blocks

## Connections
- [[WorldArchitectAI]] — uses this system
- [[WorldArchitect System Architecture v3.0]] — §4.4
