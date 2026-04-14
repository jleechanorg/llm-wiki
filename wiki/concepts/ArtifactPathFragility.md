---
title: "Artifact Path Fragility"
type: concept
tags: [pairv2, bug-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The artifact path fragility pattern addresses the observation that weaker models may write artifacts to slightly different paths than specified in contracts. Strict file-path gating is fragile when models have varying path-following capabilities.

## Why It Matters

MiniMax coder wrote IMPLEMENTATION_READY to the wrong path despite the artifact contract containing the correct absolute path. This reveals that path-following is not guaranteed across all models. The pattern suggests using process exit as the primary signal rather than file existence.

## Key Technical Details

- **Root cause**: Model capability variance in path-following
- **Mitigation**: Trust process exit, treat signal files as hints not gates
- **Scope**: `.claude/pair/pair_execute_v2.py`
- **Related concepts**: LLMRecoverableWorkflow, ProcessExitSignal

## Related Beads

- BD-pairv2-artifacts-hard-fail
- BD-pairv2-flatten-session-dir
