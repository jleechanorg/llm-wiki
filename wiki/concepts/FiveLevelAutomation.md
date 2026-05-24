---
title: "Five Level Automation"
type: concept
tags: [attractor-pattern, automation-ladder, dark-factory, levels]
date: 2026-05-24
---
## Overview
The Five-Level Automation ladder (Dan Shapiro, Jan 2026) borrows the NHTSA's driving automation levels for AI-assisted coding. It ranges from Level 0 (no AI) to Level 5 (the dark factory — lights off, nobody reviews the code).

## Key Properties
- **What**: A five-level framework for categorizing AI-assisted coding maturity
- **Why matters**: Provides a shared vocabulary for teams to understand where they are and where they're heading

| Level | Name | Description |
|-------|------|-------------|
| 0 | vi | No AI. Every character yours. |
| 2 | Pair Programming | Most "AI-native" developers are here. Productive, but you're still the bottleneck. |
| 4 | AI PM | You write specs, argue about specs, leave for 12 hours, check if the tests pass. |
| 5 | Dark Factory | Lights off. Nobody reviews the code. Nobody even looks at it. |

## Key Insight (from Shapiro/StrongDM)
1. You're not the person best qualified to write code anymore — the AI writes it
2. If you're still reviewing every PR, YOU are the bottleneck — stop reading the code
3. This creates enormous terrifying problems — quality, understanding, degradation
4. Solving those problems IS your actual job now

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[DanShapiro]] | Person | Authored the five-level framework |
| [[DarkFactory]] | Concept | Level 5 of the automation ladder |
| [[HealerAgent]] | Agent | Enables Level 5 by automating quality diagnosis |
| [[CXDB]] | Database | Enables Level 5 by providing observability without code reading |

## Connection to Attractor Pattern
The Five-Level ladder provides the maturity framework that the Attractor pattern operates within. Attractor tools (CXDB, Healer, DOT pipelines) are what you build at Level 4-5 to make the dark factory work.

## See Also
- [[DanShapiro]]
- [[DarkFactory]]
- [[HealerAgent]]
- [[CXDB]]
