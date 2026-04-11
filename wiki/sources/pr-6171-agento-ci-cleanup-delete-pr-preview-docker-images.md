---
title: "PR #6171: [agento] ci(cleanup): delete PR preview Docker images on close + self-hosted runner enforcement"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldarchitect-ai/pr-6171.md
sources: []
last_updated: 2026-04-10
---

## Summary
- Adds Docker preview image deletion workflow (pr-cleanup.yml) to prevent Artifact Registry bloat
- Enforces self-hosted runners for private workflows across all workflow files
- Adds preview-image-janitor scheduled workflow to prune stale image digests
- Improves FastEmbed download retry/backoff with new unit tests

## Metadata
- **PR**: #6171
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +639/-322 in 27 files
- **Labels**: none

## Connections
