---
title: "HMAC-SHA256 Validation"
type: concept
tags: [security, validation, webhooks, cryptography]
sources: []
last_updated: 2026-04-07
---

## Description
Cryptographic signature validation method used to verify that webhook payloads originate from GitHub. The webhook pipeline validates HMAC-SHA256 signatures before processing incoming requests.

## Connections
- Used by [[WebhookPipelineOperatorRunbook]] for ingress security
- Related to [[FailClosedErrorHandling]] — invalid signatures result in request rejection
