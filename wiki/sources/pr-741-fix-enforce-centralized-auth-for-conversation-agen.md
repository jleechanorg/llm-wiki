---
title: "PR #741: fix: enforce centralized auth for conversation agent"
type: source
tags: [codex]
date: 2025-11-15
source_file: raw/prs-/pr-741.md
sources: []
last_updated: 2025-11-15
---

## Summary
- ensure `conversation.send-message` always resolves authentication context (even when rate limiting is disabled)
- wire `conversation.delete`, `conversation.list`, and `conversation.get-history` through `AuthContextResolver` so idToken fallback is honored everywhere
- expand the admin token verification suite to cover auth-only deployments and the additional tools

## Metadata
- **PR**: #741
- **Merged**: 2025-11-15
- **Author**: jleechan2015
- **Stats**: +217/-101 in 2 files
- **Labels**: codex

## Connections
