---
name: Skeptic Cron Auto-Merge
description: The skeptic-cron.yml workflow automatically merges PRs once they are verified 7-green.
type: reference
bead: none
---

# Skeptic Cron Auto-Merge

## Context
When bringing pull requests in the `agent-orchestrator` repository to a 7/green state, the question of whether pull requests are merged automatically arises.

## Findings
- **Auto-Merge Mechanism**: The GitHub Actions workflow `.github/workflows/skeptic-cron.yml` runs periodically (on a cron schedule) to verify all 7 gates for open PRs.
- **Skeptic Verdict**: Once the skeptic agent verifies the PR and posts a comment with `VERDICT: PASS`, the 7th gate passes.
- **Auto-Merge Execution**: If all 7 gates pass, the skeptic cron workflow will automatically execute `gh pr merge --squash --admin --delete-branch` to merge the PR.
- **Enable Flag**: This behavior is controlled by the repository variable `SKEPTIC_CRON_AUTO_MERGE`, which is currently set to `"true"` in `jleechanorg/agent-orchestrator`.
- **Command Alias**: The `/ms` command is a shortcut/alias for `/memory_search` in Claude Code / OpenClaw and searches across all memory systems.

## Reusable Pattern
- Always verify repository variables and cron workflows when determining if pull requests are merged automatically.
- Do not execute manual merge commands without explicit user authorization (`MERGE APPROVED`), even if GHA has auto-merge enabled.
