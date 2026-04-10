---
title: "Anti-Loop Rule"
type: concept
tags: [rule, game-mechanic, loop-prevention]
sources: [planning-loop-detection-social-encounters-red-tests.md, game_state_instruction.md]
last_updated: 2026-04-08
---

## Summary
Game rule that enforces execution after repeated similar user actions. If the same or similar action is selected twice, the system MUST execute on the second selection — never present a third round of options.

## Definition
- **Trigger**: User selects similar action 2+ times
- **Action**: Force execution with dice roll on second selection
- **Prohibition**: Never present third round of options

## Implementation
The test validates detection by:
1. Tracking conversation history
2. Identifying similar action keywords
3. Counting occurrences of similar user messages
4. When count >= 2, marking loop as detected

## Connection to Action Execution Rule
The Anti-Loop Rule is part of the broader [[ActionExecutionRule]] which states:
- Execute chosen action with dice rolls
- Do NOT present more sub-options

## Connections
- [[PlanningLoopDetection]] — bug this rule prevents
- [[ActionExecutionRule]] — parent rule
- [[DiceRoll]] — required outcome when rule triggers
- [[ConversationHistory]] — mechanism for detection
