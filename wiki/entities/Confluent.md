---
title: "Confluent"
type: entity
tags: [streaming, schema-registry, kafka, stream-governance]
date: 2026-04-15
---

## Overview

Confluent provides stream governance via Schema Registry and Control Center. It implements broker-side validation with fail-closed semantics — invalid messages discard the entire batch.

## Key Properties

- **Schema Registry**: Centralized schema management and validation for Kafka topics
- **Stream Governance**: Three pillars — Stream Lineage, Stream Catalog, Stream Quality
- **Fail-closed validation**: "If a batch of messages is sent, and at least one is invalid, then the entire batch is discarded"
- **Schema formats**: Avro, Protobuf, JSON Schema
- **Control Center**: Monitoring and governance dashboard

## Connections

- [[StreamGovernance]] — Confluent's core governance concept
- [[SchemaIDValidation]] — broker-side schema ID verification
- [[DataContracts]] — producer-consumer schema agreements
- [[FailClosedValidation]] — Confluent's fail-closed batch discard pattern

## See Also
- [[StreamGovernance]]
- [[FailClosedValidation]]