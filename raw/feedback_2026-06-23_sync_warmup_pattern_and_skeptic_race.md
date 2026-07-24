---
name: feedback-sync-warmup-pattern-and-skeptic-race
description: Sync warmup blocking pattern for FastEmbed; Skeptic-vs-smoke dispatch race; statusCheckRollup pre-existing failures
metadata:
  type: feedback
  bead: none
---

## Pattern 1: Synchronous blocking warmup eliminates cold-start (Best Practice)

`warm_synchronously()` in `create_app()` blocks the gunicorn worker until the model is fully loaded before the worker serves traffic. This gives a guaranteed zero cold-start first request, at the cost of ~5.5s extra worker startup time.

**PR #7817 evidence**: BEFORE = background warmup triggered by first request (~2s cold-start risk); AFTER = 5.528s sync warmup at boot, first request at 0.326s.

**Why**: FastEmbed ONNX model load is ~5s. A background thread that loses the race to the first request causes silent 2s classify() latency. Gunicorn's `timeout=600s` easily absorbs 5.5s startup overhead.

**How to apply**: When adding a new ML model or heavyweight classifier to a gunicorn-served app, put `model.warm_synchronously()` in `create_app()` rather than relying on lazy/background init. Use `threading.Event` (not lock-held polling) for the readiness signal.

---

## Pattern 2: Dispatch Skeptic AFTER Real E2E comment lands, not before (Mandatory)

Skeptic gate-8 reads the PR comment containing the Real E2E pass. If you dispatch Skeptic before the smoke run posts its comment, Skeptic evaluates gate-8 before the proof exists → gives WAIT or FAIL.

**Session incident**: Dispatched Skeptic (28011194207) before smoke run 28011079421 completed. Race was resolved because the Real E2E comment landed at 08:00:59Z and Skeptic STARTED at ~08:02Z. If Skeptic had started before the comment, it would have given gate-8 WAIT.

**How to apply**: When dispatching Skeptic manually, first confirm the Real E2E comment exists via `gh pr view <N> --json comments --jq '[.comments[] | select(.body | contains("Real E2E") and contains("SHA_FRAGMENT"))] | length'`. Only dispatch after count > 0.

---

## Pattern 3: statusCheckRollup accumulates all runs; pre-existing failures aren't PR regressions (Best Practice)

`gh pr view --json statusCheckRollup` returns ALL check runs ever attached to the PR, including pre-existing failures from main. A FAILURE for a test not in the PR diff (e.g., `test_bug_char_creation_transitions.py` in this session) is NOT a regression introduced by the PR.

**How to apply**: When gate-1 shows FAILURE, first check if the failing test file is in `gh pr diff --name-only`. If not in the diff, the Skeptic will correctly classify gate-1 as PASS. Do not block merge over pre-existing unrelated failures.

---

## Pattern 4: `jq | last` on empty filtered array returns null object, not error (Anti-Pattern)

`jq '[.[] | select(...)] | last'` on an empty match returns `{"body":null,"time":null}` — tests as truthy in bash `if [ "..." ]`. This caused a false-positive "VERDICT found" alarm in this session.

**How to apply**: Always guard with `select(.body != null)` or pipe through `select(. != null)` before using `last`. Or use `length` check first: `if length == 0 then empty else last end`.
