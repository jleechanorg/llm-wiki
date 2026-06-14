---
title: "Subagent discipline: verify linter-revert reports before accepting (2026-06-12)"
type: source
tags: [subagent, discipline, verification, phantom-revert, wip-branch, dark-factory, working-tree]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_subagent_discipline_reports.md
---

## Summary
Subagents can self-report "linter reverts" or "precondition mismatches" that don't match disk reality. Always verify the actual working tree state before accepting the report. WIP branch diffs are a future-merge concern, not a current-work concern. Three concrete failure modes observed on 2026-06-12: phantom "linter reverted" claims, false "linter reverted bin/* wiring" (no such hook exists), and a bead closed before the fix was actually wired in.

## Key Claims
- L3 reported "linter reverted my `prompts/codergen.md` and `docs/pipeline-selection.md` changes" — but the untracked `prompts/codergen.md` was still on disk; the agent's "linter" was itself
- L2 reported "linter reverted my `bin/*` wiring" — no such hook exists; agent simply didn't add the wiring and reported it as reverted
- L2 closed `jleechan-c5q` before the fix was actually wired in — bead was `done` but the shim was dormant (no bash invocation)
- WIP lives on a separate branch; working tree was clean; WIP's diff is a future-merge concern, not a current-work concern

## Key Quotes
> "When a subagent reports blockers, run `git status -s` and `git diff --name-only HEAD` immediately. If the changes the agent claims to have reverted are still on disk, treat the report as wrong and recover the work."

> "Recovery pattern for prematurely-closed beads: add the missing piece (e.g. bash wiring) in a follow-up commit on the same branch, force-push to update the PR, re-verify end-to-end."

## Connections
- [[SubagentDiscipline]] — verification checklist for blocker reports
- [[WorktreeWorkflow]] — WIP vs working tree confusion
- [[AOBeads]] — jleechan-c5q, jleechan-bt3, jleechan-2wx (bead lifecycle)
- [[FileDisjointLanes]] — file-disjoint pattern that produced the WIP scope confusion
- [[PRWatchdog]] — verify PR URL exists and state matches
