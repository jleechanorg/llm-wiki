---
name: Stop the Gemini dice A/B latency experiment after feasibility
description: The pilot found no obvious latency win; retain managed code execution and do not fund the 60-pair cohort.
type: project
bead: rev-sle47
---

The 2026-08-27 A/B-only feasibility pilot compared Gemini-managed code
execution (A) with the streaming typed server-tool path (B). It did not prove
either arm faster. A was mechanism-compliant 3/3; B was compliant 2/3 with one
retained no-tool ITT miss. A median/p95 latency was 102.3s/112.6s; B was
84.4s/157.4s. The apparent B median hint is outweighed by worse tail latency,
worse reliability, missing decision-grade cost data, and only three pairs.

The high latency was not simply an absent-cache artifact. Raw BQ rows show the
three A requests were heavily cached: 96.67%, 97.09%, and 99.15% of reported
prompt tokens, yet their provider calls still took 46.93s, 57.07s, and 60.98s
and end-to-end turns took 73.4s to 112.6s. The two compliant B turns each made
two sequential provider calls. Their first calls were uncached and took 31.42s
and 87.22s; their second calls were only 56.82% and 57.53% cached and took
25.49s and 23.87s. Prompts were approximately 201k to 240k tokens. Cache misses
contributed to B's latency, especially the 87.22s first phase, but large prompt
processing, long provider generation, two-phase serialization, and additional
application overhead remained material.

Decision: stop before the fixed 60-pair/120-turn cohort and retain Arm A. Do not
repeat the pilot, add C calls, claim a causal winner, or change production
routing. Reopen only if a new product reason justifies the spend or a materially
different architecture reduces prompt size or eliminates the second sequential
Gemini call. PR #9370 may preserve the diagnostic harness, but it is not rollout
evidence.

Verification: raw `provider_exchanges.jsonl` and `attempts.jsonl` from
`pilot-abonly-a35b6d34e4-20260827T193528Z`; exact-head focused contracts passed
3/3 at `9412465babc44a1a90630c3ba5c338c2c2249bde`. The historical source bundle
still contains incomplete publication prose, so the lesson is deliberately
limited to feasibility and the stop decision.
