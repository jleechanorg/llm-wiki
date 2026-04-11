---
title: "PR #5799: fix: eliminate HuggingFace 429 cold-start delays (24-28s → 10s)"
type: source
tags: []
date: 2026-03-01
source_file: raw/prs-worldarchitect-ai/pr-5799.md
sources: []
last_updated: 2026-03-01
---

## Summary
- Fixed 24-28s Cloud Run cold starts caused by HuggingFace API 429 rate-limiting during fastembed initialization
- Added deploy-time warmup request to confirm service is live before returning
- Three-layer patch in gunicorn `on_starting` hook bypasses all HF network calls on worker boot

## Metadata
- **PR**: #5799
- **Merged**: 2026-03-01
- **Author**: jleechan2015
- **Stats**: +207/-3 in 7 files
- **Labels**: none

## Connections
