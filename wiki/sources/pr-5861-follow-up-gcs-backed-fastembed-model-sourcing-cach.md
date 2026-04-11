---
title: "PR #5861: follow-up: GCS-backed FastEmbed model sourcing + cache bootstrap simplification"
type: source
tags: []
date: 2026-03-06
source_file: raw/prs-worldarchitect-ai/pr-5861.md
sources: []
last_updated: 2026-03-06
---

## Summary
This stacked follow-up builds on #5860 and moves Docker model provisioning toward a single, deterministic preflight flow:

- Added optional **GCS-backed FastEmbed cache restore** in `scripts/preflight_model_docker.py` via `FASTEMBED_GCS_ARCHIVE_URI` (`gs://...`).
- Added `FASTEMBED_GCS_REQUIRED` guardrail for strict builds that must fail if GCS restore/validation fails.
- Kept robust fallback: when GCS cache is absent or invalid (and not required), preflight falls back to direct HuggingFace down

## Metadata
- **PR**: #5861
- **Merged**: 2026-03-06
- **Author**: jleechan2015
- **Stats**: +296/-145 in 6 files
- **Labels**: none

## Connections
