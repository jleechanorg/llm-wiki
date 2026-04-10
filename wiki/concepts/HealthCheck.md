---
title: "Health Check"
type: concept
tags: [monitoring, deployment, DevOps]
sources: [ai-universe-frontend-testing-report]
last_updated: 2026-04-07
---

## Description
An HTTP endpoint that verifies a service is running and operational. Used by deployment platforms and load balancers to determine if a service should receive traffic.

## Usage
- **AI Universe Health Endpoint**: /api/health
- **Response**: Returns 401 when authentication is required (expected behavior)
- **Render Health Check**: HEAD / request succeeds

## Source
[[AI Universe Frontend Testing Report]]
