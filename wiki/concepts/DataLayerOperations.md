---
title: "Data Layer Operations"
type: concept
tags: [architecture, data, firestore]
sources: [numeric-field-converter-utilities]
last_updated: 2026-04-08
---

## Definition
The layer of an application responsible for reading from and writing to persistent data stores. In WorldArchitect.AI, this includes Firestore document operations.

## Application in This Source
`NumericFieldConverter` is designed specifically for Firestore data layer operations where simple type conversion is needed without smart defaults or complex fallbacks.

## Related Concepts
- [[Firestore]] — Google Cloud Firestore NoSQL database
- [[Document Schema]] — structured data in Firestore collections
- [[Type Coercion]] — converting string values from JSON to proper types
