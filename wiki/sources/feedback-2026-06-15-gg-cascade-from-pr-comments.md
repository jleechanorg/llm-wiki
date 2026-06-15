---
title: "Green Gate cancellation cascade from AO worker PR comments"
type: source
tags: [green-gate, github-actions, coderabbit, ao-worker, cancel-in-progress, feedback]
date: 2026-06-15
source_file: raw/feedback_2026-06-15_gg_cascade_from_pr_comments.md
---

## Summary

AO workers posting PR comments (e.g. `@coderabbitai re-review please`) trigger new Green Gate workflow runs. Because Green Gate uses `concurrency: cancel-in-progress: true`, each new comment-triggered run cancels the currently running GG run. This creates a cascade where GG never completes as long as the worker keeps posting.

## Key Claims

- PR comments from AO workers trigger Green Gate re-runs via `issue_comment` event
- `cancel-in-progress: true` means each new run cancels the prior pending run
- Cascade stops naturally when the worker goes IDLE
- Do not assert GG pass/fail while a worker is actively posting to the PR

## Key Quotes

> "Wait for the AO worker to go IDLE before checking GG status."

## Connections

- [[GreenGate]] — the 7-gate PR eligibility workflow
- [[AOWorker]] — autonomous AO session that posts PR comments
- [[CodeRabbit]] — triggered via `@coderabbitai re-review` comment
