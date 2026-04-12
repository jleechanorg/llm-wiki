---
title: "GCP Artifact Registry Cost"
type: concept
tags: [GCP, cost, artifact-registry, Cloud-Run, billing]
last_updated: 2026-04-06
---

GCP Artifact Registry at ~$252/month (+41% MoM). Root cause: many `mvp-site-app` digests per day indicate CI without retention.

## Cost Breakdown

- `worldarchitecture-ai` `us/gcr.io` ~2.62 TB
- `ai-universe-2025` `us/gcr.io` ~282 GB
- Regional Cloud Run source repos negligible

## Root Cause

CI pipeline builds new container images without Docker layer caching or retention policy. Each PR run creates new digest, adding to registry size.

## Fixes Needed

- Add Docker lifecycle policy to prune untagged images
- Configure retention on gcr.io
- Review CI pipeline for unnecessary image builds
- Implement preview-service janitor for PR preview services

## Also Found

Legacy `mvp-site-app-pr-*` Cloud Run services persisted outside rotating pool cleanup. Dedicated self-hosted janitor workflow now prunes closed-PR services.

## Connections

- [[CronJobAutomation]] — scheduled janitor automation
- [[GreenGate]] — CI pipeline that builds images
