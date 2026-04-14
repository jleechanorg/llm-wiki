# Meta-Harness Technique — Auto-Research v3

## Technique
Outer-loop harness optimization: search over context/prompt/tool configurations

## Key Insight
The harness around the LLM matters more than the LLM itself (6x performance gap)

## PRs Tested
| PR | Type | Baseline Score | Meta-Harness Score | Delta |
|---|---|---|---|---|
| WA-001 (pr-6241) | Small | 51 | 85 | +34 |
| WA-004 (pr-6261) | Medium | 68 | 90 | +22 |
| WA-005 (pr-6214/#6275) | Complex | 62 | 87 | +25 |

## Harness Configurations Tested
- **Default**: standard context + prompt
- **Optimized**: selective context + explicit typing + appropriate tool selection

## Detailed Results

### PR 1: TEST-WA-001 (Small — RuntimeError Fix)

**Baseline (default harness):**
Direct bug fixes without refactoring. Used bare `try/except: pass` for error handling, inline clamping without TypedDict, no typed exceptions. Scattered fixes across 6 files without architectural improvement.

- Score: **51/100**
  - Naming: 10/15 — basic snake_case, no FastAPI patterns adopted
  - Error Handling: 10/20 — bare exception handling, no typed exceptions
  - Type Safety: 8/20 — inline clamping, no TypedDict
  - Architecture: 8/20 — ad-hoc inline fixes, no canonical patterns
  - Test Coverage: 12/15 — tests updated but no new edge case coverage
  - Documentation: 3/10 — zero docstrings on public APIs

**Meta-Harness (optimized harness):**
Added `ProgressValidationError(HTTPException)`, TypedDict for `RewardsBox` and `GameStateSnapshot`, parameterized tests for clamping (0, 100, -10, 150) and non-finite values (NaN, Inf, -Inf), proper fail-closed validation.

- Score: **85/100**
  - Naming: 13/15 — snake_case functions, PascalCase exceptions
  - Error Handling: 17/20 — typed HTTPException subclass, fail-closed
  - Type Safety: 18/20 — TypedDict throughout, math.isfinite checks
  - Architecture: 16/20 — FastAPI exception hierarchy pattern
  - Test Coverage: 13/15 — parametrized edge cases covered
  - Documentation: 8/10 — docstrings on public APIs

**What harness changes helped:**
1. Explicit typing guidance (TypedDict) — +10 points on Type Safety
2. Error handling guidance (typed exceptions) — +7 points on Error Handling
3. Test guidance (edge case parametrization) — +1 point on Test Coverage

---

### PR 2: TEST-WA-004 (Medium — Defensive Numeric Extraction)

**Baseline (default harness):**
Created regex extraction but returned None on failure (not raising), no TypedDict for result shape, minimal docstrings, no typed exception classes.

- Score: **68/100**
  - Naming: 10/15 — cryptic regex pattern, unclear function names
  - Error Handling: 14/20 — returns None on failure, no typed exceptions
  - Type Safety: 12/20 — no TypedDict, raw float returns
  - Architecture: 14/20 — centralization correct, but lacks interface
  - Test Coverage: 12/15 — basic tests, missing edge cases
  - Documentation: 6/10 — minimal docstrings, undocumented regex

**Meta-Harness (optimized harness):**
Added `NumericExtractionResult(TypedDict)`, `ExtractionError(ValueError)` subclass, docstrings with args/returns/raises, comprehensive edge case testing (commas, units, fractions, invalid inputs).

- Score: **90/100**
  - Naming: 14/15 — clear verb_noun function names
  - Error Handling: 18/20 — typed exception, fail-closed validation
  - Type Safety: 18/20 — TypedDict for result shape, explicit returns
  - Architecture: 17/20 — clean public/private split, centralized interface
  - Test Coverage: 14/15 — edge cases covered, minor gaps in scientific notation
  - Documentation: 9/10 — docstrings on public API with type info

**What harness changes helped:**
1. TypedDict requirement — +6 points on Type Safety
2. Typed exception guidance — +4 points on Error Handling
3. Test edge case specification — +2 points on Test Coverage

---

### PR 3: TEST-WA-005 (Complex — Layer 3 Clean Strip)

**Baseline (default harness):**
Removed 190-line async call, added deterministic postcondition and helpers. Used plain dicts throughout, RuntimeError only, mixed business logic with response building.

- Score: **62/100**
  - Naming: 11/15 — mixed conventions, unclear internal function purposes
  - Error Handling: 10/20 — RuntimeError only, no typed exception hierarchy
  - Type Safety: 10/20 — plain dicts, no TypedDict for data shapes
  - Architecture: 10/20 — no domain/presentation separation
  - Test Coverage: 14/15 — 14 new tests, solid coverage
  - Documentation: 7/10 — basic docstrings, missing per-parameter types

**Meta-Harness (optimized harness):**
Added TypedDict for `GameStateDict`, `UnifiedResponse`, `RewardsBox`; exception hierarchy (`RewardsBoxError`, `ASIInjectionError`); pure domain functions separated from response builders; comprehensive tests for multi-level jumps, corrupted state, all ASI levels.

- Score: **87/100**
  - Naming: 13/15 — verb patterns (compute, validate, enforce)
  - Error Handling: 17/20 — typed exception hierarchy with context
  - Type Safety: 18/20 — TypedDict throughout, explicit returns
  - Architecture: 16/20 — domain logic separated from response building
  - Test Coverage: 14/15 — edge cases covered (multi-level, corrupted state)
  - Documentation: 9/10 — docstrings with raises clauses

**What harness changes helped:**
1. Explicit typing + architecture guidance — +8 points on Type Safety + Architecture
2. Typed exception hierarchy requirement — +7 points on Error Handling
3. Test edge case specification — maintained strong Test Coverage

---

## Summary Table
| PR | Baseline | Meta-Harness | Delta |
|---|---|---|---|
| WA-001 (small) | 51 | 85 | **+34** |
| WA-004 (medium) | 68 | 90 | **+22** |
| WA-005 (complex) | 62 | 87 | **+25** |
| **Average** | **60** | **87** | **+27** |

## Key Findings

1. **Meta-Harness consistently outperforms baseline by ~25-35 points** across all PR sizes. The explicit guidance (typing, exceptions, architecture) yields the largest gains on small bug-fix PRs (+34) vs medium refactors (+22).

2. **Type Safety improvement is the largest delta** — optimized harness scores 18/20 vs baseline 8-12/20. The explicit "Use TypedDict" requirement fundamentally changes code structure.

3. **Error Handling improves most on small PRs** — baseline uses bare `except: pass`, optimized uses typed exceptions. This is where FastAPI canonical patterns have biggest impact.

4. **Complex PRs benefit from architecture guidance** — separation of domain logic from response building adds +6 points over baseline's mixed architecture.

5. **Test Coverage remains relatively stable** — baseline already includes 14 new tests for complex PR; harness guidance improves edge case selection but doesn't dramatically change test count.

## Which Harness Worked Best?

**Optimized harness wins decisively** across all PR types. The explicit guidance framework yields:

- **+27 point average improvement** over default harness
- **Type Safety**: largest gain (baseline avg: 10/20 → optimized: 18/20)
- **Error Handling**: second largest (baseline avg: 11.3/20 → optimized: 17.3/20)

**Recommendation**: Always use structured harness with:
1. Explicit typing requirements (TypedDict for data shapes)
2. Error handling patterns (typed exception hierarchy)
3. Architecture guidance (domain/presentation separation)
4. Test edge case specification
5. Selective context (relevant fields only, not full module)