---
title: "Net-Negative Deletion Is Ok"
type: concept
tags: [jeffrey, oracle, PR-review, minimal-changes]
sources: [jeffrey-oracle]
last_updated: 2026-04-10
---

Net-negative deletion — a PR that removes more lines than it adds (+N/-M where M > N, or pure deletion +0/-M — is acceptable when the removed code is unused, obsolete, or simplifying an existing approach. Removing dead code satisfies the minimal-changes principle because it moves the codebase in the right direction. The oracle applies this even to large deletions: a pure deletion of 33,126 lines of unused prototype code (+0/-33126) passes.

The key distinction is simplification versus bloat. A large addition justified as "removing complexity" is still subject to scrutiny if it adds significant new logic. But pure deletion of code with no remaining purpose is maximally minimal — it cannot be smaller. Hook slimming PRs (+6/-140) are a specific variant: net-negative PRs that trim hook chains to address context-bloat directly satisfy the minimal-changes principle and are approved.

This pattern was observed and applied consistently across oracle batches 1 and 2: PRs #6164, #6153, #6147, #6136, and #6134 all received "ok" verdicts based on net-negative deletion alone. The oracle does not apply a minimum-size floor for deletions the way it applies a maximum-size ceiling for additions. [[jeffrey-oracle]]
