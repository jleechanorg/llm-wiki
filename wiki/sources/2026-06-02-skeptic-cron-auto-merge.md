---
title: "Skeptic Cron Auto-Merge — 2026-06-02"
type: source
tags: [skeptic-cron, auto-merge, agent-orchestrator, github-actions]
date: 2026-06-02
---

## Summary

The skeptic cron job (`skeptic-cron.yml` workflow on GitHub Actions) periodically scans open pull requests in the repository. If all 7-green conditions are satisfied—including the 7th gate (Skeptic Agent Verdict: PASS) which is verified via the `ao skeptic verify` comment—the workflow will automatically squash-merge the PR.

## Key Findings

- **SKEPTIC_CRON_AUTO_MERGE**: This variable is defined in the GitHub repository variables. Its value is currently set to `"true"` in `jleechanorg/agent-orchestrator`.
- **Auto-Merge execution**: When a PR is verified as 7-green, the cron workflow executes `gh pr merge "$PR_NUM" --squash --admin --delete-branch` to merge the PR automatically.
- **Memory Search Alias (`/ms`)**: The `/ms` command is an alias for `/memory_search` which searches across all memory systems in the environment.

## Connections

- [[merge-gate]] — details of the 7-green verification checks.
- [[skeptic-cron]] — the GHA workflow that handles auto-merging.
- [[memory-search]] — the `/ms` command used to look up these settings.
