---
title: "Evidence Gate Dual-Signal Contract"
type: concept
tags: [ci-gate, evidence, pr-merge, fail-closed, signal-a, signal-b]
date: 2026-08-17
last_updated: 2026-08-17
sources:
  - /Users/jleechan/llm_wiki/raw/feedback_2026-08-17_factory_gh_token_and_poll_cadence.md
---

## Definition
The dark-factory `Evidence Gate` (workflow `.github/workflows/evidence-gate.yml`) is a CI gate on PRs that touch `runner/`, `daemon/`, or `.github/workflows/evidence-gate.yml`. It is **fail-closed by default** but accepts EITHER of two independent signals before it green-lights a merge:

### Signal A — `/er` verdict comment
A comment posted on the PR by a **trusted identity** carrying `/er PASS|FAIL|PARTIAL|INCONCLUSIVE` AND a head SHA reference (`head=<sha>` or `head <sha>`) matching the PR's current head SHA. Trusted identities:
- Comment body contains `[dark-factory /er]` (the er_runner bot marker), OR
- Comment author's GitHub login matches `^(dark-factory|er-runner|antig)` (the daemon allowlist).

A bare `/er PASS` from the PR author or any unlisted login does NOT green the gate. This prevents the PR author from forging a passing signal.

### Signal B — Canonical evidence marker in PR body
A line of the form `**Evidence**: <gist-url> head <sha>` in the PR body, where:
- `<gist-url>` is `https://gist.github.com/<user>/<id>` — a real, reachable, non-empty public gist.
- `<sha>` matches the PR's current head SHA (prefix-tolerant, ≥7 hex chars).
- The gist content is ≥ 256 bytes total (no 1-byte placeholders).
- The gist mentions the PR number OR the repo short name (PR anchor).
- The gist contains at least one substantive keyword: `/er PASS|FAIL|...`, `**Evidence**:`, or `PR #NUM`.

A bare gist URL without a real bundle fails.

## Why dual-signal
The dual-signal design (issue #433 hardening) binds the gate to **independent ground truth**, not to the PR author's self-assertion:
- Signal A requires a trusted identity the PR author can't claim (the bot marker or the allowlist).
- Signal B requires a real, externally-hosted bundle the PR author can't forge without leaving a public trace.

A PR with NEITHER signal fails closed (issue #424 explicit regression: "a PR with no /er verdict must show Evidence Gate FAILURE").

## Failure modes
- **No `/er` AND no gist** → FAIL (no verdict signal found).
- **`/er PASS` from PR author** → FAIL (not a trusted identity).
- **`/er PASS` for an old head SHA** → FAIL (head binding mismatch).
- **Gist < 256 bytes** → FAIL (no substantive content).
- **Gist doesn't mention PR number or repo name** → FAIL (no PR anchor).

## Workaround when you can't post `/er`
If you (the operator or implementer) can't post `/er` as a trusted bot identity — e.g. when you're operating as Claude Code without er_runner access — wire Signal B:
1. `gh gist create <evidence_bundle.md> --public --desc "..."` → get a gist URL.
2. Ensure gist body is ≥ 256 bytes, mentions PR number, contains substantive keyword.
3. Update the PR body with `**Evidence**: <gist-url> head <current_head_sha>`.
4. Push a no-op commit (or amend) to retrigger CI. The pull_request trigger re-evaluates on push.

This is exactly what happened in [[PR #651]]: Claude Code couldn't post `/er PASS` (no bot identity), so the operator-authorized merge used Signal B.

## Related
- [[Dark Factory]] — the runner whose CI runs this gate.
- [[Slow-CI Operator Directive 2026-08-16]] — pairs with this: when CI is queued, local proof + Signal B is sufficient to declare `/green`.
- [[PR #651]] — squash-merged with Signal B wired.
- `~/.claude/CLAUDE.md` — source-of-truth policy for "Merge approval".
- `.github/workflows/evidence-gate.yml` lines 83-127 — exact Signal A logic.
- `.github/workflows/evidence-gate.yml` lines 255-360 — exact Signal B logic.