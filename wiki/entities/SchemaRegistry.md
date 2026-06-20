---
title: "Schema Registry"
type: entity
tags: [schema-management, kafka, confluent, validation]
date: 2026-04-15
---

## Overview

Schema Registry (Confluent) provides centralized schema management and validation for Kafka topic message data. It enforces compatibility checking as schemas evolve.

## Key Properties

- **Centralized schema management**: Single source of truth for topic message schemas
- **Compatibility checking**: Schema evolution with backward/forward compatibility
- **Wire format validation**: Broker-side verification of schema IDs
- **Fail-closed**: Entire batch discarded if any message is invalid

## Connections

- [Confluent](Confluent.md) — Schema Registry is a Confluent product
- [ApacheKafka](ApacheKafka.md) — Schema Registry validates Kafka message schemas
- [SchemaIDValidation](../concepts/SchemaIDValidation.md) — core validation mechanism
- [DataContracts](../concepts/DataContracts.md) — schema registry enforces producer-consumer agreements

## See Also
- [Confluent](Confluent.md)
- [SchemaIDValidation](../concepts/SchemaIDValidation.md)