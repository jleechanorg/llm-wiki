---
title: "PR #6261: [antig] refactor(rewards): migrate to centralized robust numeric extraction"
type: test-pr
date: 2026-04-14
pr_number: 6261
files_changed: [defensive_numeric_converter.py, test_defensive_numeric_central_robustness.py, world_logic.py, test_rewards_box_robustness.py]
---

## Summary
Centralizes robust numeric parsing in `DefensiveNumericConverter` using regex to extract numbers from messy LLM strings like "850 XP", "1,000 gp", "10/20". Removes redundant helper functions (`_extract_reward_value`, `_get_raw`) from `world_logic.py` and replaces with Python's native `or` chaining.

## Key Changes
- **defensive_numeric_converter.py**: Added regex-based numeric extraction using `re.search(r"[-+]?[0-9]*\.?[0-9]+", value.replace(",", ""))` - handles commas, units, fractions
- **world_logic.py**: Deleted `_extract_reward_value` and `_get_raw` helpers; replaced with native `or` chaining
- **test_defensive_numeric_central_robustness.py**: New test verifying regex extraction for HP, XP, gold, AC fields
- **test_rewards_box_robustness.py**: E2E test that tries to provoke hallucinated reward fields

## Diff Snippets
```python
# defensive_numeric_converter.py - regex extraction
+import re
+if isinstance(value, str):
+    value_no_commas = value.replace(",", "")
+    match = re.search(r"[-+]?[0-9]*\.?[0-9]+", value_no_commas)
+    if not match:
+        raise ValueError(f"No numeric content found in '{value}'")
+    converted = int(float(match.group(0)))
```

## Motivation
The previous `_get_raw` helper was fragile and bypassed central type constraints. LLM units like "1,000 gp" were tricking the coercer into returning 0, causing rewards box not to render for campaign WQEl4sJb7RqWLndJK4GU.