---
title: "Sidekick branch-scoped STATE.md + commit-often proven by PR #8198 recovery"
type: source
tags: [sidekick, agent-orchestration, commit-discipline, crash-recovery]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_sidekick_branch_scoped_state_and_commit_often.md
---

## Summary
Two related lessons from an overnight (2026-07-06/07) multi-sidekick session on worldarchitect.ai: (1) a single shared `/tmp/<repo>/sidekick/STATE.md` across concurrently-running sidekicks causes write clobbers even with namespaced sections, and a fully separate per-mission path is the more durable fix; (2) the standing "commit after every green unit of work" rule was empirically proven when a crashed sidekick's finished-but-uncommitted CI fix was recovered from the working tree by a successor agent and shipped as PR #8198.

## Key Claims
- Namespacing sections within one shared STATE.md file (`## <mission> (session <id>, owner: sidekick — <scope>)`) reduces but does not eliminate clobber risk, because every sidekick is still writing into the same file — a bad append or stale read-then-write can still stomp a sibling's edit.
- Recommended fix: fully separate path per sidekick, `/tmp/<project>/sidekick/<branch-or-mission>/STATE.md`, removing the write-write race entirely. Reach for shared-file-with-namespacing only when sidekicks must actually read each other's state, and even then keep each one's mutable section in its own file with a shared index linking them.
- A sidekick working an overnight CI-fix mission crashed after finishing code but before `git commit`. Because commit-often discipline meant the working tree still held the finished fix, a successor agent found it uncommitted (not lost), committed it, and it shipped as PR #8198.

## Connections
- [[feedback-2026-07-07-swarm-orchestration-learnings-pr8191]] — documents the original clobber incident (rule 3) that this entry proposes a structural fix for
- [[project-2026-07-07-pr8198-ci-workflow-regressions]] — the fix recovered and shipped by this incident
- [[swarm-orchestration-pattern]]
- [[jleechanorg-agent-orchestrator]]
