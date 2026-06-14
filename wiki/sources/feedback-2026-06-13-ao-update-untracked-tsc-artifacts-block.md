---
title: "2026-06-13 Ao Update Untracked Tsc Artifacts Block"
type: source
tags: ["feedback", "agent-orchestrator"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_ao_update_untracked_tsc_artifacts_block.md
---

## Summary
scripts/ao-update.sh

## Key Claims
- 1. `git pull --ff-only origin main` (main clone must be on main, FF-clean)
- 2. `pnpm --filter @jleechanorg/ao-core build` (rebuilds core/dist)
- 3. `pnpm --filter @jleechanorg/ao-cli build` (rebuilds cli/dist)
- 4. **Verify new code is in dist** (greps for the symbols from your PRs):
- grep -c "perPrCooldownMs" packages/core/dist/skeptic-cron-local.js
- grep -c "headSha" packages/cli/dist/commands/skeptic/mergeGate.js

## Connections
- [[AgentOrchestrator]] — AO worker dispatch memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_ao_update_untracked_tsc_artifacts_block.md`
