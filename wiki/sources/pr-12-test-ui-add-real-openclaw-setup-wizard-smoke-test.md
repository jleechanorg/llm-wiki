---
title: "PR #12: test(ui): add real OpenClaw setup wizard smoke test with probe validation"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldai_claw/pr-12.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Add a real-browser pytest smoke test for the OpenClaw setup wizard in `testing_ui/test_openclaw_setup_wizard_pytest.py`.
- Exercise `/api/openclaw/test-connection` and fail fast on non-success payloads while surfacing explicit backend response detail.
- Resolve gateway URL/token from env (with fallback to `~/.bashrc`) and require `OPENCLAW_GATEWAY_TOKEN` for deterministic execution.
- Retry once for transient `models endpoint returned JSON but no model entries` before hard-failing.
- Keep UI a

## Metadata
- **PR**: #12
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +1902/-420 in 19 files
- **Labels**: none

## Connections
