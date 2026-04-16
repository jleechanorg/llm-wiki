---
title: "Schema ID Validation"
type: concept
tags: [schema-validation, broker-side, kafka, fail-closed]
date: 2026-04-15
---

## Overview

Schema ID Validation is Kafka's broker-side verification of schema IDs in wire format. Confluent Schema Registry validates that incoming messages match registered schemas before processing.

## Key Properties

- **Broker-side**: Validation happens at the Kafka broker, not at producer
- **Wire format**: Schema ID is embedded in message wire format
- **Fail-closed**: Invalid messages cause entire batch discard
- **Quote**: "If a batch of messages is sent, and at least one is invalid, then the entire batch is discarded"

## Connection to Governance

Schema ID Validation is a model for fail-closed governance gates — the broker (gate) rejects the entire batch if any message fails validation. This is the fail-closed semantic that PR #453 proposes for merge gates.

## See Also
- [[Confluent]]
- [[ApacheKafka]]
- [[FailClosedValidation]]