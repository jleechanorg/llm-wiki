---
title: "AI Universe Backend (Dev)"
type: entity
tags: [backend, api, gcp, cloud-run]
sources: [ai-universe-frontend-testing-report]
last_updated: 2026-04-07
---

## Description
Google Cloud Run backend service for AI Universe application, deployed at us-central1 region. Requires authentication for API access.

## Technical Details
- **URL**: https://ai-universe-backend-dev-114133832173.us-central1.run.app
- **Platform**: Google Cloud Run
- **Region**: us-central1
- **Auth**: Required (returns 401 on /api/health without credentials)

## Connections
- [[AIUniverseFrontendFinal]] — frontend consuming this backend
- [[GoogleCloudRun]] — hosting platform

## Source
[[AI Universe Frontend Testing Report]]
