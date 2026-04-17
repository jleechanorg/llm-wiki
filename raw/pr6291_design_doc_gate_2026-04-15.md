# PR #6291 — feat(ci): add design_doc_gate as blocking step before skeptic gate

**Author**: jleechan2015
**Merged**: 2026-04-15
**Labels**: CI, feat
**Files changed**: 1

## Summary
Adds a `design_doc_gate` job to `.github/workflows/green-gate.yml` that runs design doc grep gates inline. The `skeptic_gate` job now has `needs: [design_doc_gate]` so skeptic trigger only fires after design doc compliance passes.

## Changes

### `.github/workflows/green-gate.yml`
- Added new `design_doc_gate` job (158 lines)
- `skeptic_gate` now depends on `design_doc_gate` via `needs: [design_doc_gate]`
- Gate runs grep patterns on PR diffs to check for design doc compliance
- Only runs on non-fork PRs

## Design Doc Compliance Gates
The gate checks:
1. Changed production files (`mvp_site/world_logic.py`, `constants.py`, `llm_parser.py`, `llm_service.py`)
2. Design doc grep patterns to ensure architectural decisions are documented

## Note
This PR was subsequently reverted/removed by PR #6325, which removed the design_doc_gate entirely as clutter to CI definitions.

## Connections
- Related to [[GreenGateWorkflow]] — new blocking gate added
- [[SkepticGate]] — now depends on design_doc_gate
- [[DesignDocGate]] — the gate concept
- Superseded by [[PR6325]] — which removed this gate
