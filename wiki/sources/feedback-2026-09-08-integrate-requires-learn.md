---
title: "Successful /integrate includes mandatory /learn"
type: source
tags: [integrate, learn, skill, harness, workflow]
date: 2026-09-08
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree_claude_md/memory/feedback_2026-09-08_integrate_requires_learn.md
sources:
  - /Users/jleechan/llm_wiki/raw/feedback_2026-09-08_integrate_requires_learn.md
last_updated: 2026-09-09
---

## Summary
After a successful `/integrate`, the agent skipped `/learn` because the `learn`
skill demanded a separate memory-write authorization it treated as missing.
The user corrected this in-thread: `/integrate` always wants `/learn` to run
afterward, and the skill should be strengthened so this stops recurring.
The fix targets `~/.claude/skills/integrate/SKILL.md`, replacing a
skip-on-missing-separate-approval clause with a mandatory post-integration
learning step.

## Key Claims
- A request to run `/integrate` implicitly includes its required post-success
  `/learn` workflow — it is not an optional follow-up needing its own
  authorization.
- Inventing a separate approval gate for a subcommand that is already part of
  the requested workflow is itself the bug, not a safety feature.
- An explicit no-memory instruction, or a higher-priority storage restriction,
  still overrides the mandatory step — and any blocked persistence target must
  be reported individually, not silently dropped.
- A chat summary alone is not sufficient evidence that learning was captured;
  actual persistence results must be checked.
- The fix must touch both the tracked export source and the installed skill
  copy, verify they match, and keep a `user_scope` backup.
- Tracked as bead `rev-fnfwj0` (was `pending` at first ingest).

## Key Quotes
> "run /learn and /integrate always wants learn strengthen the skill if needed" — user correction, 2026-09-08

## 2026-09-09 Live Workflow Verification
The installed `/integrate` script exited 0 and created a clean `dev1788993718`
branch tracking `origin/main` at `e1c776e11d74c2679794e49deefaa8610edf4848`.
Earlier attempts correctly stopped for a behind-upstream branch; fast-forward-only
synchronization allowed success without `--force`. The previous branch was
preserved when merged-PR status could not be verified. The session invoked the
canonical `/learn` skill after success, reusing this lesson rather than
fabricating a new one — graph and prompt-substitution audits both passed.
Evidence: `~/.claude/state/integrate-test-20260909/final.json` and
`integrate-final.log`. Bead `rev-fnfwj0`.

## Connections
- [[IntegrateSh]] — the `/integrate` script/skill this rule extends with a mandatory post-success step
- [[IntegrateHardStopPattern]] — sibling `/integrate` discipline: a guardrail must not be worked around by inventing extra gates, whether hard-stop or missing-approval
- [[SkillStaleness]] — same failure shape as the mem0-probe incident: the skill's own gate logic (not the underlying mechanism) was the bug
- jleechan-skills PR: https://github.com/jleechanorg/jleechan-skills/pull/425 — installation source for the `integrate`/`learn` skill pair
