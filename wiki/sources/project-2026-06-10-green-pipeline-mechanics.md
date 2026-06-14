---
title: "Project 2026 06 10 Green Pipeline Mechanics"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-10_green_pipeline_mechanics.md
---

## Summary

Learned 2026-06-10 driving 8 level-up PRs to green (#7370/#7376 merged; #7374/#7377/#7416/#7252/#7441/#7442 evidence-verified). **Skeptic verdict plumbing (the chain Green Gate depends on):**
1. `green-gate.yml` (pull_request event) polls PR comments for `<!-- skeptic-agent-verdict -->` + `VERDICT: PASS` matching the CURRENT head SHA (`skeptic-head-sha-<sha>` marker).

## Original

Learned 2026-06-10 driving 8 level-up PRs to green (#7370/#7376 merged; #7374/#7377/#7416/#7252/#7441/#7442 evidence-verified).

**Skeptic verdict plumbing (the chain Green Gate depends on):**
1. `green-gate.yml` (pull_request event) polls PR comments for `<!-- skeptic-agent-verdict -->` + `VERDICT: PASS` matching the CURRENT head SHA (`skeptic-head-sha-<sha>` marker). No verdict at head = FAIL.
2. `skeptic-cron.yml` is `workflow_dispatch`-ONLY (no schedule in-repo; an external automation usually fires it). It only POSTS TRIGGER comments, and only for PRs that are already 6-green (its own checks incl. "comments resolved"). It does NOT write verdicts.
3. The verdict writer is `skeptic-self-verify.yml` — dispatch-only with `-f pr_number=N`: `gh workflow run skeptic-self-verify.yml -f pr_number=7376`. Manual dispatch works when the external trigger-consumer is asleep.
4. After verdict lands: rerun the FAILED pull_request-event green-gate runs (`gh run rerun <id> --failed`). A `workflow_dispatch` green-gate success does NOT attach to PR checks — only pull_request-event runs do. Multiple stale Green Gate check-runs can sit on one SHA; rerun each failed one.

**Gate 6 (Evidence) requires an https URL in the PR BODY/comments** — a verifier evidence comment alone fails `FAIL(no-evidence)`. Fix: `gh gist create <summary.md>` then append `## Evidence\n<gist-url>` to the body. Hit identically on #7416, #7441, #7442.

**Design Doc Grep Gates** carries a `world_logic.py` line-count budget (≤11000). #7376's dispatcher pushed it to 11311, failing UNRELATED PRs' gates (#7374). Right fix = extraction PR (#7442, −439 lines), not limit bumps (rogue automation bumped to 11500 on #7377's branch — unnecessary after extraction).

**Coordination hazards (recurring all day):** an unidentified automation under the shared jleechan2015 credential force-push rebases level-up branches (`gh api repos/<o>/<r>/activity?ref=refs/heads/<branch>` is the only place force_push events + timing show). Worker discipline that worked: REGULAR push only, non-fast-forward = STOP-and-report, team-lead explicitly authorizes adopt-remote after verifying the foreign rebase (AST function-diff vs main). Related: [[subagent-force-push-violation]], [[stacked-pr-single-writer-rule]].
