# Source: Refactor Backend Adjustment Registry to Immutable Types and Validations

- **Date**: 2026-05-29
- **Project**: worldarchitect.ai
- **Bead**: [[rev-xetuw]]
- **PR**: [PR #7112](https://github.com/jleechanorg/worldarchitect.ai/pull/7112)
- **Jeffrey Oracle Impact**: None (pure technical workflow and architectural safety refactoring)

---

## Context

In [PR #7112](https://github.com/jleechanorg/worldarchitect.ai/pull/7112), the backend adjustment registry was refactored. The primary architectural problem was a circular import between `backend_adjustment_registry.py` and `backend_adjustment_specs.py`. The registry needed the specs to define the active list of adjustment specs, while the specs needed type definitions (such as enums and the spec dataclass) from the registry to construct the specs.

## Architectural Solutions & Key Patterns

### 1. Breaking Circular Imports via Neutral Type Modules
Instead of keeping type definitions inside the registry or spec modules, all immutable type definitions, enums (`AdjustmentProofCategory`, `AdjustmentType`), validation logic, and the frozen dataclass (`AdjustmentSpec`) were extracted into a neutral third module `backend_adjustment_types.py` that contains no other imports from the registry or spec modules.
- **Pattern**: If Module A and Module B have circular imports because A defines types B uses, and B defines configurations/specs A uses, extract the types and validators into a neutral Module C (`*_types.py` or similar). Both A and B can safely import from C.

### 2. Strict Immutable Dataclass Validation
The `AdjustmentSpec` dataclass is defined as a frozen dataclass (`@dataclass(frozen=True)`). To ensure that all specifications are validated at instantiation and cannot be mutated or bypassed, strict `__post_init__` validation is implemented:
- **Proof-required category validation**: Restricts types of proof allowed per category (e.g., `AUDIT_ONLY` specs must have `None` root-cause-status; others require a valid proof status).
- **Rejecting raw_response**: Rejects the raw LLM output `raw_response` in any dotted path segment or server-owned fields.
- **Normalizing fields safely**: Normalizes optional/none fields safely (e.g., `None` gist URL is normalized to `""` before format validation runs).
- **Validation of runtime references**: Rejects bare `runtime:` or whitespace-only values, enforcing that non-empty content exists after the prefix.

### 3. Backward-Compatible Shim Interfaces
To avoid breaking the rest of the application, `backend_adjustment_registry.py` was retained as an export shim. It imports all symbols from the new `backend_adjustment_types.py` and `backend_adjustment_specs.py` modules and re-exports them.
- **Pattern**: When migrating internal code structures, keep the original entry point as an export shim that re-exports all external API surfaces. This guarantees zero breaking changes for callers.

## Verification & Proof Invariants

20 unit tests were added under `mvp_site/tests/test_backend_adjustment_registry.py` covering:
- Rejecting invalid URL schemes.
- Safe `None` normalization.
- Rejection of nested `raw_response` paths (e.g. `raw_response.text`, `llm.raw_response.content`).
- Rejecting bare `runtime:` references.
- Spec immutability and schema compliance.
- Bead uniqueness constraints in `.beads/issues.jsonl` to prevent duplicate automation errors.

## References
- [PR #7112](https://github.com/jleechanorg/worldarchitect.ai/pull/7112)
- Bead `rev-xetuw` (Learning closed bead)
- Files touched:
  - `mvp_site/backend_adjustment_types.py` (New types & validations module)
  - `mvp_site/backend_adjustment_registry.py` (Re-export shim)
  - `mvp_site/backend_adjustment_specs.py` (Adjuster specs using new types)
  - `mvp_site/tests/test_backend_adjustment_registry.py` (Comprehensive unit tests)
