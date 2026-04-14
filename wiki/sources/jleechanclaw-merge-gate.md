---
title: "jleechanclaw-merge-gate"
type: source
tags: [jleechanclaw, merge, deprecated]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/merge_gate.py
---

## Summary
DEPRECATED. Merge gate checks moved to agent-orchestrator's merge-gate.ts. Provides no-op stubs with DeprecationWarning for backward compatibility. All functions log deprecation warnings and return safe defaults. ConditionResult and MergeVerdict dataclasses preserved but marked as deprecated.

## Key Claims
- Deprecated in favor of AO's checkMergeGate() which covers: CI green, mergeable, CR approved, no blocking comments
- Evidence gate and openclaw approval also deprecated (AO handles these)
- check_merge_ready returns empty MergeVerdict with warnings
- Main entry point: ao verify <session-id>

## Connections
- [[jleechanclaw-pr-review-decision]] — related to PR merge workflow

## Contradictions
- Deprecated module is superseded by AO merge-gate.ts