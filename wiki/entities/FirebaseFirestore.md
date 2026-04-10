---
title: "Firebase Firestore"
type: entity
tags: [database, firebase, google]
sources: []
last_updated: 2026-04-08
---

Firebase Firestore is Google's NoSQL cloud database. WorldArchitect uses Firestore for persistent game state storage. Integration tests require a `serviceAccountKey.json` file in the project root for authentication.

## Connections
- [[IntegrationTestRunnerRealApiCalls]] — Uses Firestore for live API testing
- [[RealServiceProviderImplementation]] — Real Firestore provider implementation
