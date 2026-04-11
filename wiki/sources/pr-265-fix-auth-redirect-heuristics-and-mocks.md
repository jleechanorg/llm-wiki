---
title: "PR #265: Fix auth redirect heuristics and mocks"
type: source
tags: [codex]
date: 2025-11-16
source_file: raw/prs-/pr-265.md
sources: []
last_updated: 2025-11-16
---

## Summary
- add touch-capable fallback to the redirect heuristic and harden the vitest suite with proper global cleanup
- guard redirect result handling in `AuthProvider` and relax MSW handlers so requests without `userId` follow the new payload contract
- keep the auth strategy tests deterministic by restoring navigator/window state after each case

## Metadata
- **PR**: #265
- **Merged**: 2025-11-16
- **Author**: jleechan2015
- **Stats**: +52/-63 in 4 files
- **Labels**: codex

## Connections
