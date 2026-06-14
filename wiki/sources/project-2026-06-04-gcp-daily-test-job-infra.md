---
title: "GCP Daily Test Job Infrastructure (PR #7194)"
type: source
tags: ["gcp", "cloud-run-job", "daily-test", "worldarchitect-ai", "pr-7194"]
date: 2026-06-04
source_file: project_2026-06-04_gcp-daily-test-job-infra.md
---

## Summary
PR #7194 landed infrastructure for GCP Cloud Run Job (`wa-daily-level-up-test`) that runs `test_level_up_organic.py --level-up-scenario all` nightly against dev Cloud Run. Three infra bug rounds needed before clean run.

## Key Claims
- TESTING_AUTH_BYPASS=true is mandatory in Cloud Run Jobs (no K_SERVICE set)
- `--server-auth auto` for dev Cloud Run (GCP identity token auth)
- CLOUD_RUN_EXECUTION auto-injected by GCP runtime
- Evidence root is /tmp/worldarchitect.ai, not feat/daily globs (no git checkout inside container)
- Upload uses Python (`google-cloud-storage`), not gsutil (`python:3.11-slim` doesn't include it)
- Timeout: 2× expected runtime (1800→3600s for 25-min suite)

## Key Quotes
> Beads: rev-dbqms, rev-agr6m, rev-9nzqi, rev-5btpt, rev-ufb13 — production bugs found in GCP executions b5956, t6km5

## Connections
- [[GCPDailyTest]] — infra concept
