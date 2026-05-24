---
title: "Attractor Pattern"
type: concept
tags: [attractor-pattern, architecture, spec-driven, convergence]
date: 2026-05-24
---
## Overview
The Attractor pattern is a design philosophy for agentic coding where natural language specifications (NLSpecs) describe a system so naturally that independent implementations converge on the same architecture. Named after dynamical systems — an attractor is a state a system tends to evolve toward.

## Key Properties
- **What**: Spec-driven development where the specification is the primary artifact and code is disposable (dorodango)
- **Why matters**: Four independent implementations (Kilroy, Mammoth, Smasher, Tracker) converged on the same three-layer architecture without coordination — proving the spec is an "attractor" in design space
- **Three-layer convergence**: (1) Unified LLM Client, (2) Agent Loop with tool dispatch, (3) DOT-based Pipeline Engine — every implementation lands here

## Related Systems
| System | Language | Key Distinction |
|--------|----------|----------------|
| [[Kilroy]] | Go | Local-first CLI, CXDB checkpoints, worktree isolation |
| [[Mammoth]] | Go | 21-rule DOT linter, fan-in, verification nodes, 5-phase lifecycle |
| [[Smasher]] | Rust | Lean, HTMX dashboard, SSE streaming, smasher chat REPL |
| [[Tracker]] | Go | Dippin language, .dipx bundles, interview-mode human gates |
| [[DarkFactory]] | Python | The dark-factory repo's own runner with CXDB + Healer |

## Connection to Attractor Pattern
This IS the core concept. The Attractor pattern asserts that well-written NLSpecs act as attractors in design space, pulling independent implementations toward a common architecture. The spec is the product; the code is dorodango.

## Key Principles
1. **Specs are public, evaluators are sealed** — specs in the repo, conformance tests generated locally
2. **DOT files are the durable artifact** — version them, review them in PRs, share them
3. **Agent isolation** — implementing agents must not see holdouts/evaluator code
4. **CXDB + Healer feedback loop** — observe every step, cluster failures, auto-diagnose and auto-fix
5. **Dorodango** — polish generated code; when fundamentally wrong, discard and rebuild from spec

## See Also
- [[NLSpec]]
- [[Dorodango]]
- [[DOTAsArtifact]]
- [[CXDB]]
- [[HealerAgent]]
- [[DarkFactory]]
- [[FiveLevelAutomation]]
