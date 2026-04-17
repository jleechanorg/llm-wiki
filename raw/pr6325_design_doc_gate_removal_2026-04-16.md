# PR #6325 — ci: remove design_doc_gate from CI pipeline

**Author**: jleechan2015
**Merged**: 2026-04-16
**Labels**: antig, CI
**Files changed**: 2

## Summary
Removes the `design_doc_gate` job from `.github/workflows/green-gate.yml` and fixes a workflow dependency bug in `doc-size-check.yml` where `retry-self-hosted` was incorrectly `needs: try-self-hosted` instead of `needs: doc-size-check`.

## Changes

### `.github/workflows/doc-size-check.yml`
- Fix: `retry-self-hosted` now correctly `needs: doc-size-check` (was incorrectly `needs: try-self-hosted`)

### `.github/workflows/green-gate.yml`
- Remove entire `design_doc_gate` job (158 lines removed)
- Update workflow description from "design_doc_gate (blocking) → skeptic_gate → post trigger comment" to "pre-check 6-green eligibility → post trigger comment"
- The `skeptic_gate` job no longer has a `needs:` dependency on `design_doc_gate`

## Rationale
- CI workflow files should be clean and declarative
- Bespoke architectural tests via bash logic clutter the CI definitions
- The design_doc_gate was a blocking step meant to enforce design doc compliance via grep patterns before skeptic evaluation

## Connections
- Related to [[SkepticGate]] — skeptic_gate is now the primary gate
- Related to [[GreenGateWorkflow]] — green-gate workflow simplified
- [[DesignDocGate]] concept — the removed gate
