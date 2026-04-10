---
title: "Container Image Tagging"
type: concept
tags: [containers, versioning, deployment]
sources: [cloud-run-commit-sha-tracking]
last_updated: 2026-04-07
---

Container Image Tagging is the practice of labeling container images with version identifiers for traceability. In this implementation, images are tagged with commit SHA (e.g., `dev-a1b2c3d`) alongside a `latest` tag, enabling direct correlation between deployed containers and source code.

## Implementation
- Format: `gcr.io/PROJECT_ID/SERVICE:ENVIRONMENT-COMMIT_SHA`
- Additional tag: `ENVIRONMENT-latest`
- Example: `gcr.io/worldarchitecture-ai/mvp-site-app:dev-a1b2c3d`

## Related Concepts
- [[ContainerRegistry]] — image storage
- [[CloudRun]] — deployment target

## Wiki Connections
- Primary method in: [[Cloud Run Commit SHA Tracking]]
