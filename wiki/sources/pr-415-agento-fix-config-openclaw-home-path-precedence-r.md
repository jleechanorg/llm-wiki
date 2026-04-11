---
title: "PR #415: [agento] fix(config): OpenClaw home path precedence + roadmap (bd-9nvf, bd-qaiz)"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldai_claw/pr-415.md
sources: []
last_updated: 2026-04-09
---

## Summary
- **`findConfigFile`**: Prefer `~/.openclaw_prod` / `~/.openclaw` home config paths via `packages/core/src/user-home-config-paths.ts` (keeps `config.ts` free of `openclaw` literals for wholesome fork-isolation).
- **Tests**: `packages/core/src/__tests__/config.find-config.test.ts` (Vitest).
- **Harness / tracking**: `roadmap/README.md`, beads **bd-9nvf**, **bd-qaiz**; default PR template aligns labels with Evidence Gate parsers.

## Metadata
- **PR**: #415
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +123/-0 in 6 files
- **Labels**: none

## Connections
