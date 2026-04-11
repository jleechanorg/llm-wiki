---
title: "PR #8: [P1] feat(hooks): AO lifecycle hook + GitHub Actions workflow for novel entries"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-/pr-8.md
sources: []
last_updated: 2026-03-26
---

## Summary
Implements **P1-1** of the [Phase 2 Roadmap](docs/superpowers/plans/2026-03-26-phase2-roadmap.md) — AO Lifecycle Hooks.

- `src/hooks/event-schema.ts`: TypeScript types for `PrEvent` and `PrEventType`
- `src/hooks/ao-lifecycle.ts`: `handlePrEvent()` — triggers `branch-entry` novel pipeline on `pr_opened` / `pr_merged` / `pr_closed`; skips all other event types. Includes `buildCliArgs()` helper and `defaultRunCli()` spawn implementation.
- `tests/ao-lifecycle.test.ts`: 8 unit tests (vi.fn() mock

## Metadata
- **PR**: #8
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +738/-0 in 26 files
- **Labels**: none

## Connections
