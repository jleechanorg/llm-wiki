---
title: "Healer Agent"
type: concept
tags: [attractor-pattern, self-healing, observability, automation]
date: 2026-05-24
---
## Overview
The Healer is an automated diagnosis and fix agent in the Attractor/Dark Factory pattern. It watches CXDB, develops opinions about whether agent behaviors look right, clusters similar problems into diagnoses, and those diagnoses become investigations carried out by other agents that write prescriptions applied automatically.

## Key Properties
- **What**: Automated failure diagnosis and fix system that operates on CXDB data
- **Why matters**: Enables the dark factory — no human files the bug report, no human triages it, no human writes the fix
- **Process**: CXDB → cluster terminal failures by (node, outcome, output_hash) → emit prescription → apply fix → verify
- **Prefix routing**: gate_*, plan|implement|fix, holdout — internal namespace, not ZFC violation

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[CXDB]] | Database | Healer reads CXDB to identify failure clusters |
| [[DarkFactory]] | Pattern | Healer enables lights-off autonomous operation |
| [[StrongDM]] | Company | Built CXDB on Monday, Healer on Tuesday |

## Connection to Attractor Pattern
The Healer is what makes the dark factory viable at Level 5. Without automated failure diagnosis and fix, the human operator becomes the bottleneck reviewing agent outputs — exactly what the Attractor pattern is designed to eliminate.

## See Also
- [[CXDB]]
- [[AttractorPattern]]
- [[DarkFactory]]
- [[FiveLevelAutomation]]
