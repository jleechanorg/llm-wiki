---
title: "Reference 2026-05-30 Agentf Repo Map"
type: source
tags: [project, reference, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/reference_2026-05-30_agentf_repo_map.md
---

## Summary

26 repos cloned to . Key repos: — new ERP (249 Prisma models, multi-GAAP, event-sourced, ~80K LOC) — Software Factory (prompt → requirements/plan docs, Pillars 1-2 only; 3-5 are UI shells) — NestJS backend, 30+ modules, 51K prod LOC, 2 tenants (Gemineers + Juna Tech) — v1 SaaS, 130K prod LOC (largest codebase, likely sunset) — React/Zustand/ReactFlow frontend, 192 commits — data pipelines (Personio HR, eGora POS ETL) , , — Digital CFO chat apps , , , Full session research 2026-05-30; detail in Use this map when working in any Agnt-F repo to understand cross-repo dependencies and migration direction (v1 agf-accounting → erp rewrite).

## Key Claims

- `erp` — new ERP (249 Prisma models, multi-GAAP, event-sourced, ~80K LOC)
- `factory` — Software Factory (prompt → requirements/plan docs, Pillars 1-2 only; 3-5 are UI shells)
- `agf-api` — NestJS backend, 30+ modules, 51K prod LOC, 2 tenants (Gemineers + Juna Tech)
- `agf-accounting` — v1 SaaS, 130K prod LOC (largest codebase, likely sunset)
- `agent-f.ai` — React/Zustand/ReactFlow frontend, 192 commits
- `agf-lambda` — data pipelines (Personio HR, eGora POS ETL)
- `agentf-prod-mvp`, `gemineers`, `juna-tech` — Digital CFO chat apps

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
