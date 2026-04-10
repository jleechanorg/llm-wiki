---
title: "Gunicorn"
type: entity
tags: [web-server, python, wsgi, production]
sources: ["gunicorn-configuration-tdd-tests"]
last_updated: 2026-04-08
---

## Overview
Gunicorn (Green Unicorn) is a Python WSGI HTTP server for Unix systems. Used in production deployments to serve Python web applications with worker process management.

## In This Wiki
- [[GunicornConfigurationTddTests]] — TDD test suite validating gunicorn.conf.py configuration

## Key Properties
- **Worker class**: gthread (threaded)
- **Default formula**: (2 * CPU cores) + 1 workers
- **Default threads**: 4 per worker
- **Default timeout**: 600 seconds for long-running operations

## Configuration
Gunicorn configuration is defined in `gunicorn.conf.py` at the project root. Supports environment variable overrides:
- `GUNICORN_WORKERS` — worker count
- `GUNICORN_THREADS` — threads per worker  
- `WORLDARCH_TIMEOUT_SECONDS` — timeout value
