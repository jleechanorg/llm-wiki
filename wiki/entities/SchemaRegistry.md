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

- [[Confluent]] — Schema Registry is a Confluent product
- [[ApacheKafka]] — Schema Registry validates Kafka message schemas
- [[SchemaIDValidation]] — core validation mechanism
- [[DataContracts]] — schema registry enforces producer-consumer agreements

## See Also
- [[Confluent]]
- [[SchemaIDValidation]]