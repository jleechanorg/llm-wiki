---
title: "2026-06-13 Ao Status Partial Output Missed Live Workers"
type: source
tags: ["feedback", "worldarchitect", "agent-orchestrator"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_ao_status_partial_output_missed_live_workers.md
---

## Summary
When `ao session ls` shows \

## Key Claims
- Hermes (already dispatched) called me out in the Slack thread: "This contradicts Jeffrey's claim that there are no [active sessions]."
- 1. `ao status` (full output, no `head`/`grep` truncation)
- 2. `tmux list-sessions` (live panes exist independently of AO state DB)
- 3. `ls -lat ~/.agent-orchestrator/*/sessions/archive/ | head` (recent archive = recent deaths)
- If all three agree, report. If any disagrees, **the most-recent signal wins** — `tmux list-sessions` is ground truth because a live tmux pane means something is running whether or not AO state DB has been updated.
- - Never run `ao session ls | head -N` or `| grep -v "no active"` as the basis for "no workers." Use full output.

## Connections
- [[feedback-2026-06-13-claw-always-show-attach-urls]]
- [[feedback-2026-06-13-claw-pre-dispatch-pr-open-check]]
