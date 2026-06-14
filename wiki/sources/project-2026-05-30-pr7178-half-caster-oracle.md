---
title: "Project 2026-05-30 Pr7178 Half Caster Oracle"
type: source
tags: [project, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/project_2026-05-30_pr7178_half_caster_oracle.md
---

## Summary

PR 7178 at still encodes Paladin/Ranger spell-slot progression in backend code: maps half-casters to , then indexes . returns state unchanged, so this is warn-only telemetry/test-oracle code rather than runtime mutation. Review claims should distinguish "model owns the persisted commit" from "backend contains a deterministic oracle for validation." The user explicitly asked whether the half-caster thing is prompt-only; answering "prompt-owned" without the backend-oracle distinction would overstate the design.

## Key Claims

- (See raw memory file for full content)

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
