---
title: "State Commands"
type: concept
tags: [token-pattern, game-state, prompt-engineering]
sources: [narrative-sample-token-analysis]
last_updated: 2026-04-08
---

State commands are tokens that trigger specific game state modifications or queries. They are used to communicate changes to character attributes, inventory, location, or other persistent game data.

## Related Patterns
- Implemented via [[GameStateInstructionTokens]]
- Often contain [[JSONFragments]] for structured data
- Part of the broader token system including [[DeletionTokens]] and [[MarkupTokens]]
