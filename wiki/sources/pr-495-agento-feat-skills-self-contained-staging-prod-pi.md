---
title: "PR #495: [agento] feat(skills): self-contained staging→prod pipeline skill"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-495.md
sources: []
last_updated: 2026-04-04
---

## Summary
The OpenClaw staging→production deployment pipeline is spread across multiple scripts (deploy.sh, staging-canary.sh, gateway-preflight.sh, install-launchagents.sh), launchd plist templates, and CLAUDE.md sections. A new machine setting up from scratch had no single place to reference — the knowledge was implicit in the code and incident history.

## Metadata
- **PR**: #495
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +395/-0 in 1 files
- **Labels**: none

## Connections
