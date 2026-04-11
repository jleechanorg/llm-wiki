---
title: "TDD Tests for Modal Agent & Intent Classifier Bugs (PR #5225)"
type: source
tags: [tdd, testing, modal-agent, intent-classifier, bug-fix]
source_file: "raw/test_modal_agent_intent_classifier_bugs.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite capturing 4 critical bugs identified in PR #5225: duplicate anchor phrases between CHARACTER_CREATION and LEVEL_UP modes, level-up modal lock with no exit mechanism, CHARACTER_CREATION lacking actual creation phrases, and missing stale flag guard for level-up modal lock.

## Key Claims
- **Duplicate anchor bug**: "choose feat" vs "create character" creates routing conflicts between modes
- **Modal exit bug**: Level-up modal has no exit mechanism once triggered
- **Missing creation phrases**: CHARACTER_CREATION mode has zero actual character creation phrases
- **Stale flag bug**: No guard prevents stale modal lock from blocking future interactions
- **TDD workflow**: Tests follow Red-Green-Refactor cycle to expose bugs before fixes

## Key Quotes
> "BUG #1: Duplicate anchor phrases cause routing conflicts"
> "BUG #3: CHARACTER_CREATION mode must have actual character creation phrases"

## Connections
- Related to [[Level Up Stale Flag Tests]] — both test level-up modal state management
- Related to [[Keyword Parsing Refactor]] — anchor phrase detection refactored in that work
- Related to [[GameState Tests]] — GameState is the target of modal agent state changes

## Contradictions
- None identified in current wiki
