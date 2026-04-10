---
title: "Gunicorn"
type: concept
tags: [web-server, python, wsgi]
sources: []
last_updated: 2026-04-08
---

## Description
Python WSGI HTTP server for production deployments. Uses worker processes to handle concurrent requests. WorldArchitect.AI uses gthread workers for I/O-bound workloads.

## Key Details
- **Worker class**: gthread (threaded workers for I/O-bound tasks)
- **Concurrency**: workers × threads = simultaneous requests
- **Timeout**: aligned with downstream service limits

## Connections
- [[GunicornConfigurationWorldarchitectAiProduction]] — production configuration for WorldArchitect.AI
