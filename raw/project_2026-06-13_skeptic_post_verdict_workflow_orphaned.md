---
name: project-2026-06-13-skeptic-post-verdict-workflow-orphaned
description: Post Skeptic Verdict (one-shot) workflow ID 266061222 is orphaned — post-skeptic-verdict.yml deleted from main; /skeptic comment path is dead for PRs.
metadata: 
  node_type: memory
  type: project
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

**Discovery date:** 2026-06-13 ~23:18Z (during PR #7546 fix cycle)

## What is broken

The "Post Skeptic Verdict (one-shot)" GitHub Actions workflow (ID 266061222, path `.github/workflows/post-skeptic-verdict.yml`) appears in `gh api /repos/.../actions/workflows` and `gh workflow list` but **the file does not exist on `main`**. Confirmed via `git ls-tree -r main` and the GitHub contents API: only `skeptic-cron.yml` and `skeptic-self-verify.yml` exist under `.github/workflows/`.

**Effect:** posting a PR comment starting with `/skeptic` does **not** trigger an automated Skeptic verdict. The `/skeptic` convention is structurally dead.

Last successful run of this workflow: 2026-04-25T08:44:57Z (run 24927041085, branch `ci/post-verdict-6615`). Zero runs since then — ~50 days of PRs that should have triggered it, did not.

## How `skeptic-cron.yml` does work

The surviving `skeptic-cron.yml` (ID 253141151) only triggers on `workflow_dispatch` (manual) and runs only on `main`. It uses a reusable workflow from `jleechanorg/agent-orchestrator/.github/workflows/skeptic-cron-reusable.yml@main`. Cannot be triggered by `/skeptic` comment or by PR events.

## What used to work

The historical pattern (per run labels) was: AO bot detects `/skeptic` PR comment → creates `ci/post-verdict-<PR>` branch → pushes commit → workflow fires on `push` event to that branch → posts `VERDICT: PASS|FAIL` comment on the PR.

That mechanism no longer fires because the workflow file is gone.

## Workarounds (in priority order)

1. **Manual AO spawn**: `ao spawn --task "run skeptic on PR #N"` — if AO is healthy and the agent-orchestrator's reusable workflow still works, this may produce a verdict.
2. **Manual workflow_dispatch** of `skeptic-cron.yml` — but it's `main`-only, so it won't evaluate a PR branch. Not viable.
3. **Hand-post a `VERDICT: PASS` comment** — does not satisfy Gate 7 (the gate requires the workflow output, not just a comment), but is acceptable as a "self-verify" trail if the human reviewer is satisfied.
4. **Fix the missing workflow file** — restore `post-skeptic-verdict.yml` from git history (or recreate from agent-orchestrator) and re-enable the issue_comment trigger with the `/skeptic` body filter.

## Why this matters for /green

Gate 7 (Skeptic PASS) is **structurally unattainable** on PRs until #4 is done or #1 is run. This means any 7-green verification run will always report Gate 7 as FAIL with "no skeptic-gate run" as the reason. The verifier should distinguish this from "skeptic ran and FAILED" — currently the verifier reports both the same way.

## Why

CLAUDE.md "AO PR readiness: when you believe a PR is ready, post a PR comment starting with `/skeptic`" is the canonical instruction, but it relies on this dead workflow. Future /green cycles will hit the same wall.

## How to apply

When running /green on any PR in worldarchitect.ai and Gate 7 reports "no skeptic run" or "no /skeptic dispatched," check `gh api /repos/.../actions/workflows` to see if workflow 266061222 still has a corresponding file on main. If not, Gate 7 is environmentally blocked, not a real failure. Surface this to the operator as a structural finding, not a per-PR blocker.
