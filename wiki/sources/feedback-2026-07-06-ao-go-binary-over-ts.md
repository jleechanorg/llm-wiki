---
title: "Prefer AO Go binary over TS-AO for factory dispatch + status"
type: source
tags: [agent-orchestrator, ao-go, factory-af, dark-factory, dockering]
date: 2026-07-06
source_file: feedback_2026-07-06_ao_go_binary_over_ts.md
---

## Summary

User explicitly prefers `/Users/jleechan/bin/ao-go` (the Mach-O Go-AO binary from `/Users/jleechan/projects/tracker`) over the TS-ao wrapper `/Users/jleechan/bin/ao`. The Go-AO server binds 127.0.0.1:3001 but DOES NOT serve GET / (returns JSON `ROUTE_NOT_FOUND`). Recovery path is `ao session ls` CLI + tmux attach + reading tracker repo code directly; do NOT expect a web dashboard.

## Key Claims

- TS-AO (`/Users/jleechan/bin/ao`, Node.js) and Go-AO (`/Users/jleechan/bin/ao-go`, Mach-O from `/Users/jleechan/projects/tracker/cmd/tracker`) are SEPARATE daemons; not interchangeable.
- The Go-AO HTTP server (port 3001) has no `/` handler — calling `curl http://localhost:3001/` returns `{"error":"not_found",...}` with the ironclad JSON envelope.
- For multi-vendor consensus reference, the canonical pattern is `/Users/jleechan/projects/tracker/examples/subgraphs/final-review-consensus.dip` — Opus+GPT+Gemini parallel + conservative-merge + iron-law "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE".
- The TS-AO known dashboard console bug (websocket `noServer: true`) is documented in [[feedback_2026-05-30_ao_darkfactory_worker_bringup]] and fixed in agent-orchestrator PR #648.
- `/Users/jleechan/projects/tracker/pipeline/handlers/parallel.go` defines `ParallelHandler` with `Name() = "parallel"` + concurrent goroutines per branch target — directly applicable to dark-factory `daemon/src/verifier.rs::assess`.

## Key Quotes

> "I want to use the golang binary — stop forgetting" — user, 2026-07-06

> "Use `ao session ls` + tmux attach instead of expecting a web dashboard." — derived recovery path

> "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE" — iron law from tracker `final-review-consensus.dip`

## Connections

- [[feedback_2026-05-30_ao_darkfactory_worker_bringup]] — prior AO worker bringup notes (TS-AO dashboard bug PR #648)
- [[reference_2026-06-21_official_dynamic_workflows_vs_dotfactory]] — context on why dotfactory stays static (.dot)
- [[project_2026-07-06_af_spec_gap_audit]] — 8 spec-gap beads, multi-vendor verifier = jleechan-x1bq
- [[project_2026-07-06_four_prs_green_session_total]] — 4 of 6 PRs /green via factory-af this session
- [[AgentOrchestrator]] — concept page for AO itself (needs creation)
- [[ParallelReviewerConsensus]] — concept page for the consensus pattern (needs creation)
