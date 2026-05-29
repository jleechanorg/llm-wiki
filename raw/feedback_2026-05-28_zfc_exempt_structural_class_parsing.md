---
name: zfc-exempt-structural-class-parsing
description: _match_spellcasting_class() frozenset membership checks are ZFC-exempt; magic numbers in LLM call kwargs need named constants
metadata: 
  node_type: memory
  type: feedback
  bead: rev-h9hrm
  originSessionId: bdd86084-a7db-479c-b6e1-ca1eff524d3e
---

## Rule

**`_match_spellcasting_class()` substring matching against `_SPELLCASTING_CLASSES` frozenset is ZFC-EXEMPT.** It is deterministic structural parsing of a schema field (character class string like "Wizard/Cleric") against a canonical set of known values. This is not semantic intent routing — the output drives schema field validation, not LLM behavior selection.

**Why:** ZFC bans keyword routing that guesses *user intent* from free text. Parsing a structured schema field ("class_name") against a known enum set is deterministic schema validation, equivalent to `isinstance()` checks. No judgment call is involved.

**How to apply:** When auditing `_match_spellcasting_class()` or similar functions that check `if matched_class in _SOME_FROZENSET`, confirm:
1. Input is a structured data field (not free-form user text)
2. The frozenset is a canonical enum of known values (not ad-hoc keywords)
3. Output drives schema branching, not LLM routing

If all three hold → ZFC-exempt, mark ✅.

---

## Magic Number Extraction Pattern

**Any float/int used as a direct LLM call kwarg (temperature, top_p, max_tokens overrides) must be a named module-level constant.**

**Violation found (2026-05-28 fake3 audit, PR #7142):** `temperature=0.7` used inline twice in `_generate_spells_via_llm` (world_logic.py lines 6029, 6047 before fix).

**Fix:** Extract to `_SPELL_REPAIR_TEMPERATURE = 0.7` near frozenset declarations at module level. Commit: `d6a686db91` on branch `feat-lu-paladin-spell-button-fix-2`.

**Pattern:**
```python
# ❌ Before
"temperature": 0.7,
temperature=0.7,

# ✅ After
_SPELL_REPAIR_TEMPERATURE = 0.7  # module-level, near frozensets
...
"temperature": _SPELL_REPAIR_TEMPERATURE,
temperature=_SPELL_REPAIR_TEMPERATURE,
```

---

## sys.path.insert() at Module Level — Acceptable

`sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))` at the TOP of a testing_mcp test file is NOT the banned inline-import pattern. The ban is `def test(): from foo import bar` (import inside function body). Module-level path setup is standard pytest pattern and acceptable.

---

## References

- Branch: `feat-lu-paladin-spell-button-fix-2`
- Fix commit: `d6a686db91ef615e5fc532dd505aa9aee96e66a1`
- PR: [#7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142)
- Files: `mvp_site/world_logic.py` lines 5886-5892, 6028, 6046
- Bead: rev-h9hrm (closed)
