---
title: "PR #96: fix(agent-gemini): parse native JSON session format for done-signal (orch-cb3e)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-96.md
sources: []
last_updated: 2026-03-23
---

## Summary
Gemini CLI stores sessions as a top-level JSON object: `{ sessionId, messages: [{ type, content }, ...] }`. This is NOT JSONL. The existing `readLastJsonlEntry` helper reads the last non-empty line of the file — for Gemini's format that's always `}`, which is valid JSON but has no `type` field. So `getActivityState` returned `null` for all Gemini sessions, giving AO no signal that the agent completed its turn (bead: orch-cb3e).

## Metadata
- **PR**: #96
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +364/-125 in 6 files
- **Labels**: none

## Connections
