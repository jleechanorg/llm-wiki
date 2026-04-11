---
title: "PR #5808: perf: defer startup imports, optimize first paint, and harden OpenClaw tunnel flow"
type: source
tags: []
date: 2026-03-02
source_file: raw/prs-worldarchitect-ai/pr-5808.md
sources: []
last_updated: 2026-03-02
---

## Summary
This PR ships performance-focused startup/import/runtime improvements and related test hardening:

- Defer heavy Python imports in `mvp_site/main.py`, `mvp_site/streaming_orchestrator.py`, and `mvp_site/llm_providers/__init__.py` via lazy-loading (`LazyLoader` / `__getattr__`).
- Add compression and first-paint improvements in `mvp_site/frontend_v1/index.html` and `mvp_site/main.py` (`flask-compress`).
- Harden OpenClaw tunnel and settings path (`--doctor` preflight, stale cache/tunnel cleanup,

## Metadata
- **PR**: #5808
- **Merged**: 2026-03-02
- **Author**: jleechan2015
- **Stats**: +2031/-176 in 26 files
- **Labels**: none

## Connections
