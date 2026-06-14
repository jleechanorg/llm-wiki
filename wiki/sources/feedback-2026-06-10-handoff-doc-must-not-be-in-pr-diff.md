---
title: "Feedback 2026 06 10 Handoff Doc Must Not Be In Pr Diff"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_handoff_doc_must_not_be_in_pr_diff.md
---

## Summary

**Discovered 2026-06-10 10:19Z the hard way.** I pushed a roadmap handoff doc to `feat/dice-audit-telemetry-reconciliation` (PR #7354's branch) at commit `ab35fb739e`. The doc was `roadmap/nextsteps-2026-06-10-dice-audit-prs-7352-7353-7354-7green.md` — a 200-line handoff describing the state of PRs #7352, #7353, and #7354. **Result:** Skeptic Gate FAIL'd #7354 with:
- `<!-- skeptic-gate-8d:FAIL -->` Scope boundary gap (Unexplained Daily Audit Job and GCP Infra)
- `<!-- skeptic-gate-8c:FAIL -->` ...

## Original

# Handoff doc must NOT be in a code PR's diff

**Discovered 2026-06-10 10:19Z the hard way.** I pushed a roadmap handoff doc to `feat/dice-audit-telemetry-reconciliation` (PR #7354's branch) at commit `ab35fb739e`. The doc was `roadmap/nextsteps-2026-06-10-dice-audit-prs-7352-7353-7354-7green.md` — a 200-line handoff describing the state of PRs #7352, #7353, and #7354.

**Result:** Skeptic Gate FAIL'd #7354 with:
- `<!-- skeptic-gate-8d:FAIL -->` Scope boundary gap (Unexplained Daily Audit Job and GCP Infra)
- `<!-- skeptic-gate-8c:FAIL -->` Evidence provenance gap
- `<!-- skeptic-gate-8a:FAIL -->` Goals proof gap (Streaming and Narrative parsing validation missing)

**Why:** The Skeptic agent reads the PR's diff and finds:
1. The handoff doc references files from #7353 (`scripts/daily_dice_audit.py`, `testing_mcp/infra/Dockerfile.dice-audit`, `deploy_daily_dice_audit.sh`) that are not in the #7354 diff. → "Scope boundary gap"
2. The handoff doc references goals from #7352 (alerting) and #7353 (daily cron) that #7354's diff doesn't implement. → "Goals proof gap"
3. The handoff doc uses Gist links for evidence, not raw media files. → "Evidence provenance gap"

**Why this was a "doc-only commit" mistake:** A doc-only commit to provoke a fresh CodeRabbit review is fine — but the content of the doc must be IN-SCOPE for the PR. A multi-PR roadmap handoff doc is out-of-scope for any single PR.

**Resolution:** Reverted the handoff doc from #7354 via `git reset --hard 837e302381` (the pre-handoff-doc tip) and created a separate branch `docs/dice-audit-7green-handoff` based on origin/main to hold the handoff doc. A new push to #7354 will produce a clean Green Gate.

**Rule:** **Never push a handoff doc / nextsteps doc / multi-PR roadmap doc to a code PR's branch.** Handoff docs go in:
- A separate docs-only branch (like `docs/dice-audit-7green-handoff`) and optionally opened as a docs PR
- `~/roadmap/` outside the repo (user-scope handoff)
- A separate docs-only PR with an explicit "docs: add handoff" title

**Don't conflate handoff docs with "doc-only commit to provoke CodeRabbit re-review":** those are different concerns.
- A **provoke-CR-review doc commit** should be in-scope for the PR (e.g., a comment/docstring in the same code module as the PR's changes).
- A **handoff doc** summarizes cross-PR state and is, by design, out-of-scope for any individual PR.

**How to apply:**
- When writing a `/nextsteps` handoff for multiple PRs, always put the doc in a separate branch on `origin/main`, NOT on one of the PRs' branches.
- When deciding where to commit a handoff doc, run `git log --oneline -1` on the current branch. If the current branch is a code PR's branch (`feat/...`, `fix/...`, `chore/...`), create a new worktree from `origin/main` and commit there instead.
- If you accidentally push a handoff doc to a code PR, `git reset --hard <pre-handoff-sha>` on the worktree (no force-push needed if the local tip is the same as the pushed tip). The reset uncommits locally; a follow-up push will need `--force-with-lease` since the remote tip is now ahead of local.
- **Pre-commit checkpoint rule:** before `git commit` on a `feat/`, `fix/`, `chore/`, `refactor/` branch, ask "is this commit in the PR's scope?" If the commit is a handoff doc / roadmap / cross-PR summary, switch worktrees or create a new branch first.
