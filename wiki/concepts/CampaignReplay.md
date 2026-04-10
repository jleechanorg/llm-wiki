---
title: "Campaign Replay"
type: concept
tags: [testing, methodology, integration-test]
sources: [sariel-campaign-replay-desync-measurement]
last_updated: 2026-04-08
---

## Definition
Testing methodology that re-executes a campaign with fixed inputs to measure consistency and state tracking accuracy across multiple runs.

## Purpose
- Validate entity tracking consistency
- Identify desync patterns across interaction sequences
- Provide statistical significance through repeated runs

## Implementation
From the test script:
- Uses Flask test client for integration testing
- Executes 10 replay iterations
- Captures LLM responses at each step
- Compares against expected entity definitions
- Outputs detailed JSON results

## Key Insight
The "Cassian problem" is documented as a known edge case in campaign replay testing — indicating that certain entity tracking scenarios require special handling.

## Related
- [[DesyncMeasurement]] — The measurement approach
- [[IntegrationTest]] — Broader testing category
