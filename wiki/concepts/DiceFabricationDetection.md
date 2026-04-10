---
title: "Dice Fabrication Detection"
type: concept
tags: [dice-integrity, validation, llm-safety]
sources: [dice-logging-functions-unit-tests, dice-integrity-module-tests, code-execution-evidence-extraction-rng-verification-tests]
last_updated: 2026-04-08
---

## Definition
A validation system that detects when an LLM claims dice were rolled but provides no evidence of actual code execution or tool use. The system flags two primary violation types:

1. **Narrative Dice Fabrication**: Dice patterns found in narrative text without tool/code execution evidence
2. **Code Execution Fabrication**: Code was executed but random.randint() was not used, indicating dice values were manually specified

## How It Works

### Detection Pipeline
1. Parse structured response for dice_rolls field
2. Scan narrative text for dice patterns (e.g., "1d20", "rolled a 7")
3. Check for tool execution or code execution evidence
4. If dice found in narrative but no evidence → flag as fabrication
5. If code executed but no random source → flag as fabrication

### Logging Layers
- **Info**: Narrative dice detected (informational)
- **Debug/Warning**: Fabrication check details (toggleable)
- **Warning**: Fabrication violations detected (always logged)

## Related Concepts
- [[CodeExecutionVerification]] — verifying actual code execution
- [[NarrativeDiceDetection]] — detecting dice in narrative text
- [[DiceIntegrityModule]] — broader dice validation system
