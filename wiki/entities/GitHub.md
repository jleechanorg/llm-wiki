---
title: "GitHub"
type: entity
tags: [vcs, platform, webhooks]
sources: []
last_updated: 2026-04-07
---

## Description
Version control platform and home of the GitHub App whose webhooks are processed by the webhook pipeline. Source of X-GitHub-Delivery IDs used for deduplication.

## Connections
- [[WebhookPipelineOperatorRunbook]] — source of webhook deliveries
- Referenced in [[SmartclawRoutingDelegationFailuresPostmortem]] for cross-repo delegation
