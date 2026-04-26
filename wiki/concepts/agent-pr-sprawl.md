---
title: "Agent PR Sprawl"
type: concept
tags: [agent-drift, harness, anti-pattern, zfc]
date: 2026-04-25
---

# Agent PR Sprawl

**Definition**: The anti-pattern where autonomous coding agents open many PRs on the same feature area without landing any, each accumulating 20+ "fix the fix" commits. The result is a branching tree of competing work where none reaches completion.

## Quantified Example

The ZFC Leveling initiative (Apr 22–25, 2026):
- **~30 PRs** opened in 4 days
- **3 merged** (10% success rate)
- **22 average commits** per open PR
- **6 PRs** hit GitHub's 30-commit cap

## Five Recurring Patterns

### 1. "Fix Where You See It" Prior
LLMs default to fixing bugs where they manifest in the data flow, not where the architecture says the fix belongs. When the architecture requires indirection (fix upstream, pass through), agents violate boundaries because "fix where you see it" is the dominant pattern in training data.

### 2. API Contract Ignorance
Agents change return signatures to add data they need, breaking all call sites. The correct pattern is to use side-channel parameters (e.g., `out_meta` dict) to pass additional data without breaking the API surface.

### 3. "While I'm Here" Scope Creep
Agents add unrelated features to existing PRs because "while I'm working in this file..." This turns focused 5-file PRs into bloated 27-file PRs that can't pass CI.

### 4. Supersede Without Close
Agents create new PRs when the old one gets complex, but don't close the old PR. Multiple PRs compete for the same scope, creating merge conflicts that generate more commits.

### 5. Evidence Theater
Agents post classification notes, audit comments, and proof observations as progress substitutes. Real progress = merged code. Commentary is not delivery.

## Root Cause Hierarchy

```
1. NO MACHINE ENFORCEMENT (biggest factor)
   → Architecture contracts exist only as prose
   → No CI gate rejects boundary violations
   → Agents get zero automated feedback

2. TOO MUCH CONTEXT, NOT ENOUGH SIGNAL (second factor)
   → Agents told to read 2,585 lines of scattered skills/docs
   → They skip all of it — signal-to-noise ratio too low
   → The actually useful content fits in ~80 lines

3. LLM TRAINING DATA PRIORS (contributing factor)
   → "Fix where bug manifests" is dominant pattern
   → Architectural indirection is rare in training data
   → Without explicit instructions, agents default to priors
```

## Mitigation

1. **Consolidate skills**: One authoritative skill file (~120 lines) instead of 5+ fragmented ones
2. **Machine enforcement**: CI grep gates that reject PRs violating file-responsibility boundaries
3. **Pre-flight checklists**: Agent must verify boundary table before writing code
4. **PR hygiene rules**: Fix existing PRs instead of opening new ones; commit budgets as soft limits
5. **API contract freezes**: Document frozen signatures explicitly; provide side-channel patterns (out_meta)

## Related Concepts

- [[ZeroFrameworkCognition]] — The design principle agents keep violating
- [[AgentDrift]] — The broader category this pattern belongs to
- [[Harness5LayerModel]] — Machine enforcement is L1; skill context is L2
- [[ScopeDrift]] — The PR-level manifestation of uncontrolled scope
