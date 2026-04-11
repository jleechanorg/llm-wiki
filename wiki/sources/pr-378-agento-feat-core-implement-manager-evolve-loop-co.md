---
title: "PR #378: [agento] feat(core): implement manager evolve loop config + prompt injection"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-378.md
sources: []
last_updated: 2026-04-04
---

## Summary
Implements the Manager Evolve Loop types, config, and orchestrator-prompt injection from `docs/design/manager-evolve-loop-design.md` (bd-jhv1).

### Changes

**`packages/core/src/types.ts`**
- Added `EvolveLoopConfig` interface with all fields typed and optional: `enabled`, `pollCadence` (`"lightweight" | "standard"`), `autonomousFixScopes` (string[]), `blockedScopes` (string[]), `knowledgeBaseDir` (string), `zeroTouchWindow` (`"24h" | "30d"`)
- Added `evolveLoop?: EvolveLoopConfig` field to `Pr

## Metadata
- **PR**: #378
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +876/-25 in 11 files
- **Labels**: none

## Connections
