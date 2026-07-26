---
title: "Shipped without real-job validation — Mac ez-gh-actions virtiofs symlink regression"
type: source
tags: [ezgha, ci-cd, testing, incident, virtiofs, colima]
date: 2026-07-19
source_file: feedback_2026-07-19_shipped_without_real_job_validation.md
---

## Summary
A production daemon runtime change in the `ez-gh-actions` (`ezgha`) self-hosted GitHub Actions runner fleet shipped on synthetic single-write test evidence while its own bead's real-job acceptance criteria were explicitly left "still open." The change introduced a virtiofs-specific bug on Colima/Mac where `tar` extraction of archives containing symlinks corrupts them into unreadable 0-byte mode-000 files — breaking `actions/setup-python`, `setup-node`, and `setup-gcloud` at a 41% job failure rate for 1-2 days before detection, because the fleet's health tooling measured container *activity* (is it running) rather than job *outcome* (is it succeeding).

## Key Claims
- A disk-churn fix (bind-mounting `/home/runner/_work` to a real host directory instead of the container's ephemeral overlay) was validated pre-deploy only with a synthetic single-file write test, never a real CI job.
- The originating bead's own acceptance criteria (6 concurrent real jobs, 30 minutes of churn) were left "still open" in its notes while the feature was simultaneously live in production config — a direct contradiction that should have blocked the deploy.
- `tar`-extracting an archive containing a symlink onto the new virtiofs-backed mount corrupts the symlink; a plain `ln -s` and extraction into the container's own overlay filesystem both work fine — only tar-extracting a real archive onto virtiofs is broken.
- The bug went undetected for 1-2 days because the fleet's health tool (`doctor-runner`) measured container activity states only (EXECUTING/IDLE-OK/IDLE-STARVED/DOWN), never job success/failure — a 100%-busy, 100%-failing fleet reads as perfectly healthy under that taxonomy.
- The fix required three adversarially-reviewed rounds (commits `0d5a802` → `4970b5e` → `16ae5fc`) before it was correct: tmpfs-shadowing the three fixed action-runner cache dirs, then widening to a mirror-then-sync `tar` wrapper for the checkout path, after two further real bugs were caught in review.
- A durable fix for the detection gap — `scripts/job_outcome_monitor.py` (commit `8a745e8`) — was built as a direct consequence.

## Key Quotes
> "Still open: acceptance criterion 1 (before/after writable-layer bytes on a real representative pip-heavy job) not yet captured — needs an actual worldarchitect.ai-style job to land on this fleet while someone is watching." — the originating bead's own notes, present at the moment the feature was already live in production.

## Connections
- [[mac-fleet-outage-causal-chain-2026-07-14]] — this regression is "Layer 6" of a longer five-layer Mac fleet outage chain (reboot → watchdog no-op → disk floor → missing image → dual-Colima), each layer independently masking the next.
- [[health-probes-report-activity-not-idleness]] — the exact same structural blind spot ("does a fully-busy system produce the same reading as a fully-dead/failing one?") recurred one level up: first "listening" vs "busy" was ambiguous (2026-07-09), then "busy" vs "succeeding" was equally ambiguous here, with nothing built yet to distinguish them until this incident forced it.
- [[ActivityVsOutcomeMonitoringGap]] — the general concept this incident is an instance of.
