---
title: "PATTERNS.md - Living Document of Observed Preferences"
type: source
tags: [patterns, preferences, workflow, documentation]
sources: []
source_file: raw/PATTERNS.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Living document capturing implicit patterns and preferences observed through GitHub history analysis and interaction patterns. Unlike CLAUDE.md (explicit rules), this captures learned behaviors with confidence levels ranging from 60-100%. Covers code style, review focus, workflow patterns, communication preferences, quality standards, and problem-solving approaches.

## Key Claims

- **Structured Commit Format**: 100% confidence — all commits follow standardized prefixes (fix:, feat:, docs:, refactor:)
- **Zero Test Tolerance**: 100% confidence — never accept partial test success, fix ALL failing tests
- **Evidence-Based Debugging**: 95% confidence — always show exact errors before proposing fixes
- **Phased Implementation**: 85% confidence — complex work broken into clear phases (investigation → implementation → testing → documentation)
- **DRY/SOLID Principles**: 95% confidence — strong preference for non-duplicated, well-organized code
- **No Temporary Comments**: 100% confidence — avoid TODO, FIXME, HACK comments, implement properly or document elsewhere
- **Root Cause Analysis**: 90% confidence — dig deep to find actual cause, not just symptoms

## Key Patterns

### Merge Conflict Resolution
- Evidence Standards docs: combine both approaches (lightweight + full capture)
- Beads merge artifacts: remove `.beads/beads.base.jsonl` and `.beads/beads.left.jsonl`

### Context-Aware Execution
- **Emergency/Fix**: Surgical changes, focused testing
- **Feature/Refactor**: Comprehensive analysis, full test suite
- **Production**: Extra validation, careful rollout

### Pattern Application Rules
1. Apply patterns with >80% confidence automatically
2. Explicit user instructions override patterns
3. Track success/failure to adjust confidence
4. When patterns conflict, prefer higher confidence or ask

## Connections

- [[ClaudeCode]] — patterns derived from Claude Code session analysis
- [[GitHub]] — patterns extracted from PR/commit history

## Contradictions

- None identified in current wiki content