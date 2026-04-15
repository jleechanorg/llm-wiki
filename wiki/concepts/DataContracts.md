---
title: "Data Contracts"
type: concept
tags: [data-contracts, producer-consumer, schema-agreements, governance]
date: 2026-04-15
---

## Overview

Data Contracts are producer-consumer schema agreements that define what data gets in. They enforce compatibility between data producers and consumers in streaming systems.

## Key Properties

- **Producer-consumer agreements**: Formal contracts for schema compatibility
- **Schema evolution**: Data contracts define compatibility rules for schema changes
- **Enforcement**: Data contracts are validated at write time
- **Governance**: Data contracts are a governance tool for data quality

## Connection to Governance

Data contracts are a governance pattern — the same concept could apply to PR governance: what constraints must a PR satisfy before being eligible for merge? Data contracts == merge requirements.

## See Also
- [[StreamGovernance]]
- [[GovernanceLayer]]