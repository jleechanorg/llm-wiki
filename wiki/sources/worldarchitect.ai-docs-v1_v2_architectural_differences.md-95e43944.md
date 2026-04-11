---
title: "V1/V2 Architectural Differences Reference"
type: source
tags: [worldarchitect, architecture, v1, v2, react, flask, migration, debugging]
sources: []
last_updated: 2026-04-07
---

## Summary
Technical reference for understanding fundamental architectural differences between V1 (Flask/server-side) and V2 (React/client-side) implementations of WorldArchitect.AI. Covers core architecture comparison, critical implementation differences in campaign data loading, data format conversion, common integration issues, and debugging patterns.

## Key Claims
- **V1 Architecture**: Flask with Jinja2 templates, server-side data fetching before page render, server maintains session state
- **V2 Architecture**: React with TypeScript, client-side API calls after component mount, React state hooks and context
- **Data Format V1**: `{actor, text, mode, timestamp}` — actor is "gemini" | "user" | "system"
- **Data Format V2**: `{id, type, content, timestamp, author, choices?}` — author is "player" | "ai" | "system", type is "narration" | "action" | "dialogue" | "system" | "choices"
- **Common Issues**: Missing API calls in V2 components, data format mismatches between versions, V1 server-side auth vs V2 client-side token management, V2 state initialization requiring explicit loading

## Key Quotes
> "V2 components assume data is available without explicit loading" — solution: add `apiService.getCampaign(campaignId)` calls in useEffect hooks
> "V1 and V2 expect different data structures" — solution: implement format conversion functions when loading V1 data into V2 components

## Connections
- [[WorldArchitect.AI]] — the platform being migrated from V1 to V2
- [[Testing Design Document]] — covers testing strategy for both versions

## Contradictions
- None identified — this is a technical reference document, not a claim-making document
