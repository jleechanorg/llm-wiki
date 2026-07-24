# SuperCommand

`/super <task>` — the slash entry point that runs the full superpowers pipeline (brainstorm + write plan + execute) end-to-end and dispatches the produced plan to [[SuperpowersCloudBuild]].

## Critical fix (2026-07-20)
Earlier `/super` versions had a **bug**: on jeff-ubuntu (unenrolled at the time), `/super` fell through to local `subagent-driven-development` OR used `claudeg`/OpenRouter — both wrong. `/super` must ALWAYS dispatch to the real Cloud Build box (internal proxy, NOT OpenRouter). Fixed by:
1. Enrolling jeff-ubuntu as a [[CloudBuildBastionHost]] (copied Mac's keypair + state + scripts).
2. Removing the local-subagent + claudeg fallback branches from the command on BOTH machines.

## Versions
- v1 (2026-07-20 13:10) — thin `claudeg` router (transitional shim) — WRONG
- v2 (2026-07-20 14:00) — real Cloud Build dispatch but stopped at every clarifying Q
- v3 (2026-07-20, current) — full pipeline auto-pick, ONE summary table, ONE user gate, then dispatch to the box from either machine

## Companion
- `/superlight <task>` — legacy local-GLM-5.2 router via `claudeg` (OpenRouter). One-liners only; NOT the box; affected by OpenRouter 402 credit exhaustion.
