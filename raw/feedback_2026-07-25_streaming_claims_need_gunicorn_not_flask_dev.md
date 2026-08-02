---
name: streaming-claims-need-gunicorn-not-flask-dev
description: "worldarchitect.ai's local dev server runs Flask's single-threaded app.run(), production runs gunicorn with gthread workers — a streaming/concurrency claim tested on the dev server proves nothing about production behavior"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:46:09.805Z
---

worldarchitect.ai's `run_local_server.sh` path starts the app via Flask's `app.run()` (confirmed at `mvp_site/main.py:5671-5675`, single dev process, `debug`/`use_reloader` controlled by env vars). Production runs `gunicorn -c gunicorn.conf.py main:create_app()` (confirmed at `mvp_site/Dockerfile:99`), with gthread workers — the Dockerfile comment states "Performance: 12+ concurrent requests vs 1 request with default sync worker."

A lane measured narrative text jumping from placeholder to full length in a single step when captured against the local dev server, and treated that as a finding about production streaming behavior. It is not — Flask's dev server and gunicorn's threaded/multi-worker model can behave differently for anything involving concurrency, request queuing, or chunked/streamed responses. A dev-server-only capture cannot settle a production streaming claim.

**Rule:** for any claim about streaming delivery, concurrency, or request-queuing behavior in worldarchitect.ai, run gunicorn locally (`gunicorn -c gunicorn.conf.py main:create_app()` from `mvp_site/`) rather than `run_local_server.sh`'s Flask dev server, or explicitly caveat the claim as "dev-server only, not verified against the production server model." This is a specific case of the general "optimization baseline fidelity" principle in `~/.claude/CLAUDE.md` (A/B control must match the deployed config) applied to correctness claims rather than cost claims.
