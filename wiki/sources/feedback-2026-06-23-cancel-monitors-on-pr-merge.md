---
title: "Cancel monitors immediately when PR is merged"
type: source
tags: [worldarchitect, ci, monitors, workflow]
date: 2026-06-23
source_file: raw/feedback_2026-06-23_cancel_monitors_on_pr_merge.md
last_updated: 2026-06-23
---

## Summary

When the user confirms a PR is merged, immediately stop all active CI/smoke/Skeptic/Green Gate monitors. Stale monitors continue polling and dispatching redundant workflows for 20+ minutes, generating noise and wasting CI resources.

## Key Claims

- PR #7802 had 5 stale monitors running 20+ min after merge confirmation.
- Stale `byu4t7go3` dispatched a redundant Skeptic run on the already-merged branch.
- `TaskStop` API requires no parameters (current API) — if it fails, note IDs and let them timeout.

## Connections

- [[worldarchitect-ai]] — repo
- [[GreenGateWorkflow]] — the workflow system these monitors watch
