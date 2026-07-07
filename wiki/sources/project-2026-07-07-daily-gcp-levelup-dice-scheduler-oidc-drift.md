---
title: "Daily GCP level-up + dice jobs: Cloud Scheduler OIDC-vs-OAuth drift (401, 9 days silent)"
type: source
tags: [gcp, cloud-scheduler, cloud-run-jobs, iam, oauth, oidc, worldarchitect, incident, monitoring-gap]
date: 2026-07-07
source_file: ../raw/project_2026-07-07_daily_gcp_levelup_dice_scheduler_oidc_drift.md
---

## Summary
The "daily GCP level-up + dice validation jobs" for worldarchitect.ai are implemented as **GCP Cloud
Scheduler → Cloud Run Jobs** (project `worldarchitecture-ai`, region `us-central1`), NOT GitHub Actions
cron or launchd/crontab — so keyword searches for `schedule:`/launchd/crontab miss them. They silently
failed for ~9 days (2026-06-28 → 2026-07-07) with HTTP 401 UNAUTHENTICATED on every daily fire, due to
two drifted-config defects, and were fixed live on 2026-07-07.

## Key Claims
- The automation is Cloud Scheduler jobs `wa-daily-dice-audit-scheduler` + `wa-daily-level-up-scheduler`
  (cron `0 7 * * *` UTC) invoking Cloud Run Jobs `wa-daily-dice-audit` + `wa-daily-level-up-test`.
- Root cause #1: schedulers used an **OIDC identity token** but the Cloud Run **Admin API** only accepts
  an **OAuth access token** → 401. Diagnostic rule: **401 = wrong token TYPE (OIDC-vs-OAuth)**, **403 =
  missing IAM role**.
- Root cause #2: missing **`roles/run.invoker`** on both Cloud Run Jobs (empty per-job IAM).
- Fix (live gcloud, reversible): grant `run.invoker` to each scheduler SA on its job, then
  `gcloud scheduler jobs update http <SCHED> --oauth-service-account-email=<SA> --uri=<v2 :run URL>`.
- Diagnose scheduler failures with `gcloud logging read 'resource.type=cloud_scheduler_job'` (shows the
  real HTTP status). The repo scripts always used `--oauth-service-account-email`, so live OIDC was drift.
- Monitoring gap: silent 9-day failure with no alert on scheduler `status.code != 0` — a watchdog is
  warranted. Cloud Run Job images are frozen at build time, so a frozen-vs-current test failure requires
  checking `git log origin/main -- <file>` dates vs last image-rebuild date before calling it a regression.

## Key Quotes
> "401 UNAUTHENTICATED = the Admin API rejects the OIDC identity token; it needs an OAuth access token." — root-cause note

## Connections
- [[GCP Cloud Scheduler]] — the trigger mechanism, drifted to OIDC
- [[Cloud Run Jobs]] — the invoked target requiring OAuth + run.invoker
- [[WorldArchitect.AI]] — the project whose daily level-up/dice validation this powers
- [[Runtime Activation Claim]] — related discipline: verify the mechanism, don't trust status strings
