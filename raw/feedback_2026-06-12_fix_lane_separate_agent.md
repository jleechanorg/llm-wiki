---
name: fix-lane-as-separate-agent-pattern
description: When an initial lane's PR comes back from review with actionable findings, spawn a SEPARATE fix-lane subagent (not extend the original lane). The fix lane is read-only on what was already shipped, then pushes targeted commits. Don't mix "build" and "fix-review-response" mentalities in one agent.
metadata:
  node_type: memory
  type: feedback
  bead: jleechan-8py, jleechan-wou
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When a 2-lane parallel fanout lands a PR pair and BOTH come back from review with actionable findings, **spawn a fresh fix-lane subagent** — not a continuation of the original lane agents. One subagent can handle both branches (read-only on what shipped, then push targeted fix commits per PR).

**Why:** Original Lane A (panic hook) and Lane B (structural preflight) both came back with real findings on the SAME day — CRITICAL argparse ambiguity, MAJOR test pollution to `~/.dark-factory/panics/`, MEDIUM `exec` bypassing trap architecture, MEDIUM `chmod +x` missing. The original agents were tuned for "build green from spec," not "respond to 5-comment review thread with surgical fixes." A fresh agent reads the diff + the review, writes a fix list, and pushes 1-2 commits per PR. Cleaner than extending the original.

**Bugbot stale-comment trap:** `CHANGES_REQUESTED` from a pre-fix review does NOT auto-dismiss when the fix commits land — Bugbot doesn't re-thread its comments against the new head automatically. Per the `jleechan-xpv` pattern, treat `CHANGES_REQUESTED` from pre-fix reviews as stale when (a) actionable items = 0, (b) CI green, (c) CodeRabbit skipped/approved. Admin-merge is fine.

**Argparse `--bash-argv` lesson:** any boolean-style flag followed by a positional argv is greedy and steals tokens. Pattern: pass complex payloads as JSON-encoded strings (single argument, no ambiguity). The fix lane applied this to all bash-trap arg forwarding in `bin/dark-factory` + `bin/df-healer`.

**`exec python` defeats bash traps:** `exec` replaces the shell, so the EXIT trap never fires on Python's non-zero exit. Either remove `exec` (bash stays alive, trap fires) OR use a subshell wrapper. The fix lane chose remove-exec. Trade-off: one extra bash process per invocation.

**Test pollution to `~/.dark-factory/panics/`** is the failure mode the v9 perf-log lesson warned about. Make the panic dir an explicit `--panic-dir` flag and the test pass a tmp_path; never let a test write to the real `~/.dark-factory/` tree.

**Related:** [[feedback_2026-06-12_cli_preflight_wip_avoidance]] (file-disjoint lanes pattern that produced the PRs this fix lane cleaned up), [[feedback_2026-05-31_pr10_coderabbit_stall]] (jleechan-xpv admin-merge pattern), [[project_2026-06-12_thermo_simplify_cross_validation]] (file-overlap pre-check).
