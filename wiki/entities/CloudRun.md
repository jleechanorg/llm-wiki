---
title: "Cloud Run"
type: entity
tags: [google-cloud, serverless, container]
sources: []
last_updated: 2026-04-08
---

## Description
Google Cloud serverless container platform that provides the deployment target for WorldArchitect.AI. Automatically provides PORT environment variable and requires compatible logging to stdout/stderr.

## Connections
- [[GunicornConfigurationWorldarchitectAiProduction]] — deployment configuration uses Cloud Run PORT env var
- [[WorldArchitectAIDockerProductionImage]] — container image for Cloud Run deployment
- [[CloudRunTrafficRouting]] — revision readiness vs traffic routing vs endpoint resolution are separate facts; canonical deploys must pass `--to-latest`
