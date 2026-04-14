---
title: "Mem2Evolve Test: PR #6254 XP Progress Tracking"
type: autoresearch
date: 2026-04-14
pr_number: 6254
experiment: mem2evolve
---

## 1. Experience Accumulated from This PR

### Problem Diagnosis Experience
- **Primary symptom**: Rewards box not rendering for campaigns with XP progress but no `xp_gained`
- **Secondary cascade**: Missing rewards → scrubbed planning choices → missing level-up UI
- **Root cause**: `has_visible_content` check only considered `xp_gained`, ignoring `current_xp`/`next_level_xp`

### Atomicity Cascade Pattern
The PR revealed a new cascade pattern:
```
suppressed rewards box (backend)
  → scrubbed planning choices (atomicity enforcement)
    → missing level-up UI (user-facing bug)
```
This demonstrates that backend visibility checks have frontend rendering consequences.

### LLM String Coercion Pattern
Discovered that LLM outputs like "850 XP", "1,000 gp" can trick numeric coercers into returning 0, not 0.0 or the string itself.

---

## 2. Dynamically Created Tools/Helpers from This Experience

### Tool: Dual-Field Visibility Checker
```python
def has_visible_content(xp_gained, current_xp, next_level_xp, gold, loot, level_up_available, progress_percent):
    """Check visibility using both earned and progress fields."""
    return (
        (xp_gained and xp_gained > 0)
        or (current_xp > 0 and next_level_xp > 0)  # Progress field check
        or (gold and gold > 0)
        or bool(loot)
        or level_up_available
        or (progress_percent and progress_percent > 0)
    )
```

### Tool: Atomicity Cascade Detector
```python
def detect_atomicity_cascade(suppressed_field, downstream_fields):
    """Detect when field suppression cascades to downstream effects."""
    if not suppressed_field:
        return [f"Potential cascade to {d}" for d in downstream_fields]
    return []
```

---

## 3. Key Patterns Discovered

### Pattern 1: Invisible Content Problem
When a field has semantic meaning (XP progress) but numeric value is falsy (0), the field becomes invisible to visibility checks. **Fix**: Always check paired fields together.

### Pattern 2: LLM String Coercion
LLMs output strings with units ("850 XP"), which numeric coercers may interpret as 0. **Fix**: Regex extract numeric content before type conversion.

### Pattern 3: Atomicity Cascade
Backend field suppression cascades to frontend rendering. If field A is required for field B to render, hiding A hides B. **Fix**: Consider downstream effects in visibility logic.

---

## 4. How This Informs Future Fixes

### For Similar Visibility Bugs
- Check ALL semantically meaningful fields, not just primary indicators
- Always verify paired fields (current_X + next_X) together
- Test with both zero and non-zero values for each field type

### For Numeric Extraction
- Never trust direct string-to-number coercion
- Use regex to extract numeric content before conversion
- Handle commas, units, and fractional notations

### For Atomicity Issues
- Map downstream dependencies before implementing field suppression
- Consider frontend rendering implications of backend logic
