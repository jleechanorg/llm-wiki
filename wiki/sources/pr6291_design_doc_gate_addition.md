---
title: "PR #6291 — Add design_doc_gate as Blocking Step Before Skeptic Gate"
type: source
tags: [CI, green-gate, skeptic, design-doc, workflow]
date: 2026-04-15
source_file: ../raw/pr6291_design_doc_gate_2026-04-15.md
---

## Summary
PR #6291 adds a `design_doc_gate` job to `.github/workflows/green-gate.yml` (158 lines) that runs design doc grep gates inline. The `skeptic_gate` job gains `needs: [design_doc_gate]` so the skeptic trigger only fires after design doc compliance passes.

**Note**: This PR was subsequently reverted/removed by [[PR6325]], which removed the `design_doc_gate` entirely as clutter to CI definitions.

## Gate Behavior
- Only runs on non-fork PRs (`github.event.pull_request.head.repo.fork == false`)
- Checks if PR touches production code files (`mvp_site/world_logic.py`, `constants.py`, `llm_parser.py`, `llm_service.py`)
- Skips gate entirely if PR does not touch production code
- If PR fails design doc compliance → `skeptic_gate` never runs

## Design Doc Compliance Gates
The grep gates check for design doc patterns in changed files:
- Must have corresponding documentation for architectural changes
- Prevents skeptic evaluation on undocumented changes

## Changes
- `.github/workflows/green-gate.yml` — added 158-line `design_doc_gate` job
- `skeptic_gate` gained `needs: [design_doc_gate]`

## Connections
- [[GreenGateWorkflow]] — new blocking gate added to workflow
- [[SkepticGate]] — now gated behind design_doc_gate
- [[DesignDocGate]] — the gate concept
- [[PR6325]] — which superseded/removes this PR
- [[AWKCompatibility]] — grep portability fix in PR #6309 was made while this gate existed
