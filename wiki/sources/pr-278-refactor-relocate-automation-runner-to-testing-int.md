---
title: "PR #278: refactor: relocate automation runner to testing_integration"
type: source
tags: [codex]
date: 2025-10-11
source_file: raw/prs-/pr-278.md
sources: []
last_updated: 2025-10-11
---

## Summary
- relocate the automation runner package, manifest, and CLI entrypoint under testing_integration
- update the run-all-tests wrapper and CLI defaults to reference the new paths
- add a package initializer so testing_integration can expose the runner module

## Metadata
- **PR**: #278
- **Merged**: 2025-10-11
- **Author**: jleechan2015
- **Stats**: +672/-118 in 10 files
- **Labels**: codex

## Connections
