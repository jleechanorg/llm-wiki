---
title: "Canonical Code Patterns"
type: concept
tags: [canonical, python, typescript, rust, fastapi, requests, pydantic, sqlalchemy, celery, trpc, tanstack-query, tokio]
sources: []
last_updated: 2026-04-14
---

## Summary

Canonical code patterns are the defining architectural and stylistic choices made by the world's most respected open-source codebases. Studying these patterns — FastAPI's typed exceptions, Requests' elegant API surface, tRPC's end-to-end type inference, TanStack Query's reactive state machine, and Tokio's composable async primitives — provides a north star for evaluating any generated code.

## Key Canonical Repos

| Repo | Primary Strength | Key Pattern |
|------|-----------------|-------------|
| [FastAPIErrorHandling](FastAPIErrorHandling.md) | Exception hierarchy | Typed HTTP exceptions with docstrings |
| [RequestsAPIDesign](RequestsAPIDesign.md) | API simplicity | Flat request functions, session composition |
| [PydanticPatterns](PydanticPatterns.md) | Type validation | BaseModel, Field(), ValidationError, discriminated unions |
| [SQLAlchemyPatterns](SQLAlchemyPatterns.md) | ORM patterns | sessionmaker, DeclarativeBase, select(), object state machine |
| [CeleryPatterns](CeleryPatterns.md) | Task queue | bind=True tasks, autoretry/backoff, canvas primitives |
| [tRPCTypeSafety](tRPCTypeSafety.md) | End-to-end types | Procedure generics, input/output inference |
| [TanStackQueryState](TanStackQueryState.md) | State caching | Observer pattern, query key hashing |
| [AxumAsyncPatterns](AxumAsyncPatterns.md) | Composable handlers | Layered middleware, From extraction |

## How to Use

See the `canonical_code_scorer` skill for scoring any generated code against these 5 repos on: naming consistency, error handling, type safety, architecture, and test coverage signal.

## Connections

- [FastAPIErrorHandling](FastAPIErrorHandling.md) — Python async, typed errors
- [RequestsAPIDesign](RequestsAPIDesign.md) — Simple & correct API design
- [tRPCTypeSafety](tRPCTypeSafety.md) — TypeScript end-to-end types
- [TanStackQueryState](TanStackQueryState.md) — React Query state management
- [AxumAsyncPatterns](AxumAsyncPatterns.md) — Rust async composable handlers
- [CanonicalCodeScorer](CanonicalCodeScorer.md) — Quantitative scoring engine that evaluates generated code against these canonical repos using a 6-dimension rubric (70%) + token-level diff similarity (30%)
