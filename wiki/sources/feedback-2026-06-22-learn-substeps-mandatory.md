---
title: "/learn sub-steps are MANDATORY every time, never skip"
type: source
tags: [feedback, worldarchitect, process-compliance, learn-skill, anti-pattern, pr-7815]
date: 2026-06-22
source_file: raw/feedback_2026-06-22_learn_substeps_mandatory.md
---

## Summary
The `/learn` skill's five required persistence targets (Claude memory + MEMORY.md + roadmap log + bead + wiki-ingest) are first-class deliverables, not gate-blocking optional skips. User correction 2026-06-22: "do this always dont skip Skipped the wiki-ingest + roadmap-log + bead-creation sub-steps of /learn's protocol." The only legitimate "skip" is when the target is actually unreachable — and even then, report the blocker and continue.

## Key Claims
- For every `/learn` invocation, always produce **all five** persistence targets in this order:
  1. `~/.claude/projects/<project_key>/memory/<type>_YYYY-MM-DD_<slug>.md` + MEMORY.md index entry
  2. `~/roadmap/learnings-YYYY-MM.md` log entry
  3. A bead in `.beads/issues.jsonl` (or `none` if beads truly unavailable + report why)
  4. LLM wiki ingest via the `wiki-ingest` skill (mandatory, never direct write)
  5. mem0 save when available (optional; report missing dep if not)
- The `cd` to the worktree boundary is **not** a reason to skip — those paths live in `$HOME` and the worktree writes to its own git tree; the persistence targets are *outside* the worktree by design.
- "Project CLAUDE.md doesn't enforce them as gate-blocking" is a **wrong** argument. /learn is a skill contract, not a CI gate.
- Common mistake (mine, 2026-06-22): claiming "those targets are not reachable from the worktree without a cross-write" as a reason to skip — the cross-write IS the work.

## Key Quotes
> "do this always dont skip" — user correction 2026-06-22

## Connections
- [[GATE6bDescriptionGate]] — sister learning from same PR cycle
- [[SelfHostedRunnerInfraFlakeVsRealFailure]] — same PR cycle
- [PR #7815](https://github.com/jleechanorg/worldarchitect.ai/pull/7815) (merged 2026-06-23T02:21:20Z) — the PR cycle where this rule was first violated, then corrected
- /learn SKILL.md "Required outputs" #1-#5
- Bead: rev-i1spe
