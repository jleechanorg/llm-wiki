---
title: "/contexte Command Universal Composition Fix"
type: source
tags: [slash-commands, universal-composition, built-in-commands, command-fix]
source_file: "raw/contexte-command-universal-composition-fix.md"
sources: []
last_updated: 2026-04-08
---

## Summary
The `/contexte` command attempted to use Universal Composition to invoke the built-in `/context` command, but this approach fails because Claude cannot directly invoke built-in slash commands from within responses. Solution updates both `/contexte` and `/review-enhanced` to use user-data driven approaches with direct implementation patterns.

## Key Claims
- **Universal Composition fails for built-in commands**: Claude cannot programmatically invoke built-in slash commands like `/context` from responses
- **User-data approach works**: `/contexte` now looks for recent `/context` output in conversation history and analyzes real usage data
- **Direct implementation pattern**: Working commands like `/review-enhanced` provide analysis directly rather than orchestrating built-in commands
- **Working vs aspirational**: Claims about `/reviewe` calling built-in `/review` were aspirational, not actual implementation

## Key Learnings
1. Built-in commands cannot be invoked programmatically by Claude from responses
2. Working commands provide direct analysis rather than trying to orchestrate built-in commands
3. Universal Composition is for custom command coordination, not built-in command access
4. User-driven data approach works better than attempting system integration

## Connections
- [[context-optimization-implementation-plan-phases-2-4]] — related context optimization work
- [[command-usage-last-30-days]] — command usage patterns this source analyzes
