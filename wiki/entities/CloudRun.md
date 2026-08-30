---
title: "Cloud Run"
type: entity
tags: [google-cloud, serverless, container]
sources: [feedback-2026-08-30-cloud-run-and-mem0-drift-guardrails]
last_updated: 2026-08-30
---

## Description
Google Cloud serverless container platform that provides the deployment target for WorldArchitect.AI. Automatically provides PORT environment variable and requires compatible logging to stdout/stderr.

## Connections
- [[GunicornConfigurationWorldarchitectAiProduction]] — deployment configuration uses Cloud Run PORT env var
- [[WorldArchitectAIDockerProductionImage]] — container image for Cloud Run deployment
- [[CloudRunTrafficRouting]] — revision readiness vs traffic routing vs endpoint resolution are separate facts; canonical deploys must pass `--to-latest`
- [[RepositoryDefaultsDoNotRemediateLiveState]] — merged capacity defaults do not update existing revisions; enumerate and remediate live services independently
