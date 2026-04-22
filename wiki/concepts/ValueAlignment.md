---
title: "Value Alignment"
type: concept
tags: [value-alignment, chai, inverse-reinforcement-learning, cirl]
date: 2026-04-15
---

## Overview

Value Alignment is the goal of ensuring AI systems pursue goals that are aligned with human values. Stuart Russell's CHAI research is canonical — "Any initial formal specification of human values is bound to be wrong in important ways."

## Key Properties

- **CHAI**: Center for Human-Compatible AI (Stuart Russell, Anca Dragan, Pieter Abbeel)
- **CIRL**: Cooperative Inverse Reinforcement Learning — foundational framework for value alignment
- **Core insight**: "AI systems should be uncertain of their objectives, and should be deferent to humans" — Stuart Russell
- **Precautionary**: "We don't have to wait for such incidents to arise" — Partnership on AI

## Connection to Governance

Value alignment research directly informs governance constraint design. If we can't fully specify values upfront, governance systems need:
- Feedback loops to detect misalignment (Grok's critique #3)
- Async escalation for edge cases (not blocking)
- Versioned policy objects that can be corrected

## See Also
- [[CHAI]]
- [[CIRL]]
- [[GovernanceLayer]]