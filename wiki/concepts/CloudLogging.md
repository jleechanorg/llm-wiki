---
title: "Cloud Logging"
type: concept
tags: [cloud, logging, google-cloud, gcp, production]
sources: ["centralized-logging-utility"]
last_updated: 2026-04-08
---

## Definition
Google Cloud Logging (formerly Stackdriver Logging) provides centralized logging for applications running on Google Cloud Platform. Logs are accessible via the Cloud Logging console and can be filtered, searched, and analyzed.

## Key Features
- **Unified Logging**: Aggregates logs from multiple sources (VM instances, containers, Cloud Run, App Engine)
- **Log Routing**: Filter and route logs to different sinks (Cloud Storage, BigQuery, Pub/Sub)
- **Log Retention**: Configurable retention periods for different log types
- **Error Reporting**: Automatic error grouping and tracking

## Usage in This Source
The centralized logging utility outputs to Cloud Logging via stdout/stderr, which is the standard mechanism for containerized applications on GCP. Combined with file logging to /tmp for local development.

## Connections
- [[PythonLogging]] — underlying logging mechanism that writes to stdout/stderr
- [[GunicornProductionConfiguration]] — web server often deployed on GCP with Cloud Logging integration
- [[FirestoreService]] — GCP service that would use Cloud Logging for operational visibility
