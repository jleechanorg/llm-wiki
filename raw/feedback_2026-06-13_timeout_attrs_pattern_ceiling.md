---
name: timeout-attrs-contract-pattern-ceiling
description: "The F5/F6 contract-test pattern (extract + assert on existing artifacts + add to canonical allow-list) reached a stable plateau at 4 pipeline families (factory, slim, airbnb-clone, amazon-clone). A 5th is mechanical but adds limited value."
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-7rd
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

The F5/F6 contract-test pattern (PRs #61, #62, #63, #64, #65) extracts a small testable contract, asserts on existing artifacts, and adds the result to a canonical allow-list. It has scaled to 4 pipeline families in dark-factory:
- factory/ (`pipelines/factory/{gates,pr_gates}.dot`) — PR #62
- slim/ (`pipelines/slim/{minimal_feature_cs,levelup_pra_validate}.dot`) — PR #63
- airbnb-clone/ (`benchmarks/airbnb-clone/pipelines/{master,sprint-1/2/3}.dot`) — PR #64
- amazon-clone/ (`benchmarks/amazon-clone/pipelines/{dark_factory,kilroy,mammoth,slim,smasher,tracker}.dot`) — PR #65

A 5th family is now <15 min of mechanical work (copy test, scope allow-list, scan for codergen nodes, add timeouts) but the marginal value drops. The 4th family in a single session is the natural ceiling for this pattern.

**Why:** Diminishing returns on the 5th family unless a new WIP-clean pipeline family surfaces. Better next moves:
1. **Refactor the 4 timeout-attr test files into 1 parameterized helper** (`tests/test_pipeline_timeouts.py` with per-family fixture) — ~80% code reduction, single source of truth, new file is file-disjoint from all 4 existing tests.
2. **Start checking values across the canonical allow-list** (timeout=300? timeout=1800? what's the next-narrower rule?).
3. **WIP triage** (`jleechan-xsg` P1) — still the highest-leverage unblocking action.

**How to apply:** When a contract-test pattern has scaled to N pipeline families, ask "is the 5th mechanical and limited, or does it surface new structure?" If mechanical+limited, pivot to refactoring (parameterize) or value-pinning. If structural, continue. The pattern isn't exhausted; it has reached a stable plateau.

**Test design lessons from F6e:**
- Scoped allow-list is a contract review tool: `_CODERGEN_600_EXPECTED` enumerates exactly which nodes MUST be 600s vs exempt, with inline comments like `"""slim""" : {"implement"},  # ``fix`` is 300 (intentional)`. The test reads as the contract spec.
- Mixed-form tolerance: pydot returns `timeout=600` (int) and `timeout="600"` (string) unchanged. `_normalise_timeout(value) → int(value)` makes the test agnostic to form.
- TDD caught real gaps mid-flight: smasher's `test`/`holdout` tool nodes had no `timeout`; the failing test made the gap visible before the PR was created.
