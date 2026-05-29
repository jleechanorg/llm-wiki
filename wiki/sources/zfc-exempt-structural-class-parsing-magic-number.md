# ZFC-Exempt Structural Class Parsing + Magic Number Extraction

**Date:** 2026-05-28  
**Type:** feedback / best practice  
**Bead:** rev-h9hrm (closed)  
**Branch:** feat-lu-paladin-spell-button-fix-2  
**PR:** [#7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142)

## Summary

During `/fake3` audit on PR #7142, two findings were resolved:

1. **`_match_spellcasting_class()` confirmed ZFC-exempt** — substring matching against `_SPELLCASTING_CLASSES` frozenset is deterministic structural parsing of a schema field, not semantic intent routing.
2. **Magic number `0.7` extracted** — two inline `temperature=0.7` usages in `_generate_spells_via_llm` replaced with `_SPELL_REPAIR_TEMPERATURE = 0.7` module-level constant.

## ZFC-Exempt Pattern

```python
def _match_spellcasting_class(class_lower: str) -> str | None:
    for t in [p.strip() for p in re.split(r"[/,]", class_lower) if p.strip()]:
        for sc in _SPELLCASTING_CLASS_PRIORITY:
            if sc == t or sc in t:
                return sc
    return next((sc for sc in _SPELLCASTING_CLASS_PRIORITY if sc in class_lower), None)
```

**Exempt because:**
- Input is a structured data field (`class_name`), not free-form user text
- Frozenset (`_SPELLCASTING_CLASSES`) is a canonical enum of D&D class names
- Output drives schema field selection, not LLM routing or model behavior

## Magic Number Fix

```python
# Before (two occurrences in _generate_spells_via_llm):
"temperature": 0.7,

# After (module-level constant near frozensets):
_SPELL_REPAIR_TEMPERATURE = 0.7
...
"temperature": _SPELL_REPAIR_TEMPERATURE,
```

Commit: `d6a686db91ef615e5fc532dd505aa9aee96e66a1`

## Relation to [[ZFCNorthStar]]

This learning adds precision to the ZFC exemption boundary: frozenset membership checks on structured schema fields are NOT ZFC violations, even when the frozenset contains class names that appear in other ZFC-violating contexts.
