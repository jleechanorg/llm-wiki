---
title: "PR #6325 — Remove design_doc_gate from CI Pipeline"
type: source
tags: [CI, green-gate, workflow, design-doc]
date: 2026-04-16
source_file: ../raw/pr6325_design_doc_gate_removal_2026-04-16.md
---

## Summary
PR #6325 removes the `design_doc_gate` job from `.github/workflows/green-gate.yml` (158 lines removed) and fixes a workflow dependency bug in `doc-size-check.yml`. The rationale: CI workflow files should be clean and declarative, and bespoke architectural tests via bash logic clutter CI definitions.

## Key Changes

### `.github/workflows/doc-size-check.yml`
- `retry-self-hosted` now correctly `needs: doc-size-check` (was incorrectly `needs: try-self-hosted` — a bug fix)

### `.github/workflows/green-gate.yml`
- Removed entire `design_doc_gate` job (158 lines)
- Workflow description updated: "design_doc_gate (blocking) → skeptic_gate" → "pre-check 6-green eligibility → post trigger comment"
- `skeptic_gate` no longer has a `needs:` dependency on `design_doc_gate`

## Design Decision
The `design_doc_gate` was originally added by PR #6291 to enforce design doc compliance via grep patterns before skeptic evaluation. PR #6325 removed it as "clutter" — the skeptic gate is now the primary gate without a design doc pre-check requirement.

## Connections
- [[GreenGateWorkflow]] — workflow simplified by removing design_doc_gate
- [[SkepticGate]] — skeptic_gate is now the primary gate without preconditions
- [[DesignDocGate]] — the removed gate concept
- [[PR6291]] — the PR that added design_doc_gate (subsequently removed)
- [[AWKCompatibility]] — the POSIX regex fix in PR #6309 was made to green-gate.yml which still existed at that time
