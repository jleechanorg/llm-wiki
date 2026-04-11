---
title: "AO Cursor Workers — 7-Green Queue (No Auto-Merge)"
type: source
tags: [agent-orchestrator, cursor, skeptic, ci, auto-merge, github-actions, workflow]
source_file: "raw/ao-cursor-workers-7-green-queue.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Operational guide for configuring Agent Orchestrator (AO) and Cursor workers to drive fixes until 7-green status (CI + CR + Bugbot + threads + evidence + skeptic verdict) while preventing automatic merges via skeptic-cron. Uses GitHub repository variables to manage a denylist of PRs that should never auto-merge.

## Key Claims
- **Denylist mechanism**: `SKEPTIC_MERGE_DENYLIST` variable holds comma-separated PR numbers never merged by skeptic-cron
- **Auto-merge toggle**: `SKEPTIC_CRON_AUTO_MERGE` set to `false` disables all automatic merges
- **7-green definition**: CI passes + CR passes + Bugbot passes + threads resolved + evidence verified + skeptic posts VERDICT: PASS
- **Manual merge workflow**: Operators set denylist, run AO/Cursor until 7-green, merge manually when ready

## Key Commands
```bash
# Set denylist for open PRs
gh variable set SKEPTIC_MERGE_DENYLIST -b '6094,6086,6093,6095,6034,6069' -R jleechanorg/worldarchitect.ai

# Clear denylist to enable auto-merge
gh variable delete SKEPTIC_MERGE_DENYLIST -R jleechanorg/worldarchitect.ai
```

## Current PR Queue
| Priority | Bead | PR | Focus |
|----------|------|-----|--------|
| P0 | rev-n2td | #6094 | Self-hosted MVP shards / Firestore transaction |
| P0 | rev-3srb | #6086 | Deploy gcloud --quiet / ABORTED retry |
| P1 | rev-smrb | #6093 | JWT / auth hardening |
| P1 | rev-1j5h | #6095 | Core test infra + skeptic workflows |
| P1 | rev-zz65 | #6034 | Custom Campaign Wizard re-enable |
| P1 | rev-bn76 | #6069 | Skeptic align with AO |


## Connections
- [[AgentOrchestrator]] — orchestrates Cursor/Codex workers for PR automation
- [[Cursor]] — AI code editor used as worker for running fixes
- [[Skeptic]] — CI workflow that posts VERDICT after 7-green check
- [[WorldArchitectAI]] — target repository for PRs

## Workflow
1. Set `SKEPTIC_MERGE_DENYLIST` to open PRs requiring manual merge
2. Run AO/Cursor workers until all checks pass
3. Verify skeptic posts "VERDICT: PASS" on current head SHA
4. Merge manually when ready
5. Remove PR numbers from denylist or delete variable entirely
