---
title: "Cloud Run Commit SHA Tracking"
type: source
tags: [cloud-run, gcp, cicd, deployment, git, traceability]
source_file: "raw/cloud-run-commit-sha-tracking.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Comprehensive commit SHA tracking for Cloud Run deployments using three complementary approaches: container image tagging (primary), Cloud Run labels (metadata), and Cloud Build integration (automatic). Enables full traceability from deployed container back to exact source code commit.

## Key Claims
- **Container Image Tagging**: Image tags include commit SHA (e.g., `gcr.io/PROJECT_ID/SERVICE:ENVIRONMENT-COMMIT_SHA`) as primary tracking method
- **Cloud Run Labels**: Short SHA (7 chars) and full SHA (40 chars) labels preserved across revisions
- **Cloud Build Integration**: Automatically captures source information in build history
- **Local Deployments**: Uses `git rev-parse HEAD` to detect commit SHA
- **CI/CD Deployments**: Uses `GITHUB_SHA` environment variable from GitHub Actions
- **Fallback**: Timestamp-based identifier (`local-YYYYMMDD-HHMMSS`) when git unavailable

## Key Quotes
> "Every deployment is now traceable back to its exact source code commit."

## Connections
- [[CloudRun]] — the GCP service being tracked
- [[GitHubActions]] — CI/CD platform for automated deployments
- [[GoogleCloud]] — underlying cloud provider

## Contradictions
- None identified
