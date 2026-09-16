---
name: Advice Withheld on Partial ER Requires Operator Exception
description: When historical pre-edit failing output is missing, /er and /advice must fail closed as WITHHELD despite 4-reviewer code approval; merge requires explicit operator exception.
type: feedback
bead: rev-u5kx2.3
---

## Context
In PR #9406 (feat/telemetry-server-and-client-metrics; prod +646/-157, non-prod +3331/-39), four code reviewers (Gemini, ChatGPT, Codex, and Opus) fully approved the code and architecture, and CI was clean (30 passed, 6 skipped, 1 neutral; 0 unresolved threads). However, original pre-edit failing output for backend RED had been lost during execution recovery.

## Invariant & Rule
1. **No Retrospective Relabeling of ER**: Retrospective execution of RED tests reproduces expected behavior but cannot establish original pre-edit chronology. The Evidence Review (/er and /es) must strictly remain `PARTIAL` rather than being relabeled `PASS`.
2. **Advice Quorum Fail-Closed**: In `/advice`, satisfying the 4-reviewer code-approval quorum does NOT override missing or partial evidence. The final verdict must fail closed as `WITHHELD` (e.g., `VERDICT: WITHHELD at <SHA> — mandatory ER prerequisite is PARTIAL; code-review quorum is satisfied`).
3. **Explicit Operator Merge Exception**: Merging under a PARTIAL evidence state is strictly forbidden by default; it is authorized ONLY when the operator issues an explicit `MERGE APPROVED` accompanied by the documented `PARTIAL-evidence` exception.

## Verification
- Head: `f14e9fd6491ed2d34ead53780547ee14c752820c`.
- Merged: `0e8e1a5b15ce890250df75a0d3d526e0be0d8692`.
- Gist receipt: https://gist.github.com/jleechan2015/54af46d977f456fb90f3754837b9eafb
- Local audit state: `/Users/jleechan/.claude/state/pr9406-paused-2026-09-13/approval-advice-synthesis.md` and `merge-approved-result.md`.
