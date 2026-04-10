---
title: "Git SHA Tracking"
type: concept
tags: [git, versioning, traceability]
sources: [cloud-run-commit-sha-tracking]
last_updated: 2026-04-07
---

Git SHA Tracking is the practice of capturing and storing git commit identifiers throughout the deployment pipeline for complete traceability. This implementation uses `git rev-parse HEAD` locally and `GITHUB_SHA` in CI/CD, with a timestamp-based fallback (`local-YYYYMMDD-HHMMSS`) when git is unavailable.

## Methods
- **Local**: `git rev-parse HEAD`
- **CI/CD**: `GITHUB_SHA` env var
- **Fallback**: `local-YYYYMMDD-HHMMSS`

## Wiki Connections
- Core concept in: [[Cloud Run Commit SHA Tracking]]
