---
title: "Apache Kafka"
type: entity
tags: [streaming, event-platform, broker-side-validation]
date: 2026-04-15
---

## Overview

Apache Kafka is an event streaming platform with broker-side schema validation. Confluent Schema Registry extends Kafka with centralized schema management.

## Key Properties

- **Broker-side validation**: Kafka validates schema IDs at the broker level in wire format
- **Schema ID Validation**: Schema Registry verifies schema IDs before message processing
- **Fail-closed**: Invalid messages cause entire batch discard
- **Formats**: Avro, Protobuf, JSON Schema

## Connections

- [[SchemaIDValidation]] — Kafka broker-side schema ID verification
- [[FailClosedValidation]] — Kafka/Confluent fail-closed batch discard pattern
- [[Confluent]] — Confluent Schema Registry extends Kafka

## See Also
- [[SchemaIDValidation]]
- [[FailClosedValidation]]