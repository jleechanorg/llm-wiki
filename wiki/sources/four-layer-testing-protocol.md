---
title: "Four-Layer Testing Protocol (/4layer)"
type: source
tags: [testing, protocol, unit-tests, e2e, browser-testing]
sources: []
last_updated: 2026-04-14
---

## Summary

Four-Layer Minimal Repro Testing Protocol that climbs the testing ladder in order: Unit Tests -> End-to-End Tests -> MCP/HTTP API Tests -> Browser Tests. Stop climbing when blocker is conclusively reproduced.

## Key Claims

- Layer 1 (Unit Tests): Fastest (seconds), tests isolated modules/functions
- Layer 2 (End-to-End Tests): Fast (seconds-minutes), full backend flow with mocked external services
- Layer 3 (MCP/HTTP API Tests): Medium (minutes), real server with MCP/HTTP API calls
- Layer 4 (Browser Tests): Slowest (minutes-tens of minutes), full UI automation with real browser
- Classification: Unit layer failure = backend logic bug, End2end = integration/API issue, MCP = server/MCP protocol issue, Browser = UI/frontend issue
- Evidence requirements: Full paths, log lines, screenshots, exact evidence directory

## Key Quotes

> "Stop climbing when blocker is reproduced — Don't waste time on higher layers"

> "Always attach concrete evidence — Full paths, log lines, screenshots"

## Connections

- [[HarnessEngineering]] — Testing quality validation
- [[CommandSystemDocumentation]] — Testing command suite (/test, /tdd, /testui)

## Contradictions

- None identified
