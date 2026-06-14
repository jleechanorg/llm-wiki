---
name: codergen-prompt-contract-must-exempt-special-shapes
description: "When writing a contract test that pins 'every codergen node has X,' the test must exempt topology-only shapes (point, component, tripleoctagon) because they never reach _codergen at runtime."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When pinning the contract "every codergen node has a non-empty prompt"
(or any other codergen-specific attribute), the test must mirror the
engine's handler dispatch — which means exempting special shapes that
never reach `_codergen`.

**The shapes the engine handles specially** (verified against `runner.engine._is_parallel_node` + `_is_join_node` + general dispatch):

| Shape | Handler | Why exempt |
|---|---|---|
| `point` (width=0, height=0) | none | Topology anchor (e.g. `_base.dot`'s `explore_in`/`explore_out`); never reached by `_codergen` |
| `component` (no explicit type) | parallel | Fan-out node; engine handles via the parallel branch |
| `tripleoctagon` (no explicit type) | join | Fan-in barrier; engine handles via the parallel branch |
| `Mdiamond` | start | Built-in; caught by name skip |
| `Msquare` | exit | Built-in; caught by name skip |

A test that flags `explore_in` / `explore_out` as "codergen nodes
missing a prompt" is wrong — those are zero-width routing anchors
that the engine never instantiates. The right exemption: skip the
test's prompt check when `node.attrs.get("shape")` is in
`{"point", "component", "tripleoctagon", "Mdiamond", "Msquare"}`.

**Why this matters:** the F6i codergen-prompt test initially flagged
`explore_in` and `explore_out` as offenders, but reading `_base.dot`
and the engine's dispatch logic showed they are routing-only anchors.
The 1-line exemption fix is `shape in {"point", "component",
"tripleoctagon"}: return False` in `_node_needs_prompt`.

**Generalization:** when pinning a contract on "every X-shaped node
has Y," the test helper should mirror the engine's actual dispatch
chain — not a simplified "no type means default codergen" rule.
Special shapes (point, component, tripleoctagon) are routed
elsewhere and are exempt from any codergen-specific contract.

**How to apply:** Before writing a contract test on a node attribute,
read the engine's handler resolution (typically
`runner.engine._is_parallel_node` / `_is_join_node` for shape
special-cases) and mirror the dispatch order in the test helper.
The cost of missing a special shape is a noisy false-positive test
that gets "fixed" by loosening the assertion, which loses the
contract.
