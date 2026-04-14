# REV: Schema-Driven Field Access (Replace Hardcoded Strings)

**Status:** COMPLETED
**Priority:** MEDIUM (Code Quality / Maintainability)
**Component:** mvp_site/schemas, mvp_site/game_state.py
**Created:** 2026-02-15
**Completed:** 2026-02-17
**Effort:** 6-9 hours (Hybrid) | 18-24 hours (Full)

## Problem

Field names are hardcoded as strings throughout the codebase:
- **366 hardcoded field accesses** in `game_state.py` alone (228 `.get("field")` + 138 `["field"]`)
- **~2000+ estimated** project-wide
- **Risk**: Typos not caught until runtime, refactoring requires manual find/replace
- **Inconsistency**: Some fields already extracted from schema (`get_canonical_equipment_slots()`), most are not

```python
# Current (hardcoded strings - risky)
resources = player_character_data.get("resources")
gold = resources.get("gold")
equipment = player_character_data.get("equipment")
backpack = equipment.get("backpack")

# Desired (schema-driven - safe)
from mvp_site.schemas.field_constants import FIELD_PC_RESOURCES, FIELD_RESOURCE_GOLD
resources = player_character_data.get(FIELD_PC_RESOURCES)
gold = resources.get(FIELD_RESOURCE_GOLD)
```

## Impact

**Current Pain Points:**
- Typos cause runtime failures: `resources.get("gld")` silently returns `None`
- Refactoring is manual: Renaming `gold` → `currency` requires grep + manual review
- No IDE autocomplete for field names
- Schema changes don't propagate to code automatically
- Hard to track all uses of a field (string search finds false positives)

**Future Benefits:**
- ✅ Refactor-safe: Rename in schema → constant updates everywhere
- ✅ Type-safe: Constants are `Final` (immutable)
- ✅ IDE autocomplete: `FIELD_` prefix triggers IntelliSense
- ✅ Grep-friendly: Easy to find all uses of a field
- ✅ No divergence: Generated from schema at import time

## Root Cause

Historical evolution:
1. Started with hardcoded strings (fast initial development)
2. Added JSON schema later (PR #4534)
3. Some fields extracted from schema (`get_canonical_equipment_slots()`)
4. Most fields still hardcoded (technical debt)

## Recommended Solution: Hybrid Approach (Pragmatic)

**Phase 1: Add Common Field Path Constants** (6-9 hours)

```python
# mvp_site/schemas/validation.py (extend existing pattern)
_COMMON_FIELD_PATHS_CACHE: dict[str, str] | None = None

def get_common_field_paths() -> dict[str, str]:
    """Return commonly-used field paths extracted from schema.

    Focuses on high-traffic nested paths (80/20 rule).
    """
    global _COMMON_FIELD_PATHS_CACHE
    if _COMMON_FIELD_PATHS_CACHE is not None:
        return dict(_COMMON_FIELD_PATHS_CACHE)

    # Extract from schema (similar to get_canonical_equipment_slots)
    schema = load_schema("game_state")
    defs = schema.get("$defs", {})

    paths = {
        # PlayerCharacter nested paths
        "pc.resources": "resources",
        "pc.equipment": "equipment",
        "pc.stats": "stats",
        "resource.gold": "gold",
        "resource.hit_dice": "hit_dice",
        "equipment.backpack": "backpack",
        # ... top 20 most-used paths
    }

    _COMMON_FIELD_PATHS_CACHE = dict(paths)
    return dict(paths)
```

**Refactor hot paths in game_state.py:**
- Gold canonicalization functions (2 functions, ~150 lines)
- Combat state normalization
- Player character data access
- Equipment/inventory handling

**Phase 2: Expand Coverage** (Future, as needed)
- Add more paths based on usage patterns
- Monitor adoption and refine API
- Optional: Full constant generation for 100% coverage

## Alternative Solutions Considered

### Option 1: Full Schema-Generated Constants (18-24 hours)
```python
# Auto-generated at import time
FIELD_PLAYER_CHARACTER_DATA: Final = "player_character_data"
FIELD_PC_RESOURCES: Final = "resources"
FIELD_RESOURCE_GOLD: Final = "gold"
```

**Pros:** Complete coverage, zero divergence
**Cons:** High effort (366+ changes in one file), verbose code

### Option 2: TypedDict with Literal Types (24+ hours)
```python
class ResourcesDict(TypedDict, total=False):
    gold: int
    hit_dice: dict[str, int]
```

**Pros:** Type checker catches typos, IDE autocomplete
**Cons:** Very high effort, doesn't eliminate hardcoded strings

### Option 3: Runtime Codegen (18-20 hours)
```python
# Generated dynamically at import
FIELDS = _generate_field_constants()
# Usage: FIELDS.FIELD_GOLD
```

**Pros:** Zero maintenance, auto-syncs
**Cons:** Import-time overhead, debugging complexity

## Acceptance Criteria

**Phase 1 (Hybrid):**
- [x] Add `get_common_field_paths()` to `validation.py`
- [x] Generate top 20 field paths from schema (cached) - 59 paths generated
- [ ] Refactor gold canonicalization to use constants (future work)
- [ ] Refactor combat state access to use constants (future work)
- [x] Update tests to verify constant correctness
- [ ] Documentation in CLAUDE.md or `.claude/skills/` (future work)

**Phase 2 (Optional Full Coverage):**
- [ ] Generate all field constants from schema
- [ ] AST-based automated refactoring tool
- [ ] Migrate all 366+ hardcoded accesses in game_state.py
- [ ] CI check to prevent new hardcoded field strings

## Related

- PR #4534: Schema Validation Warnings (adds JSON schema)
- `.claude/skills/code-centralization.md`: Search existing code before writing new
- ADR-0003: Unified Game State Schema (establishes schema as source of truth)

## Evidence: Existing Patterns Work

Already schema-driven (successful):
- `get_canonical_equipment_slots()` - extracts from schema at runtime
- `get_social_hp_request_severity_values()` - extracts enum values
- `get_game_state_top_level_properties()` - extracts top-level keys

**This proves:**
- Schema extraction is fast (cached)
- Import-time generation is safe (already used)
- Code is maintainable (one source of truth)

## Effort Breakdown

**Hybrid Approach (Recommended):**
- Design API: 1-2 hours
- Implement `get_common_field_paths()`: 2-3 hours
- Refactor game_state.py hot paths: 3-4 hours
- Testing: 1-2 hours
- **Total: 6-9 hours**

**Full Coverage (Optional):**
- Constant generation: 4-6 hours
- AST refactoring tool: 4-6 hours
- Migration: 8-12 hours
- Testing: 2-4 hours
- **Total: 18-24 hours**

## Notes

- **Do NOT implement in PR #4534** - already large (350 files)
- Separate cleanup PR recommended
- Start with Hybrid, expand to Full if team wants 100% coverage
