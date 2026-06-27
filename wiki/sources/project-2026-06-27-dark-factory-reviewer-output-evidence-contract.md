---
title: "Dark Factory reviewer/output/evidence contract and deterministic install smoke"
type: source
tags: [dark-factory, attractor, evidence, reviewer, install, uv]
date: 2026-06-27
source_file: raw/project_2026-06-27_dark_factory_reviewer_output_evidence_contract.md
---

## Summary

On 2026-06-27, dark-factory was updated and merged to `origin/main` at commit `9f854a8c238dfeafbf164904e8993236a2b61aed`.

The key learning is that status strings are routing metadata only. LLM pipeline nodes must pass full free-form output and artifact references downstream, while durable logs/evidence keep each node's prompt, input, output, transcript, and hashes inspectable.

## Key Claims

- `/f`, `/fs`, and `/factory` runs are unproven unless they invoke the actual `dark-factory` binary and echo command/run proof.
- Every run should produce an evidence envelope with command echo, events JSONL, CXDB hashes, `node_io.jsonl`, pipeline copy, and transcript references.
- Reviewer dedupe must preserve independence: use `parallel_reviewer` for redundant/independent reviewer lanes, but log each lane separately and pass a combined free-form review bundle downstream.
- Shadow Codex review should default on, with an explicit opt-out parameter.
- Installer smoke should be a deterministic install check. Do not use sealed holdout graphs as default installer smoke.
- Installer dependency input should be locked. `requirements.lock` is committed and mandatory; missing lockfiles fail closed.

## Verification

- Merged-main focused pytest suite: `186 passed`.
- Independent Codex Spark reviews reported no blockers.
- `origin/main` verified at `9f854a8c238dfeafbf164904e8993236a2b61aed`.
- `./install.sh --no-link --no-cmds` passed with `uv 0.9.13` and `final_outcome: success`.
- Temp-copy negative test without `requirements.lock` failed with `RC=1` and `ERROR: requirements.lock not found.`

## Connections

- [DarkFactory](../concepts/DarkFactory.md)
- [EvidenceBundles](../concepts/EvidenceBundles.md)
- [AttractorParallelExecution](../concepts/AttractorParallelExecution.md)
- [InstallScriptIdempotency](../concepts/InstallScriptIdempotency.md)
