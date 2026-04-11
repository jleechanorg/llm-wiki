---
title: "PR #300: chore: deprecate 12 orchestration modules duplicated by agent-orchestrator"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-300.md
sources: []
last_updated: 2026-03-20
---

## Summary
The jleechanclaw repo contains 12 Python orchestration modules (`src/orchestration/`) that were originally built as the MVP implementation. These modules have since been superseded by production-quality TypeScript equivalents in [agent-orchestrator](https://github.com/jleechanorg/agent-orchestrator). Maintaining both creates drift risk, duplicated bug fixes, and confusion about which is canonical.

Related: bd-aa3 dedup tracker bead

## Metadata
- **PR**: #300
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +2146/-567 in 22 files
- **Labels**: none

## Connections
