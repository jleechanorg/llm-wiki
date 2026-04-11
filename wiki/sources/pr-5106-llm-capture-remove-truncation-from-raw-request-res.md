---
title: "PR #5106: LLM capture: remove truncation from raw request/response logging"
type: source
tags: []
date: 2026-02-09
source_file: raw/prs-worldarchitect-ai/pr-5106.md
sources: []
last_updated: 2026-02-09
---

## Summary
- remove truncation from LLM capture artifacts when capture is enabled
- store full `raw_response_text` in processing metadata
- store full `system_instruction_text`, `request_payload`, and `response_text` in `llm_request_responses.jsonl`

## Metadata
- **PR**: #5106
- **Merged**: 2026-02-09
- **Author**: jleechan2015
- **Stats**: +10/-22 in 1 files
- **Labels**: none

## Connections
