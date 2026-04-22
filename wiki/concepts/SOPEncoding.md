---
title: "SOP Encoding"
type: concept
tags: [sop, meta-programming, multi-agent, prompt-engineering]
date: 2026-04-15
---

## Overview

SOP (Standardized Operating Procedures) Encoding is a pattern where human workflows are encoded as agent prompts or process sequences. [[MetaGPT]] is the canonical example — it assigns diverse roles to agents based on SOPs to reduce cascading hallucinations.

## Key Properties

- **Assembly line paradigm**: Different agent roles handle different SOP stages
- **Role assignment**: Agents assigned based on domain expertise matching SOP steps
- **Hallucination reduction**: Human-like verification at each SOP stage
- **Meta-programming**: SOPs encoded as prompts rather than code

## MetaGPT Example

```
SOP for bug fix:
1. Requirements Agent → understands bug report
2. Code Agent → implements fix
3. Test Agent → writes tests
4. Review Agent → validates fix
```

## Governance Connection

AO's evolve loop is an 8-phase SOP. Governance layer (GOVERNANCE.md, SCOPE.md) can be seen as encoding operating constraints as runtime-readable SOP supplements. PR #452 proposes loading these at the OBSERVE phase.

## See Also
- [[MetaGPT]]
- [[AutonomousAgentLoop]]
- [[GovernanceLayer]]
