---
name: dice-audit-monitoring-spec-gcp-heartbeat-alert-daily-job-design-only-not-coded
description: How to monitor for dice-audit regressions in GCP; the conditionAbsent gotcha; daily-job mirror facts
metadata: 
  node_type: memory
  type: project
  originSessionId: 8db1dfd9-b927-4982-b047-67735868e667
---

`/innovate` + `/nextsteps` design (PR #7280 follow-up). Goal: catch dice-audit regressions in prod GCP before they go silent. **Design/research only — no implementation code written** (user: "research the spec but dont code it yet"). Repo `jleechanorg/worldarchitect.ai`; GCP project `worldarchitecture-ai`, service `mvp-site-app-stable`, region `us-central1`. Nextsteps handoff: `roadmap/nextsteps-2026-06-05-dice-audit-monitoring.md`.

**Core innovation — "Dice Telemetry Heartbeat":** the regression signature is the `DICE_AUDIT: notation=` INFO heartbeat (`mvp_site/dice.py:468`) going SILENT while request traffic continues — not warnings appearing. A warning-presence alert cannot catch telemetry that stopped emitting.

**LOAD-BEARING GCP CORRECTION:** `conditionAbsent` does NOT reliably fire on **log-based metrics** — Cloud Monitoring injects a synthetic zero into time-series gaps, so the series reads "present, value 0." Model absence as `conditionThreshold` `COMPARISON_LT` (heartbeat `< 2`/1h) + `evaluationMissingData: EVALUATION_MISSING_DATA_ACTIVE`. Second mandatory guard: AND-gate (`combiner:"AND"`) with Cloud Run `run.googleapis.com/request_count > 0` so scale-to-zero idle ≠ false alarm. Ratio alert `warning/(warning+heartbeat) > 0.05` needs MQL/PromQL (two-metric denominator) and MUST be its own single-condition policy.

**Verification BLOCKER (do before creating heartbeat metric):** confirm the INFO `DICE_AUDIT: notation=` log actually reaches Cloud Logging as `jsonPayload.message` in prod. `mvp_site/logging_util.py:51-65` only emits JSON when `K_SERVICE` is set; if prod logs it as `textPayload`, every metric filter must switch `jsonPayload.message=~` → `textPayload=~`.

**Daily job mirror** (`testing_mcp/infra/*` level-up pattern → `wa-daily-dice-audit`): Cloud Scheduler → Cloud Run Job, cron `17 9 * * *` America/New_York (09:17 ET, dodges the 07:00 ET level-up job + its 60-min task timeout). Dockerfile MUST add `COPY scripts/ ./scripts/` (level-up image doesn't). Parameterize `send_report_email.py` GCP_JOB_NAME/subject (hardcoded lines 18/193) for shared use; `upload_to_gcs.py` already generic. Top-N active-campaign selection reuses `scripts/daily_campaign_report.py:256-280,533-548` (per-user `list_users().iterate_all()` → skip `is_test_user` → `campaigns.where(last_played>=cutoff)` → rank `max(last_played,generated)` → top-N). `scripts/audit_dice_rolls.py` must be fixed first: `main()` always exits 0 (line ~1086) and warnings are print-only; refactor `audit_campaign_dice()` (line 891) to RETURN the `_build_audit_warnings(...)` list (discarded line ~1064), keep CLI exit 0, add `daily_dice_audit.py` wrapper that exits non-zero only on real-failure signatures (`"chi-square"`+`"exceeds threshold"` 874-877, `"No provably fair/code-execution dice sources found"` 786-789), EXCLUDING benign (`underpowered/inconclusive` 837, `unknown notation` 803).

**No monitoring-as-code exists** in repo (no .tf/log-based metrics/alert policies — all manual console). Seed `monitoring/dice/` as first IaC (gcloud scripts + policy JSON + idempotent deploy.sh). Cost: counter log-based metrics billed 8 bytes/point (negligible); alert policies free until ~Sept 1 2026 then ~$0.35/mo each; always pin `resource.type` to dodge the Unspecified-Resource cost trap. Slack channel via native GCP `--type=slack` (needs self-minted Slack bot OAuth token as `auth_token` credential — user must mint) or `--type=webhook_tokenauth`.

Beads: rev-1fmed (heartbeat), rev-b3ua9 (warning/invalid alerts), rev-4rdlp (daily job), rev-gid6g (audit exit-code), rev-qe641 (IaC seed). PR #7280 OPEN / CHANGES_REQUESTED / MERGEABLE — monitoring is a SEPARATE follow-up PR, not a #7280 blocker.
