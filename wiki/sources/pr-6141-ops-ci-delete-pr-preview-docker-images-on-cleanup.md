---
title: "PR #6141: ops(ci): delete PR preview Docker images on cleanup to prevent Artifact Registry bloat"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6141.md
sources: []
last_updated: 2026-04-07
---

## Summary
- pr-cleanup.yml now deletes the Docker image from Artifact Registry when a PR is closed
- Uses the commit-sha label stored on the Cloud Run service to construct the image tag
- Prevents future gcr.io bloat (reached ~2.5TB from PR preview images)

## Metadata
- **PR**: #6141
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +68/-0 in 1 files
- **Labels**: none

## Connections
