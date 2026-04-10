---
title: "API Testing"
type: concept
tags: [testing, api, integration]
sources: []
last_updated: 2026-04-08
---

API testing validates that external service integrations work correctly. WorldArchitect's API tests verify connections to Google Gemini (for AI generation) and Firebase Firestore (for data persistence). These tests require valid credentials and are typically run manually or in dedicated test environments.

## Requirements for API Testing
- `GEMINI_API_KEY` environment variable
- `serviceAccountKey.json` for Firebase authentication
- Network access to Google Cloud services

## Connections
- [[IntegrationTestRunnerRealApiCalls]] — Bash script for API testing
- [[GoogleGemini]] — AI API being tested
- [[FirebaseFirestore]] — Database API being tested
