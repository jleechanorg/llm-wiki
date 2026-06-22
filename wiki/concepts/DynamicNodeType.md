---
title: "Dynamic Node Type"
type: concept
tags: [dark-factory, dot-engine, dynamic-workflows, level5, type-attribute]
date: 2026-06-22
sources:
  - /Users/jleechan/llm_wiki/raw/project_2026-06-22_g3_closure_dynamic_node_design.md
last_updated: 2026-06-22
---

# Dynamic Node Type (`type="dynamic"`)

## Overview

A new DOT node type for the Dark Factory `.dot` engine that lets Claude (with high effort) re-plan substeps inside a single session, closing the G3 (runtime-determined fan-out) gap. Designed as a structural counterpart to `type="codergen"` — fixed-shape nodes that the runner dispatches verbatim.

## Key Properties

- **New attribute on DOT nodes**: `type="dynamic"` declares a node as runtime-shaped. Requires `default="<static_node_name>"` for the non-Claude fallback.
- **Driver-based dispatch**: when the driver is Claude Code (in-session, has the native Workflow tool), the runner shells `claude -p --effort high` with an auto-wrapped prompt. When the driver is any other CLI (`codex` / `ao` / `agy`), the runner resolves the `default` static node and runs it as a normal `codergen`.
- **Both paths use `--effort high`** (option a: full parity). The only thing that changes between drivers is who runs the model, not how hard it thinks.
- **Auto-wrap template** (injected by `_wrap_dynamic_prompt` above the authored prompt body):

> You are a dynamic node in a Level-5 dark-factory pipeline. You may re-plan substeps, expand or compress work as you see fit. The runner will record your output to CXDB; downstream nodes consume `ctx.state`.

- **No multi-agent fan-out**: high effort does not give Claude the ability to spawn subagents. "Dynamic" is a prompt-authoring distinction (model has more latitude inside one session), not an orchestrator-level one. For true multi-agent dynamic workflows, use native Claude Dynamic Workflows (Workflow tool / ultracode) — which the Dark Factory itself does not use.
- **CXDB + perf log apply identically**: dynamic nodes are recorded to the event log the same way as any other node, with the same `(run_id, seq, node, outcome, ts, output_hash, output_head, metadata)` shape.

## Why high effort and not ultracode

- Ultracode = the native Workflow tool / multi-agent subagent orchestration. The Dark Factory's n=10 Sonnet benchmark showed ultracode gives no separation on any axis for first-pass coding tasks and is ~5–9% slower. So `type="dynamic"` uses `claude -p --effort high` (single-session high reasoning) instead, which gives most of the "Claude decides" benefit without the orchestrator overhead.
- This keeps the runner as the single orchestrator. CXDB, Healer, perf-log, and conformance-validate invariants all stay unified — they don't get split between the runner and a subagent-orchestrating tool.

## Conformance contract

Every `type="dynamic"` node MUST have a `default="<static_node>"` reference. The static fallback node MUST exist in the same graph. Conformance check: `bin/conformance validate` rejects the `.dot` if the default is missing, points to a non-existent node, or points to itself.

## Connections

- [[DOTAsArtifact]] — the `.dot` is the durable spec; `type="dynamic"` adds a new node kind to that artifact.
- [[CXDB]] — dynamic nodes record to CXDB identically to static nodes.
- [[HealerAgent]] — failure clustering works on dynamic node output the same way.
- [[ConformanceLevel5Rule]] — the rule set that enforces the hard + soft tier around dynamic nodes.
- [[Level5AutonomyReview]] — the operational goal this design serves.
- [[DynamicWorkflowsNativeVsDotEngine]] — the gap analysis that identified the G3 problem.
- [[WorkflowGraphgenBenchmark]] — the n=10 benchmark that justified picking high-effort over ultracode.

## When to use

- **Use `type="dynamic"` when:** the implementation step benefits from Claude re-planning substeps at runtime (e.g., explore / plan / implement / fix loops where the structure of the work depends on what was discovered).
- **Use `type="codergen"` when:** the work shape is known at author time and re-planning would just be overhead (e.g., a single-shot review node, an evidence-bundle compile, a final report).
- **Use the native Workflow tool / ultracode directly when:** you need genuine multi-agent fan-out (K-spread ≥ 1 dynamic endpoints, V/C > 1) — the Dark Factory does not do this itself, but you can call it from a Claude Code session.
