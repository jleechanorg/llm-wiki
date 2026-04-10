---
title: "Cloud Build"
type: concept
tags: [cicd, gcp, build]
sources: [cloud-run-commit-sha-tracking]
last_updated: 2026-04-07
---

Cloud Build is Google's CI/CD platform that builds, tests, and deploys containers. Automatically captures source commit information in build history, providing an additional layer of traceability for deployments triggered through Cloud Build.

## Usage
- Lists builds with commit information: `gcloud builds list`
- Filter by commit: `--filter="source.repoSource.commitSha=<COMMIT_SHA>"`
- Shows: build ID, status, source commit, images

## Related Concepts
- [[GoogleCloud]] — hosting platform
- [[GitHubActions]] — alternative CI/CD

## Wiki Connections
- Referenced in: [[Cloud Run Commit SHA Tracking]]
