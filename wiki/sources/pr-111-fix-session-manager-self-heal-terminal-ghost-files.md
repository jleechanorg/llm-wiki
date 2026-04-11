---
title: "PR #111: fix(session-manager): self-heal terminal ghost files blocking orchestrator respawn"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-111.md
sources: []
last_updated: 2026-03-23
---

## Summary
The `ai.agento.orchestrators` launchd daemon (KeepAlive=true) was silently failing to start `ao-orchestrator` and `wa-orchestrator` on every retry. The error in `/tmp/ao-orchestrators.err.log`:

```
✖ Orchestrator setup failed
Error: Failed to setup orchestrator: Session ao-orchestrator already exists but is not in a reusable state
```

Root cause: when lifecycle-manager marks an orchestrator session as `killed`, it writes a metadata file (`status=killed\nrole=orchestrator\n`) with **no `runtime

## Metadata
- **PR**: #111
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +45/-0 in 2 files
- **Labels**: none

## Connections
