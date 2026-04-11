---
title: "PR #5880: fix: robust streaming LLM fallback — correct JSON guard, mock-mode unification, and de-duplicated narrative classifier"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5880.md
sources: []
last_updated: 2026-03-08
---

## Summary
- **Bug**: Short valid narratives (e.g. \"You wait.\", 9 chars) were silently dropped by an overly-aggressive `len(...) > 20` gate in the streaming fallback path, causing the raw `JSON_PARSE_FALLBACK_MARKER` sentinel to be returned to the client instead of the model's actual output.
- **Bug**: The `mock_services_mode` field in the streaming `done` payload used `os.getenv(\"MOCK_SERVICES_MODE\")` directly, missing per-request mock mode activated via `SMOKE_TOKEN` / Flask `g`.
- **Bug**: The JSON

## Metadata
- **PR**: #5880
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +112/-20 in 2 files
- **Labels**: none

## Connections
