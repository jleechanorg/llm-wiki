---
title: "CI change-detector self-reference gap (2026-07-02)"
type: source
tags: [ci, testing, github-actions, worldarchitect]
date: 2026-07-02
source_file: raw/project_2026-07-02_ci_change_detector_self_reference_gap.md
---

## Summary
`scripts/ci-detect-changes.sh` in jleechanorg/worldarchitect.ai unconditionally treated `.github/**` diffs as "no test groups selected," which meant a fix to `.github/workflows/test.yml` itself (PR #8133, restoring git-tracked exec permissions on self-hosted runner checkouts) could never trigger its own regression test — the `Directory tests` matrix job showed SKIPPED on every trigger type, including manual `workflow_dispatch` of the exact same commit. Fixed by adding a targeted exception: changes to the workflow file or the change-detector script itself now select every test group.

## Key Claims
- Any CI change-detector must include itself and the workflow file(s) it configures in its own "run everything" trigger set, or fixes to it can never self-verify.
- `workflow_dispatch` does NOT bypass a change-detector gate that runs as a prerequisite job — it still computes the same `has-changes` result as the normal trigger.
- When citing a CI run as proof a fix works, the run's actual head-commit SHA must be checked against the PR's current head — a run dispatched before the fix landed will show pre-fix (broken) behavior and silently invalidate the citation. An independent evidence-reviewer caught exactly this mistake in the same PR.

## Key Quotes
> "The self-hosted runner lost communication with the server." — GitHub's own check-run annotation, observed on 5/6 Directory-tests matrix groups during an unrelated jeff-ubuntu host outage that coincided with this fix's verification.

## Connections
- [[WorldarchitectAI]] — the repo this pattern was found in
- [[SelfHostedRunnerOutage]] — the jeff-ubuntu outage that complicated verifying this fix
- [[EvidenceCitationDiscipline]] — the general practice of verifying cited artifacts match the claim before using them as proof
