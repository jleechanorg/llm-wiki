---
name: Gunicorn Worker Sizing and Cloud Run Concurrency Architecture
description: Comprehensive architectural record on why 1 Gunicorn worker with high threads is optimal for Python on Cloud Run, and how to detect/prevent silent Cloud Run traffic pinning.
type: reference
bead: rev-gunicorn-concurrency-pinning
---

# Gunicorn Worker Sizing and Cloud Run Concurrency Architecture

## Context & Incident
When investigating slow page loads on dev (`mvp-site-app-dev`), Playwright captured a 27.1s freeze on static CSS assets (`campaign-click-fix.css` took 27.127s). Forensics revealed:
1. Cloud Run `spec.traffic` was hard-pinned to an old 16-thread revision (`mvp-site-app-dev-04682-2zz`), starving concurrent asset requests.
2. Even though CI deployed newer revisions, they received 0% traffic due to the explicit revision pinning.
3. Once traffic was updated to `latestRevision: true` with 180 threads (`mvp-site-app-dev-04773-zks`), asset load time dropped to 0.14s and page load dropped to 0.49s.

## Key Architectural Rules & Invariants

### 1. Gunicorn 1 Worker + High Thread Count on Cloud Run
- **The Failure Mode of `(2*CPU)+1`**: On Cloud Run instances with `startup-cpu-boost=true`, `(2*CPU)+1` spawned 17 worker processes. 17 concurrent Python module imports (`google.genai`, `fastembed`, `firebase_admin`) saturated CPU and caused **240s (4-minute) cold-start hangs** and 17x heap duplication (6.6–8.2 GB RSS OOMs).
- **The Threaded Solution**: Cloud Run services must use `GUNICORN_WORKERS=1` with high thread counts (`GUNICORN_THREADS=180`), synchronized with `containerConcurrency=180`.
- **GIL Mechanics**: In Python/CPython, the Global Interpreter Lock (GIL) is **released during all network socket I/O** (`Py_BEGIN_ALLOW_THREADS`). Because this service is >95% I/O-bound (Gemini SSE streaming, Firestore queries, MCP subprocesses), 180 threads run concurrently with near-zero CPU contention.
- **Official Google Standard**: Google's official Cloud Run Python documentation explicitly recommends:
  `gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app`

### 2. Cloud Run Static Revision Pinning Prevention
- If a Cloud Run service is ever updated with an explicit revision name in `spec.traffic`, subsequent `gcloud run deploy` calls deploy new revisions with 0% traffic.
- Health checks hitting the main service URL evaluate the old pinned revision, giving false-positive success.
- **Rule**: Deploys must include `--to-latest` or update traffic explicitly (`gcloud run services update-traffic <service> --to-latest`).
- **Telemetry Check**: Always verify `labels.revision_name` in live request logs before assuming deployed code is serving traffic.

## References
- PR #7984 (Issue #7961) — Single worker cold-start remediation
- PR #9387 / Revision `mvp-site-app-dev-04773-zks`
- Google Cloud Documentation: Optimize Python applications for Cloud Run (https://cloud.google.com/run/docs/tips/python#optimize_gunicorn)
