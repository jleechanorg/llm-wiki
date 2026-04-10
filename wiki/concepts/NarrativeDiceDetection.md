---
title: "Narrative Dice Detection"
type: concept
tags: [dice-integrity, nlp, parsing]
sources: [dice-logging-functions-unit-tests]
last_updated: 2026-04-08
---

## Definition
The process of scanning narrative text (non-structured response text) for patterns that indicate dice rolls were performed, such as:

- Explicit notation: "1d20", "2d6", "d100"
- Natural language: "rolled a 15", "got a seven", "the die shows 18"
- Contextual: "attack roll", "saving throw", "damage roll"

## Detection Behavior
- **When Found**: Logs DICE_NARRATIVE_DETECTED at info level
- **Without Evidence**: Flags as narrative dice fabrication if no tool/code execution
- **With Evidence**: Validates against structured response dice_rolls field

## Related Concepts
- [[DiceFabricationDetection]] — uses detection results
- [[StructuredResponseParsing]] — parsing structured dice data
