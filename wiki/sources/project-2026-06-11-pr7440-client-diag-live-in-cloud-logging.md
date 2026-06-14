---
title: "Project 2026 06 11 Pr7440 Client Diag Live In Cloud Logging"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_pr7440_client_diag_live_in_cloud_logging.md
---

## Summary

PR #7440 (`feat(diag): client-side diagnostic logging → Cloud Logging`) was merged 2026-06-11T00:18:16Z. Auto-Deploy Dev ran and built Cloud Run revision `mvp-site-app-dev-03100-65q` from main HEAD `ff979f9f9d0ab365e12c8c6edda7c88c2430ef79`. **Live proof at `https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app/api/client_diag`** (project: `worldarchitecture-ai`, service: `mvp-site-app-dev`):

Curl probe with iPhone Safari UA:
```
$ curl -X POST .../api/client_diag -d '{"session_id":"verify-7440-ff97...

## Original

PR #7440 (`feat(diag): client-side diagnostic logging → Cloud Logging`) was merged 2026-06-11T00:18:16Z. Auto-Deploy Dev ran and built Cloud Run revision `mvp-site-app-dev-03100-65q` from main HEAD `ff979f9f9d0ab365e12c8c6edda7c88c2430ef79`.

**Live proof at `https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app/api/client_diag`** (project: `worldarchitecture-ai`, service: `mvp-site-app-dev`):

Curl probe with iPhone Safari UA:
```
$ curl -X POST .../api/client_diag -d '{"session_id":"verify-7440-ff979f9f","app_version":"verify-7440","user_agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15","events":[{"ts_ms":1234567890,"level":"info","name":"verify.test_event","fields":{"action":"curl-probe","merge_commit":"ff979f9f9d"}}]}'
HTTP/2 204
```

Cloud Logging entry (real, not mock):
```json
{
  "jsonPayload": {
    "message": "[client_diag] cdiag_name=verify.test_event cdiag_level=info cdiag_ts_ms=1234567890 cdiag_session=verify-7 cdiag_app_version=verify-7440 cdiag_ua=Mozilla/5.0_(iPhone;_CPU_iPhone_OS_17_5_like_Mac_O cdiag_field_action=curl-probe cdiag_field_merge_commit=ff979f9f9d"
  },
  "labels": {"commit-sha": "ff979f9", "revision_name": "mvp-site-app-dev-03100-65q"},
  "logName": "projects/worldarchitecture-ai/logs/run.googleapis.com/stderr",
  "resource": {"type": "cloud_run_revision", "service_name": "mvp-site-app-dev"},
  "severity": "INFO", "timestamp": "2026-06-11T00:26:43.303343Z"
}
```

**Bugbot 98b5b8c2 fix verified live**: iPhone Safari UA string with 10+ spaces collapsed to underscores, 1 token instead of 17. Pre-fix would have broken `textPayload=~"cdiag_ua=..."` queries.

**Token analysis**: 9 total tokens (1 bracket + 8 cdiag_* key=value). All cdiag_* values are space-free. "Mozilla" and "iPhone" survive intact in `cdiag_ua`.

**Auto-Deploy Dev smoke-tests step FAILS** (separate, pre-existing — does NOT block deploy). Last successful smoke was 6d before. Deploy itself (4m52s) succeeds and the new revision goes live.

**`mcp__worldai__ops_gcloud_logs_read` gotcha**: `contains` with literal `[client_diag]` returned 0 entries even though entries exist. The MCP wrapper uses `textPayload:` filter which may not match bracket literals. Workaround: omit `contains`, filter post-hoc on `jsonPayload.message` or `textPayload`. Also the wrapper fails on `severity=INFO` alone with a JSON parse error — pass no severity, then filter client-side.

**Next step for ITP investigation**: ask the iPhone Safari user to load the prod page once. Their page-load events (`page.boot`, `auth.callback_fire`, `signin.click`, etc.) will flow through and land in Cloud Logging with `cdiag_*` structured fields.

**Why this matters**: real prod service-name is `mvp-site-app` (not `-dev`). Dev was the verification target. Production deploys happen on a separate cadence (last prod deploy was 2026-06-01; PR #7440 has not yet been deployed to prod). When the user next asks about the iPhone Safari sign-in bug, query prod service `mvp-site-app` for the same cdiag_ fields, not dev.
