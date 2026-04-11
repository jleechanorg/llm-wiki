---
title: "PR #337: [agento] feat(core): add CLI-keyed model defaults"
type: source
tags: []
date: 2026-04-01
source_file: raw/prs-worldai_claw/pr-337.md
sources: []
last_updated: 2026-04-01
---

## Summary
Model selection in AO is currently role/project-based (`agentConfig.model` + `orchestratorModel`) and does not provide a central CLI-keyed default map. This causes ambiguity when different CLIs require different model IDs. We need a default model surface that is always keyed by CLI/agent identifier.

Upstream check: ComposioHQ mirror currently does not expose `modelByCli` in core config/selection. I verified this in `/Users/jleechan/projects_reference/agent-orchestrator-mirror/packages/core/src/

## Metadata
- **PR**: #337
- **Merged**: 2026-04-01
- **Author**: jleechan2015
- **Stats**: +327/-12 in 18 files
- **Labels**: none

## Connections
