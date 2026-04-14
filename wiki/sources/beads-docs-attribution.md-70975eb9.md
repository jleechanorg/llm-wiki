---
title: "Beads Attribution — beads-merge"
type: source
tags: [beads, merge, attribution, open-source, 3-way-merge]
date: 2026-04-07
source_file: beads-merge attribution in bd/docs
last_updated: 2026-04-07
---

## Summary
The 3-way merge functionality in `internal/merge/` of bd is based on **beads-merge** by @neongreen (Emily). The vendored algorithm provides field-level 3-way merge logic, issue identity matching, dependency/label merging with deduplication, and conflict marker generation. Exposed as `bd merge` CLI command and library API.

## Key Claims
- **Vendored from**: beads-merge by @neongreen (https://github.com/neongreen/mono/tree/main/beads-merge)
- **Integration discussion**: https://github.com/neongreen/mono/issues/240
- **Adapted for bd**: Uses bd's `internal/types.Issue` instead of custom types, integrated with JSONL export/import
- **bd-specific fields**: Support for Design, AcceptanceCriteria, and other bd-specific fields added
- **License**: MIT License

## Key Quotes
> "Special thanks to @neongreen for building beads-merge and graciously allowing us to integrate it into bd. This solves critical multi-workspace sync issues and makes beads much more robust for collaborative workflows."

## Connections
- [[Beads Changelog]] — related project updates
- [[Neongreen]] — original author (vendored beads-merge library)

## Contradictions
- None identified

## What is 3-Way Merge
3-way merge is an algorithm that takes three versions of data (base, theirs, yours) and produces a merged result by comparing changes from the base to each side, identifying conflicts, and applying non-conflicting changes automatically.