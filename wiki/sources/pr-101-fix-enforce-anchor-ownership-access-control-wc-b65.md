---
title: "PR #101: fix: enforce anchor ownership access control (WC-b65)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-101.md
sources: []
last_updated: 2026-03-26
---

## Summary
`anchorHash` in `packages/backend/src/network/chain_anchor.ts` allows any caller to overwrite any entity anchor because the `anchorOwners` map is never populated. Ownership recording was deferred to after successful RPC tx confirmation, but since the RPC stub never succeeds, no ownership is ever recorded — making `isAnchorOwnerAuthorized` always return `true`.

## Metadata
- **PR**: #101
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +238/-3 in 2 files
- **Labels**: none

## Connections
