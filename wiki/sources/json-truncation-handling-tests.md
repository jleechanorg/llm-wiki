---
title: "JSON Truncation Handling Tests"
type: source
tags: [python, testing, json, compaction, bug-fix]
source_file: "raw/test_json_truncation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
RED test suite verifying that _compact_game_state never returns invalid JSON. When compaction would exceed budget, the function should return the original game_state instead of truncating mid-object. Currently fails because lines 579-581 truncate the JSON string, producing invalid JSON.

## Key Claims
- **_compact_game_state never returns invalid JSON**: Function must return valid JSON or original input
- **Budget exceeded = original returned**: When compacted JSON exceeds max_chars, return original game_state
- **Truncation bug in lines 579-581**: Code truncates with `compacted_json[:max_chars]`, breaking JSON structure
- **Test matrix [3,1,1] through [3,2,4]**: 8 tests covering edge cases for budget handling

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| [3,1,1] | Fits budget | Return compacted JSON |
| [3,1,2] | Exactly at budget | Return compacted JSON |
| [3,1,3] | Slightly over budget | Return original (valid) |
| [3,1,4] | Way over budget | Return original with warning |
| [3,2,1] | Truncation mid-object | Return original (safe fallback) |

## Connections
- [[CompactGameState]] — function being tested
- [[JSONCompaction]] — concept being validated
- [[ContextCompaction]] — module containing the bug
