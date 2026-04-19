---
title: "Skeptic Cron Diagnostic Recap"
type: source
tags: [workflow, ci-cd, diagnostics, automation]
date: 2026-04-18
source_file: "raw/skeptic_cron_diagnostic_recap_20260418.md"
---

## Summary
A diagnostic recap of persistent CI/CD blocks affecting WorldArchitect.AI Pull Requests. Investigating PRs #6356 and #6360 revealed that `gh pr checks` is a flawed indicator of PR health, as it reports a passing status for `Green Gate` simply because the CodeRabbit webhook triggered successfully, while the `skeptic-cron.yml` sweeps strictly enforce actual 7-green constraints.

## Key Claims
- **The CodeRabbit Stale Trap:** The `CHANGES_REQUESTED` state in GitHub pull requests does not clear automatically if code is patched; it must be explicitly re-approved using `@coderabbitai resolve` to unblock Gate 3.
- **Comment Resolution Blockade:** Gate 5 strictly counts unresolved inline GitHub review threads via the GraphQL API, meaning fixing code without formally collapsing threads leads to a merge rejection.
- **The `gh pr checks` Illusion:** A `CodeRabbit: pass` in standard GitHub checks simply confirms webhook execution, masking missing approvals and deep structural policy failures.
- **Evidence Stringency:** Gate 6 requires explicit `gist.github.com` or terminal recording links in the PR body; without them, the `skeptic-cron` bot halts the merge loop.

## Key Quotes
> "`CodeRabbit: pass` in `gh pr checks` does NOT mean the code was approved; it merely means the CodeRabbit CI webhook triggered successfully." — Diagnostic Session
> "Gate 5 strictly counts unresolved inline GitHub review threads via the GraphQL API... threads must be formally collapsed." — Diagnostic Session

## Connections
- [[Skeptic Cron]] — The strict enforcement workflow validating 7-green PR constraints.
- [[CodeRabbit]] — The AI code review system requiring explicit thread resolution to clear `CHANGES_REQUESTED`.
- [[Green Gate]] — The misleading GitHub Actions check that reports "pass" erroneously when individual underlying requirements fail.
- [[Pull Request Debugging]] — The process of distinguishing webhook success from actual policy approval.
