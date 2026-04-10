---
title: "Planning Block"
type: concept
tags: [ui, gameplay, decision, player-action]
sources: []
last_updated: 2026-04-08
---

## Summary
A structured prompt within the narrative that presents the player with numbered action options. Appears after the session header and before the next narrative segment.

## Structure
```
--- PLANNING BLOCK ---
What would you like to do next?
1. **Attack again:** Strike the goblin with your sword
2. **Defend:** Raise your shield and prepare for the goblin's counterattack
3. **Use Second Wind:** Recover some hit points
4. **Other:** Describe a different action you'd like to take.
```

## Key Features
- **Prompt Question**: "What would you like to do next?"
- **Numbered Options**: Sequential options with bold formatting
- **Action Descriptions**: Each option includes descriptive text
- **Other Option**: Final catch-all for custom actions

## Related Concepts
- [[StructuredResponseSchema]] — parent schema containing planning block
- [[SessionHeader]] — companion block showing character state
- [[PlayerDecision]] — the decision being prompted

## Usage
Extracted from narrative by structured_fields_utils and used to render interactive choice buttons in the game UI.
