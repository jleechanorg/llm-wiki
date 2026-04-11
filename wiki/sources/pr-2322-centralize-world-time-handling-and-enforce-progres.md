---
title: "PR #2322: Centralize world time handling and enforce progression"
type: source
tags: [codex]
date: 2025-12-10
source_file: raw/prs-worldarchitect-ai/pr-2322.md
sources: []
last_updated: 2025-12-10
---

## Summary
- centralize world time parsing, comparison, and progression helpers into a shared module and wire them through the story loop
- add regression coverage for timestamp parsing plus inferred progression when the model omits time
- tighten prompt guidance so timestamp_iso drives the session header/calendar and document backend auto-advancement when time is missing

## Metadata
- **PR**: #2322
- **Merged**: 2025-12-10
- **Author**: jleechan2015
- **Stats**: +408/-124 in 6 files
- **Labels**: codex

## Connections
