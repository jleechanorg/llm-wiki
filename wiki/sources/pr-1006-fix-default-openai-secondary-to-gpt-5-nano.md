---
title: "PR #1006: fix: default OpenAI secondary to gpt-5-nano"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-/pr-1006.md
sources: []
last_updated: 2026-03-09
---

## Summary
- switch the default OpenAI secondary model from `gpt-5-mini` to `gpt-5-nano`
- update cost/display aliases so OpenAI defaults stay internally consistent
- keep non-PR Cloud Run deployments warm with `minScale=1`
- rotate and validate the Gemini API key in GCP Secret Manager

## Metadata
- **PR**: #1006
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +77/-124 in 17 files
- **Labels**: none

## Connections
