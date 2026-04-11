---
title: "Merge Decisions: Faction Minigame Branch"
type: source
tags: [merge-decisions, faction-minigame, evidence-standards, unit-tests, testing, refactoring]
sources: []
source_file: worldarchitect.ai-docs-merge_decisions_pr_faction_minigame.md
date: 2025-12-30
last_updated: 2026-04-07
---

## Summary

Merge decisions for branch `claude/add-force-creation-system-Mxqh0` merged from `origin/main` on 2025-12-30. Key resolution combined HEAD's additions (test execution artifacts, git provenance) with main's additions (JSONL and server logs) into unified evidence standards checklist. New features added: Unit Test Evidence Standards, Test Execution Evidence requirements, and unit test support in /generatetest command. Refactored `testing_mcp/faction/test_unit.py` to use centralized `lib/evidence_utils.py`, removing ~100 lines of duplicated code.

## Key Claims

- **Combined Evidence Checklist**: Merged both branch additions into unified requirements covering ALL evidence files (JSONL, server logs, test execution artifacts, git provenance)
- **Unit Test Evidence Standards**: Clarified that unit tests (no server) still need proper evidence with required vs optional fields
- **Test Execution Evidence**: New requirement mandates command line, raw stdout/stderr, and exit code captured to `artifacts/`
- **Git Provenance File**: Full git provenance output now saved as `git_provenance_full.txt` with checksum
- **Code Deduplication**: `testing_mcp/faction/test_unit.py` refactored to use centralized `lib/evidence_utils.py`, removing ~100 lines of duplicated evidence capture code
- **Unit Test Support in /generatetest**: Added keyword detection for unit tests and template for unit test generation

## Key Quotes

> "Combined both additions into a unified checklist item: Checksums: SHA256 for ALL evidence files including JSONL and server logs (via write_with_checksum())"

> "Test execution evidence: command + stdout/stderr + exit code saved to artifacts/"

> "testing_mcp/faction/test_unit.py now uses centralized lib/evidence_utils.py - Removed ~100 lines of duplicated evidence capture code"

## Files Changed

- `.claude/skills/evidence-standards.md` - Added Unit Test Evidence section
- `.claude/commands/generatetest.md` - Added unit test support + merged checklist
- `testing_mcp/faction/test_unit.py` - Refactored to use lib utilities
- `.claude/commands/savetmp.py` - Enhanced for test execution artifacts

## Connections

- [[EvidenceStandards]] — extends evidence-standards.md with unit test section
- [[GenerateTestCommand]] — /generatetest command enhanced for unit test detection
- [[TestingMCP]] — faction minigame testing infrastructure

## Contradictions

- None identified - this merge combines complementary additions rather than conflicting ones