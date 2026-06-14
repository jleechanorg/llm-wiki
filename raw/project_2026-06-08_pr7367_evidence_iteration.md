---
name: pr7367-evidence-iteration
description: "PR #7367 desktop auth-init indicator — Skeptic rounds 19-21 progress, hosted video evidence, design doc N/A"
metadata:
  type: project
---

# PR #7367 — Desktop auth-init indicator evidence iteration

**Date:** 2026-06-08
**PR:** [#7367](https://github.com/jleechanorg/worldarchitect.ai/pull/7367) — `fix(auth): render minimal authenticating indicator on desktop 8s timeout`
**Branch:** `fix/desktop-auth-init-indicator`
**Final head:** `dffc7df8160bbb9442bc2e0fe5d56adcba4c114f`

## Skeptic round-by-round progression

**Round 19 (head 3de8dd99b, 23:27 UTC):**
- FAIL on gates 1, 3, 4, 5, 6, 7, 8, 8c
- Critical bug: indicator used `color:rgba(255,255,255,0.7)` (light text on transparent background) — INVISIBLE on light-theme body
- Fix: added inline `background-color:rgba(0,0,0,0.55)` + `color:#ffffff` + `role="status"` + `aria-live="polite"`

**Round 20 (head 177c8374f, 23:48 UTC):**
- PASS on gates 1-5, 7
- FAIL on gate 6/8c: evidence videos were local `/tmp/...` paths, not hosted HTTPS URLs
- Fix: committed 3 mp4 videos + checksums + bundle files to `docs/evidence/pr-7367/`, referenced as `https://github.com/jleechanorg/worldarchitect.ai/blob/<sha>/docs/evidence/pr-7367/*.mp4`

**Round 21 (head dffc7df816, 00:08 UTC):**
- PASS on gates 2-7 (Gate 6 evidence now accepted)
- FAIL on gate 1: CI was in flight at time of verdict
- FAIL on gate 8: design doc N/A justification missing from PR body
- Fix: added `## Design decision & tracking` section with explicit `Design doc: N/A — small auth-init UX improvement on the 8s watchdog fallback path; not a design-doc-driven change.`

## Why the round 22 verdict was slow

The Skeptic Cron worker uses a `FAIL_SUPPRESS_WINDOW_SECS` to avoid re-triggering after a recent FAIL verdict. After round 21 (00:08 UTC), subsequent cron runs suppress new triggers for PR 7367 until the suppress window expires. The next Green Gate re-runs (00:58-00:59 UTC) are still timing out without finding a fresh verdict.

This is consistent with the prior memory entry: "Skeptic worker down fleet-wide; PR #7262 6/7 parked on Gate 7" — the worker is not the issue, but the suppress window + head-changes + cron schedule create a long effective latency between iterations.

## Key lessons

1. **Code-trace + tests ≠ sufficient evidence for UI changes.** Skeptic Gate 8c requires real browser video tied to the changed behavior, not just static screenshots or mock-driven test runs. The mp4 videos satisfy this for the desktop test page. The live preview video shows that the app's redirect path takes over before the 8s watchdog can act in production — that's honest data, not a gap.

2. **Color contrast is a real bug class, not a nitpick.** `rgba(255,255,255,...)` text on a transparent background is a theme-dependent invisibility bug. Skeptic round 19 caught it because the gate explicitly checks the diff's claim ("so the user knows something is happening") against the actual rendered visibility. Inline `background-color:rgba(0,0,0,0.55)` + `color:#ffffff` is the right fix because it bypasses the theme system.

3. **Hosted evidence is required.** Skeptic Gate 6 / 8c requires HTTPS media URLs tied to the head SHA. Local paths or gist-hosted base64 PNGs are insufficient. The pattern that works: commit `.mp4` files to `docs/evidence/pr-<PR-NUMBER>/` on the branch and reference them as `https://github.com/jleechanorg/worldarchitect.ai/blob/<sha>/docs/evidence/pr-<N>/<file>` in the PR body.

4. **Design doc N/A must be explicit in PR body.** Skeptic Gate 8 checks for an explicit `Design doc: N/A` with one-line justification, or a full GitHub blob URL to `roadmap/*.md` / `docs/design/**/*.md` on `main`. Omitting the section causes Gate 8 to fail.

5. **The Skeptic FAIL-suppress window is real.** `FAIL_SUPPRESS_WINDOW_SECS` in the cron workflow prevents re-triggering for a window after a recent FAIL verdict. To iterate fast on the same head after a fix, you may need to push a new commit (new head SHA) so the cron finds a missing verdict for the new SHA.

6. **Close-and-reopen to retrigger Green Gate** is the supported pattern — it does not lose history, and it gives the Skeptic a fresh verdict on the new head SHA. Use `gh pr close <PR> --comment "..." && sleep 2 && gh pr reopen <PR>`.

## Bundles

- Local: `/tmp/worldarchitect.ai/fix/desktop-auth-init-indicator/auth-init-indicator-test/latest/`
- Public: hosted at `https://github.com/jleechanorg/worldarchitect.ai/blob/dffc7df8160bbb9442bc2e0fe5d56adcba4c114f/docs/evidence/pr-7367/`
- Bundle files: `evidence.md`, `metadata.json`, `run.json`, `test_output.txt`, `full_diff.patch`, `desktop_test_real.mp4`, `mobile_test_real.mp4`, `desktop_preview_real.mp4` + `.sha256` checksums
