---
title: "Autonomous Sanctuary Mode Tests"
type: source
tags: [testing, sanctuary, autonomy, MCP, E2E]
sources: [worldarchitect.ai-testing_mcp-sanctuary_autonomy_analysis.md-bd149cb6.md]
source_file: testing_mcp/test_sanctuary_autonomous.py
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Test suite validating Sanctuary Mode works autonomously — LLM recognizes quest completion without explicit "quest complete" language. Includes 4 scenarios: autonomous activation (statistical), natural expiration, overwrite protection, and duration scales.

## Key Claims
- **Autonomous Activation**: Statistical test requiring 70%+ success rate across 10 runs — LLM activates sanctuary after neutral action with NO completion keywords
- **Natural Expiration**: Deterministic test verifying sanctuary expires at `expires_turn` without intervention
- **Overwrite Protection**: Epic sanctuary (20 turns) not overwritten by Medium completion (5 turns)
- **Duration Scales**: All 4 scales produce correct durations (minor=3, medium=5, major=10, epic=20 turns)
- **Trigger Source Logging**: Logs `trigger_source` to prove autonomous detection (boss_defeated, dungeon_cleared, etc.)

## Test Scenarios

### 1. Autonomous Activation (Statistical)
- 10 iterations (3 with `--quick` flag)
- Success rate required: 70%+
- Tests LLM autonomously activates sanctuary after boss defeat
- Player says neutral action ("I search Klarg's body") with NO completion keywords

### 2. Natural Expiration (Deterministic)
- Activate sanctuary → advance turns past expiration → verify `active: false`

### 3. Overwrite Protection (Deterministic)
- Complete Epic arc → advance to turn 15 → complete Medium quest → verify Epic preserved

### 4. Duration Scales (Parameterized)
- Tests all 4 scales: minor=3, medium=5, major=10, epic=20 turns

## Key Features
- ✅ Uses shared utilities from `testing_mcp/lib/` — no reimplementation
- ✅ Follows `.claude/skills/evidence-standards.md`
- ✅ Logs trigger_source to prove autonomous detection
- ✅ Statistical validation (70%+ success rate)
- ✅ Tests run against real MCP server (not mocks)

## Execution Time
- Quick mode (3 runs): ~5-10 minutes
- Full mode (10 runs): ~15-30 minutes

## Connections
- [[Sanctuary Mode Autonomy Analysis]] — this test suite validates the analysis by testing autonomous activation
- [[Testing MCP]] — uses the testing framework's shared utilities

## Contradictions
- None — complements existing analysis by testing whether autonomous activation works in practice
