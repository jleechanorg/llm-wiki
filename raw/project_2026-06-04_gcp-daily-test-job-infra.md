---
name: gcp-daily-test-job-infra
description: GCP Cloud Run Job daily level-up test infrastructure — auth, timeout, email format, and production bugs found
type: project
bead: rev-dbqms, rev-agr6m, rev-9nzqi, rev-5btpt
---

## Context

PR [#7194](https://github.com/jleechanorg/worldarchitect.ai/pull/7194) landed infrastructure for a GCP Cloud Run Job (`wa-daily-level-up-test`) that runs `test_level_up_organic.py --level-up-scenario all` nightly against the dev Cloud Run service, uploads evidence to GCS, and emails a report.

Three infra bug rounds were needed before the job ran cleanly.

## Key Infrastructure Rules

### TESTING_AUTH_BYPASS=true is mandatory in Cloud Run Jobs

Cloud Run Jobs do NOT set `K_SERVICE`. Without `TESTING_AUTH_BYPASS=true`, `clock_skew_credentials.py::validate_deployment_config()` raises `ValueError: WORLDAI_GOOGLE_APPLICATION_CREDENTIALS requires WORLDAI_DEV_MODE=true`. Set it as an explicit `export` in `entrypoint.sh` **before** the python invocation.

### --server-auth auto for dev Cloud Run service

The dev target (`mvp-site-app-dev-i6xf2p72ka-uc.a.run.app`) requires GCP identity token auth. Use `--server-auth auto` in the test runner invocation. `--server-auth none` causes `HTTP 401 Unauthorized: {"message":"No token provided"}`.

### CLOUD_RUN_EXECUTION is auto-set by GCP runtime

Cloud Run Jobs automatically inject `CLOUD_RUN_EXECUTION` (e.g. `wa-daily-level-up-test-t6km5`). No need to export it in `entrypoint.sh`. Use it in `send_report_email.py` to build direct GCP console URLs.

### Evidence root is /tmp/worldarchitect.ai, not feat/daily globs

Inside the Cloud Run container there is no git checkout — `<branch>` resolves to `unknown`. The test writes artifacts under `/tmp/worldarchitect.ai/unknown/<work-name>/`. Copy the entire tree with `cp -r "${EVIDENCE_ROOT}/." "${LOCAL_EVIDENCE_DIR}/"` (glob-based copy never matched).

### Upload uses Python, not gsutil

`Dockerfile.test-runner` is built from `python:3.11-slim` which does not include `gsutil`. Use `python3 testing_mcp/infra/upload_to_gcs.py` (uses `google-cloud-storage` Python package already installed).

### Timeout: set to 2x expected runtime, not 1.2x

The test suite ran ~25 min with 8 scenarios. The original 30-min timeout left 5 min of headroom. Increased to 3600s (60 min) in `deploy_daily_test.sh:26`. Rule: always set Cloud Run Job timeout to ≥ 2× measured runtime.

## Email Format (send_report_email.py)

Email now includes:
1. Per-scenario table with ✅/❌ badge + error details — read from `scenario_results_checkpoint.json` via `os.walk()`
2. GCP Execution Logs URL: `https://console.cloud.google.com/run/jobs/executions/details/us-central1/{CLOUD_RUN_EXECUTION}/logs?project=worldarchitecture-ai`
3. Cloud Logging URL: filtered by `resource.labels.job_name` + `execution_name`
4. GCS Evidence Browser URL: `https://console.cloud.google.com/storage/browser/wa-test-evidence/daily/{DATE_STAMP}?project=worldarchitecture-ai`

## Production Bugs Found (GCP executions b5956, t6km5)

| Bead | Scenario | Failure |
|---|---|---|
| `rev-dbqms` | god_mode_reward_visibility | XP awarded but rewards_box not persisted to Firestore story entry |
| `rev-agr6m` | multi_level_organic_progression | Level-3 modal escape + free-form edit advance player_turn (modal lock not enforced for Sacred Oath selection) |
| `rev-9nzqi` | projected_level_up_button_text | level_up_available=true but rewards_box absent from response |
| `rev-5btpt` | multi_level_organic_progression | finish_level_up_return_to_game copy missing "applies recommended options" |
| `rev-ufb13` | atomicity_e2e | rewards_box present but xp_gained ≤ 0 (still reproducible, P0) |

## Files Changed

- `testing_mcp/infra/entrypoint.sh` — TESTING_AUTH_BYPASS, --server-auth auto, cp -r tree copy, exports for email
- `testing_mcp/infra/send_report_email.py` — scenario table, GCP URLs, CLOUD_RUN_EXECUTION
- `testing_mcp/infra/deploy_daily_test.sh` — timeout 1800→3600
- `testing_mcp/infra/Dockerfile.test-runner` — python:3.11-slim, no gsutil

## References

- PR [#7194](https://github.com/jleechanorg/worldarchitect.ai/pull/7194) merged
- Commits: `d80d0a17b4` (TESTING_AUTH_BYPASS), `fda8555e35` (--server-auth auto), `aa93c76f77` (email format), `947fe51d49` (timeout 60min)
- GCP executions: `wa-daily-level-up-test-b5956` (2026-06-04), `wa-daily-level-up-test-t6km5` (2026-06-05)
- Email confirmed received: Gmail IDs `19e950663d96e700`, `19e952d33d6192f5`
