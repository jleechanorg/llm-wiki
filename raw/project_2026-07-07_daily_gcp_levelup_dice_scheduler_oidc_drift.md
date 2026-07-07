---
name: project_2026-07-07_daily_gcp_levelup_dice_scheduler_oidc_drift
description: Daily GCP level-up + dice jobs were 401-dead 9 days (Cloud Scheduler OIDC-vs-OAuth drift + missing run.invoker); fixed live; where the automation actually lives
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f25f46e-82da-4972-abaa-dccc69c7b94e
---

The "daily GCP level-up and dice jobs" are **GCP Cloud Scheduler → Cloud Run Jobs**, NOT GitHub
Actions cron and NOT launchd/crontab. Keyword searches for `schedule:` / launchd / crontab will
MISS them. Canonical facts (project `worldarchitecture-ai`, region `us-central1`):

- Scheduler `wa-daily-dice-audit-scheduler`  → Cloud Run Job `wa-daily-dice-audit`
- Scheduler `wa-daily-level-up-scheduler`     → Cloud Run Job `wa-daily-level-up-test`
- Both fire daily `0 7 * * *` UTC. Setup scripts: `testing_mcp/infra/deploy_daily_test.sh` +
  `deploy_daily_dice_audit.sh`. Evidence lands in `gs://wa-test-evidence/daily/<YYYY-MM-DD>/summary.json`.
  Job task-timeout 3600s. Level-up runs `test_level_up_organic.py --level-up-scenario all` (8 scenarios)
  against the dev server `mvp-site-app-dev-i6xf2p72ka-uc.a.run.app`.

**INCIDENT (2026-07-07):** both jobs had been 401-dead since creation ~2026-06-28 — dice had ZERO
executions ever, level-up 1 failed. Root cause = TWO drifted-config defects:
1. Schedulers used an **OIDC identity token** (`oidcToken`) but the Cloud Run **Admin API** only
   accepts an **OAuth access token** → HTTP **401 UNAUTHENTICATED** on every fire. (The repo scripts
   always used `--oauth-service-account-email`, so the live OIDC was manual/legacy drift.)
2. Missing **`roles/run.invoker`** on both jobs (empty per-job IAM) — would 403 even after the OAuth fix.

**FIX (live gcloud, reversible, no repo change):**
```
gcloud run jobs add-iam-policy-binding <JOB> --region=us-central1 \
  --member="serviceAccount:<SCHED_SA>@worldarchitecture-ai.iam.gserviceaccount.com" --role=roles/run.invoker
gcloud scheduler jobs update http <SCHED> --location=us-central1 \
  --uri="https://run.googleapis.com/v2/projects/worldarchitecture-ai/locations/us-central1/jobs/<JOB>:run" \
  --oauth-service-account-email="<SCHED_SA>@worldarchitecture-ai.iam.gserviceaccount.com"
```
Verify: `gcloud scheduler jobs describe <SCHED>` → `status:{}` (not code:2); scheduler logs show
httpRequest.status 200; a new Cloud Run execution appears run-by the SA.

**KEY LESSONS:**
- Diagnose scheduler failures via `gcloud logging read 'resource.type=cloud_scheduler_job'` — it shows
  the real HTTP status (401 vs 403 matters: 401 = wrong token TYPE/OIDC-vs-OAuth; 403 = missing role).
- MONITORING GAP: these failed SILENTLY for 9 days (no alert on scheduler `status.code!=0`). Worth a
  watchdog. Tracked in bead **rev-3lr86**.
- The Cloud Run Job image is FROZEN at build time (last rebuild 2026-06-29 via `deploy-levelup-test.yml`,
  which only auto-rebuilds when specific level-up paths change on main). To validate CURRENT code you
  must rebuild the image — but the dev SERVER is always current (auto-deploys on merge), so only the
  TEST HARNESS is frozen. Check `git log origin/main -- <file>` dates vs the last rebuild date to know
  if a rebuild is even needed.
- Post-fix validation (2026-07-07): dice PASS 3/3; level-up stable 5-6/8. Two DETERMINISTIC failures
  (`real_llm_classifier_exit_path`, `projected_level_up_button_text`: "level_up_available=true without
  canonical planning choices") are PRE-EXISTING (level-up runtime unchanged since 2026-06-29), NOT a
  fleet-drive regression → bead **rev-7qlmj**. One INTERMITTENT streaming-zero-chunks crash (random
  scenario ~1/run) = known transient provider/infra flake → bead **rev-pvn9i**.

Related: [[feedback_2026-06-24_runtime_activation_claim_required]].
