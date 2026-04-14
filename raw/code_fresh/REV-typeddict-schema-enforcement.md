# REV: TypedDict for Compile-Time Schema Enforcement

**Status:** COMPLETED
**Priority:** HIGH (Developer Experience / Type Safety)
**Component:** mvp_site/schemas, type checking
**Created:** 2026-02-15
**Completed:** 2026-02-17
**Effort:** 12-16 hours
**Depends On:** PR #4534 (JSON Schema as source of truth)
**Related:** REV-schema-driven-field-access, REV-protobuf-vs-json-analysis

## Problem

**Current state lacks compile-time type safety:**
```python
# Runtime - typos cause bugs
gold = player_character_data.get("resorces", {}).get("gold")
# Returns: None (silently fails - bug discovered when user complains)

# No IDE autocomplete
player_character_data.get("???")  # No suggestions

# Refactoring requires manual grep
# Renaming "gold" → "currency" needs careful find/replace
```

**Impact:**
- ❌ Typos discovered at runtime (or never if `.get()` returns None)
- ❌ No IDE autocomplete for field names
- ❌ Refactoring is error-prone (manual verification needed)
- ❌ ~366 hardcoded field accesses in game_state.py alone
- ❌ Tests needed to catch schema violations

## Solution: TypedDict (Generated from JSON Schema)

**Add compile-time type checking via TypedDict:**
```python
# mvp_site/schemas/typed_dicts.py (auto-generated from game_state.schema.json)
from typing import TypedDict, NotRequired

class ResourcesDict(TypedDict, total=False):
    """Player resources (gold, hit dice, etc.)."""
    gold: int
    hit_dice: dict[str, int]
    spell_slots: dict[str, int]
    class_features: dict[str, Any]
    consumables: list[dict[str, Any]]

class PlayerCharacterData(TypedDict, total=False):
    """Player character state."""
    entity_id: str
    display_name: str
    level: int
    resources: ResourcesDict
    equipment: EquipmentDict
    stats: StatsDict
    # ... all fields from JSON schema

class GameStateDict(TypedDict, total=False):
    """Complete game state."""
    campaign_id: str
    user_id: str
    game_state_version: int
    session_id: str
    turn_number: int
    player_character_data: NotRequired[PlayerCharacterData]
    world_data: NotRequired[dict[str, Any]]
    combat_state: NotRequired[CombatStateDict]
    # ... all top-level fields
```

**Usage with type checking:**
```python
# mypy catches typos at development time
def canonicalize_gold(pc_data: PlayerCharacterData) -> None:
    resources: ResourcesDict = pc_data.get("resources", {})
    gold = resources.get("gld")  # ❌ mypy error: "gld" not in ResourcesDict
    #                     ^^^
    # Expected one of: gold, hit_dice, spell_slots, class_features, consumables

# IDE autocomplete
resources.get("...")  # ← IDE shows: gold, hit_dice, spell_slots, etc.
```

## Benefits

### 1. Compile-Time Error Detection
```python
# Before (runtime bug)
gold = player_character_data.get("resorces", {}).get("gold")  # Typo!
# Test runs, gold is None, bug discovered in production

# After (caught by mypy)
pc_data: PlayerCharacterData = player_character_data
resources: ResourcesDict = pc_data.get("resorces", {})  # ❌ mypy error!
# Error caught before code runs
```

### 2. IDE Autocomplete
- IntelliSense shows valid field names
- Reduces typos during development
- Faster coding (less looking up schema)

### 3. Refactor-Safe
```python
# Rename "gold" → "currency" in JSON schema
# TypedDict auto-regenerates (git diff shows changes)
# mypy catches all code using old "gold" field
# Compiler-assisted refactoring instead of grep
```

### 4. 80% of Protobuf Benefit, 20% of Effort
- Protobuf: 40-60 hours migration, binary format, conversion overhead
- TypedDict: 12-16 hours migration, keep JSON, no conversion

## Implementation Plan

### Phase 1: Code Generation Script (4 hours)

**Create:** `scripts/generate_typeddict.py`

```python
"""Generate TypedDict definitions from game_state.schema.json."""
import json
from pathlib import Path
from typing import Any

def json_type_to_python(json_type: str | list) -> str:
    """Convert JSON schema type to Python type hint."""
    if isinstance(json_type, list):
        # Union types (e.g., ["string", "null"] → str | None)
        types = [json_type_to_python(t) for t in json_type]
        return " | ".join(types)

    type_map = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "list[Any]",  # Refined later based on items
        "object": "dict[str, Any]",
        "null": "None",
    }
    return type_map.get(json_type, "Any")

def generate_typeddict_from_schema(schema: dict[str, Any]) -> str:
    """Generate TypedDict classes from JSON schema."""
    output = []
    output.append("# AUTO-GENERATED from game_state.schema.json")
    output.append("# DO NOT EDIT MANUALLY - regenerate with scripts/generate_typeddict.py")
    output.append("")
    output.append("from typing import Any, TypedDict, NotRequired")
    output.append("")

    # Generate from $defs first (dependency order)
    defs = schema.get("$defs", {})
    for def_name, def_schema in defs.items():
        output.append(generate_class_from_def(def_name, def_schema))

    # Generate top-level GameStateDict
    output.append(generate_class_from_def("GameState", schema))

    return "\n".join(output)

def generate_class_from_def(name: str, schema: dict) -> str:
    """Generate a single TypedDict class."""
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    lines = [f"class {name}Dict(TypedDict, total=False):"]
    if desc := schema.get("description"):
        lines.append(f'    """{desc}"""')

    for field_name, field_schema in properties.items():
        field_type = json_type_to_python(field_schema.get("type", "Any"))

        # Handle $ref to other TypedDicts
        if "$ref" in field_schema:
            ref = field_schema["$ref"].split("/")[-1]
            field_type = f"{ref}Dict"

        # Use NotRequired for optional fields
        if field_name not in required:
            field_type = f"NotRequired[{field_type}]"

        if field_desc := field_schema.get("description"):
            lines.append(f'    {field_name}: {field_type}  # {field_desc}')
        else:
            lines.append(f'    {field_name}: {field_type}')

    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    schema_path = Path(__file__).parent.parent / "mvp_site/schemas/game_state.schema.json"
    output_path = Path(__file__).parent.parent / "mvp_site/schemas/typed_dicts.py"

    schema = json.loads(schema_path.read_text())
    typeddict_code = generate_typeddict_from_schema(schema)
    output_path.write_text(typeddict_code)

    print(f"✅ Generated TypedDict definitions: {output_path}")
```

### Phase 2: Integration with Existing Code (4 hours)

**Update:** `mvp_site/schemas/__init__.py`
```python
# Export TypedDict types
from .typed_dicts import (
    GameStateDict,
    PlayerCharacterData,
    ResourcesDict,
    EquipmentDict,
    CombatStateDict,
    # ... all generated types
)

__all__ = [
    # ... existing exports
    "GameStateDict",
    "PlayerCharacterData",
    "ResourcesDict",
    # ... all TypedDict exports
]
```

**Update:** `mvp_site/game_state.py` (gradual adoption)
```python
from mvp_site.schemas import PlayerCharacterData, ResourcesDict

def _canonicalize_player_gold_in_place(
    player_character_data: PlayerCharacterData,  # ← Type hint added
    *,
    corrections_out: list[str] | None = None,
) -> None:
    """Normalize legacy/misplaced gold into canonical location."""
    resources: ResourcesDict = player_character_data.get("resources", {})
    #           ^^^^^^^^^^^^^
    # mypy now validates all field accesses!

    canonical_gold = resources.get("gold")  # ✅ Type-checked
```

### Phase 3: Enable mypy in CI (2 hours)

**Create:** `.mypy.ini`
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False  # Start permissive, increase strictness later
ignore_missing_imports = True

[mypy-mvp_site.schemas.*]
disallow_untyped_defs = True  # Strict for schema module

[mypy-mvp_site.game_state]
disallow_untyped_defs = True  # Strict for game_state (high-risk)
```

**Update:** `.github/workflows/presubmit.yml`
```yaml
- name: Type check with mypy
  run: |
    pip install mypy types-jsonschema
    mypy mvp_site/schemas/ mvp_site/game_state.py --config-file .mypy.ini
```

### Phase 4: Gradual Migration (2-4 hours)

**Priority order:**
1. `mvp_site/game_state.py` - 366 field accesses (highest impact)
2. `mvp_site/schemas/validation.py` - Schema utilities
3. `mvp_site/firestore_service.py` - Database layer
4. `mvp_site/world_logic.py` - State processing

**Migration pattern:**
```python
# Before (untyped)
def process_state(state_dict: dict) -> dict:
    gold = state_dict.get("player_character_data", {}).get("resources", {}).get("gold")
    return state_dict

# After (typed)
def process_state(state_dict: GameStateDict) -> GameStateDict:
    pc_data: PlayerCharacterData = state_dict.get("player_character_data", {})
    resources: ResourcesDict = pc_data.get("resources", {})
    gold = resources.get("gold")  # All type-checked!
    return state_dict
```

### Phase 5: Auto-Regeneration Hook (2 hours)

**Create:** `scripts/pre-commit-typeddict.sh`
```bash
#!/bin/bash
# Regenerate TypedDict if schema changed
if git diff --cached --name-only | grep -q "game_state.schema.json"; then
    echo "🔄 Schema changed, regenerating TypedDict..."
    python scripts/generate_typeddict.py
    git add mvp_site/schemas/typed_dicts.py
    echo "✅ TypedDict regenerated"
fi
```

**Install hook:**
```bash
ln -s ../../scripts/pre-commit-typeddict.sh .git/hooks/pre-commit
```

## Acceptance Criteria

**Phase 1-3 (Minimum Viable):**
- [x] `scripts/generate_typeddict.py` generates valid TypedDict from JSON schema
- [x] `mvp_site/schemas/typed_dicts.py` created with all major types
- [x] mypy enabled in CI (presubmit.yml)
- [x] At least one module migrated (`game_state.py` recommended)
- [x] CI passes with mypy checks

**Phase 4-5 (Full Adoption):**
- [ ] All high-risk modules typed (game_state, validation, firestore_service, world_logic)
- [ ] Pre-commit hook auto-regenerates TypedDict on schema changes
- [ ] Documentation in `.claude/skills/typed-dict-usage.md`
- [ ] Team training on TypedDict best practices

## Testing Strategy

### 1. Test TypedDict Generation
```python
# scripts/tests/test_generate_typeddict.py
def test_typeddict_matches_schema():
    """Verify generated TypedDict matches JSON schema structure."""
    schema = load_schema("game_state")
    typeddict_code = generate_typeddict_from_schema(schema)

    # Parse generated code and verify structure
    assert "class GameStateDict(TypedDict" in typeddict_code
    assert "player_character_data: NotRequired[PlayerCharacterData]" in typeddict_code
```

### 2. Test mypy Catches Typos
```python
# mvp_site/tests/test_typeddict_enforcement.py
def test_mypy_catches_field_typos():
    """Verify mypy catches typos in typed code."""
    # This test doesn't run - it's checked by CI mypy
    # If this file has typos, CI will fail

    pc_data: PlayerCharacterData = {"display_name": "Test"}
    resources: ResourcesDict = pc_data.get("resorces", {})  # ❌ Should fail mypy
    # Expected: error: TypedDict "PlayerCharacterData" has no key "resorces"
```

## Trade-offs

### Pros
- ✅ Compile-time error detection (typos caught before runtime)
- ✅ IDE autocomplete (IntelliSense)
- ✅ Refactor-safe (compiler-assisted)
- ✅ Keep JSON (human-readable, tooling)
- ✅ Low migration cost (12-16 hours vs 40-60 for Protobuf)
- ✅ 80% of Protobuf benefit, 20% of effort

### Cons
- ⚠️ Runtime still uses strings (TypedDict doesn't enforce at runtime)
- ⚠️ TypedDict can diverge from schema (need codegen + hooks)
- ⚠️ Gradual adoption means mixed typed/untyped code during migration
- ⚠️ mypy adds CI build time (~30-60 seconds)

## Alternative Considered: Protobuf

**See:** `.beads/REV-protobuf-vs-json-analysis.md`

**Decision:** TypedDict first, Protobuf if insufficient

**Evaluation criteria (3-6 months):**
- Schema violations <1%/turn → TypedDict sufficient
- Schema violations >5%/turn → Revisit Protobuf

## Related Beads

- **REV-schema-driven-field-access** - Generate field constants from schema
- **REV-protobuf-vs-json-analysis** - Protobuf vs JSON trade-offs
- **PR #4534** - JSON Schema as source of truth (prerequisite)

## Success Metrics

**Short-term (1 month):**
- Zero mypy errors in CI
- At least 200/366 field accesses in game_state.py typed
- Typos caught by mypy (before runtime)

**Long-term (3-6 months):**
- All high-risk modules typed
- Schema violation rate measured
- Developer satisfaction survey (is TypedDict helpful?)

## Rollout Plan

**Week 1:** Phase 1-3 (Infrastructure)
- Generate TypedDict
- Enable mypy in CI
- Migrate game_state.py (core module)

**Week 2-3:** Phase 4 (Gradual Migration)
- Migrate validation.py, firestore_service.py, world_logic.py
- Fix mypy errors found during migration

**Week 4:** Phase 5 (Automation)
- Pre-commit hook
- Documentation
- Team training

**Month 2+:** Monitoring
- Track schema violations in production
- Decide: TypedDict sufficient or need Protobuf?

## Notes

**Why TypedDict over Pydantic BaseModel?**
- TypedDict is lightweight (no runtime overhead)
- Works with existing dict-based code (gradual migration)
- Pydantic already used for to_model/from_model (different use case)
- TypedDict for type checking, Pydantic for serialization

**Compatibility with existing code:**
- TypedDict is structural typing (duck typing)
- Existing `dict` code still works (gradual adoption)
- No breaking changes (add types incrementally)
