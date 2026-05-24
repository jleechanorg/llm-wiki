---
title: "Agent Isolation"
type: concept
tags: [attractor-pattern, security, adversarial, eval-contamination]
date: 2026-05-24
---
## Overview
Agent isolation is the Attractor pattern's core security constraint: the implementing agent (codergen worker) must not see the holdout tests, evaluator code, or any _holdout/ test sources. This preserves the adversarial guarantee — the agent can't pass tests by reading them.

## Key Properties
- **What**: Operational + mechanical isolation preventing implementing agents from accessing evaluation artifacts
- **Why matters**: Without isolation, agents can game conformance tests by reading them (identical to AttractorBench's "don't ship the conformance tests" rule)
- **Enforcement**: (1) Operational — prompt construction never references holdout paths; (2) Mechanical — `sandbox-exec` denies file-read on holdout paths; `_sanitized_env` strips `DARK_FACTORY_HOLDOUTS` and `*HOLDOUT*` env vars
- **Role matrix**: Implementing agent sees specs+prompts+dot graph+its worktree; Evaluator sees holdouts+specs+diff; Operator (you) sees everything but must not paste holdout content to implementing agent prompts

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[AttractorBench]] | Benchmark | Conformance tests generated locally, excluded from repo |
| [[DarkFactory]] | Repo | Implements agent isolation via sandbox-exec and env stripping |
| [[AdversarialEvaluation]] | Concept | Agent isolation is a form of adversarial evaluation |

## Connection to Attractor Pattern
Agent isolation is the Attractor pattern's adversarial guarantee. The whole point of separating specs from evaluators is that the implementing agent proves its work against unknown tests — just like a student taking an exam doesn't get to see the answer key.

## See Also
- [[AttractorBench]]
- [[AdversarialEvaluation]]
- [[DarkFactory]]
