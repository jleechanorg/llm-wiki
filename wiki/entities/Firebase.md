---
title: "Firebase"
type: entity
tags: [service, backend, database, google]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Description
Google's mobile and web application development platform providing Firestore database for WorldArchitect.AI campaign data persistence. Requires service account credentials and clock skew patch handling.

## Key Features
- **Firestore**: NoSQL database for campaign and game state storage
- **Service Account Credentials**: File-based or environment variable authentication
- **Clock Skew Patch**: Custom handling for time-ahead credential issues

## Connections
- [[WorldArchitect.AI]] — uses Firebase for data persistence
