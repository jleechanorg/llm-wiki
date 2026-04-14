---
title: "SkepticGate"
type: concept
tags: [ci, evidence, gate, automation, skeptic]
sources: []
last_updated: 2026-04-11
---

# SkepticGate

SkepticGate is a CI gate that runs before PRs can merge, requiring evidence that automated checks actually ran and passed. It is named for the "skeptic" agent that challenges whether automation is real vs. theater.

## Core Principle

**Evidence over assertion.** A CI check that ran but produced no evidence is indistinguishable from a check that didn't run. SkepticGate requires per-check artifacts with timestamps, not just a green checkmark.

## How It Works

SkepticGate runs as a GitHub Actions workflow triggered on `pull_request` events. It:
1. Collects artifacts from all automated tools (lint, test, evidence bundles)
2. Validates each artifact has: tool name, timestamp, pass/fail verdict, duration
3. Fails closed if any required artifact is missing or stale
4. Reports which specific checks failed and why

## Skeptic vs. Green Gate

SkepticGate was renamed `green-gate.yml` in PR #6189 because "skeptic" was misleading — it sounded like the gate challenged everything, when it actually validates that automated evidence exists.

| Gate | Purpose |
|------|--------|
| Green gate | Confirms CI checks ran and passed |
| Skeptic gate | Confirms evidence exists to PROVE checks ran |

## Failure Modes

- **Missing artifact**: Tool ran but didn't upload evidence → hard fail
- **Stale artifact**: Evidence predates the PR's latest commit → hard fail
- **Silent skip**: Tool skipped due to path filters → soft fail (warning)

## Key PRs
- [[PR-6189]] — rename: skeptic-gate.yml → green-gate.yml
- [[PR-6185]] — fix: paginate Gate-5 review threads
- [[PR-6184]] — fix: check only header section for VERDICT

## Connections
- [[EvidenceBundle]] — what SkepticGate requires per check
- [[CICDWorkflows]] — where SkepticGate fits in the CI pipeline
- [[FailClosedErrorHandling]] — SkepticGate fails closed, not open
- [[jeffrey-oracle]] — would ask "where is the evidence?" for any PR without SkepticGate artifacts
