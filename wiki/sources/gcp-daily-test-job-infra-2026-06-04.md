# GCP Cloud Run Job daily test infra — auth, timeout, email format (2026-06-04)

**Source**: `project_2026-06-04_gcp-daily-test-job-infra.md`
**Type**: project
**Date**: 2026-06-04
**Bead**: rev-zsls4
**PR**: [#7194](https://github.com/jleechanorg/worldarchitect.ai/pull/7194)

## Summary

PR #7194 landed infrastructure for a GCP Cloud Run Job (`wa-daily-level-up-test`) running nightly level-up integration tests against the dev Cloud Run service. Three rounds of infra bug fixes were required before the job ran cleanly.

## Key Rules Learned

### TESTING_AUTH_BYPASS=true is mandatory in Cloud Run Jobs
Cloud Run Jobs do NOT set `K_SERVICE`. Without this env var, `clock_skew_credentials.py::validate_deployment_config()` raises `ValueError`. Set it as explicit `export` in `entrypoint.sh` **before** the python invocation.

### --server-auth auto for dev Cloud Run service
The dev target requires GCP identity token auth. `--server-auth none` → `HTTP 401 Unauthorized`.

### CLOUD_RUN_EXECUTION is auto-set by GCP runtime
No need to export it in `entrypoint.sh`. Use it in `send_report_email.py` to build direct GCP console URLs.

### Evidence root is /tmp/worldarchitect.ai, not feat/daily globs
Inside Cloud Run container, `<branch>` resolves to `unknown`. Use `cp -r "${EVIDENCE_ROOT}/." "${LOCAL_EVIDENCE_DIR}/"`.

### Upload uses Python, not gsutil
`python:3.11-slim` does not include Cloud SDK / `gsutil`. Use `python3 testing_mcp/infra/upload_to_gcs.py`.

### Timeout: 2x expected runtime
Increased from 1800s → 3600s. Rule: always set to ≥2× measured runtime.

## Production Bugs Found (executions b5956, t6km5)

- `rev-dbqms`: god_mode_reward_visibility — XP awarded but rewards_box not persisted
- `rev-agr6m`: multi_level_organic_progression — Level-3 modal lock not enforced for Sacred Oath selection
- `rev-9nzqi`: projected_level_up_button_text — level_up_available=true but rewards_box absent
- `rev-5btpt`: multi_level_organic_progression — finish_level_up copy missing "applies recommended options"
- `rev-ufb13`: atomicity_e2e — rewards_box present but xp_gained ≤ 0 (P0)

## Concepts

[[cloud-run-jobs]] [[testing-auth-bypass]] [[gcp-evidence-upload]]
