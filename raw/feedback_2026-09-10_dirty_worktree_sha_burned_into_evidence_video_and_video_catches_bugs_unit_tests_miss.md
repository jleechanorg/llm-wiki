---
name: dirty-worktree-sha-burned-into-evidence-video
description: Evidence-capture scripts computing git rev-parse HEAD burn in a stale/wrong SHA if the tree is dirty at capture time; real browser video also catches bugs unit tests miss entirely
metadata: 
  node_type: memory
  type: feedback
  bead: rev-zcosna
  originSessionId: a1bf86e1-1dc0-4af1-8ef7-978121f5e63f
  modified: 2026-09-10T17:58:38.412Z
---

**Rule 1 (Mandatory): a `testing_ui/capture_*.py` script that burns `git rev-parse HEAD` into a video/screenshot caption must only be run against a clean, committed tree — never mid-edit.**

**Why:** on PR #9831, `testing_ui/capture_class_resources_fix_evidence_pr9831.py` computed `GIT_SHA` at import time via `git rev-parse HEAD`. The first real capture ran while the actual fix (`mvp_site/frontend_v1/app.js`'s `class_features` container-expansion logic) was staged on disk but not yet committed. The video's burned-in caption showed the PRIOR commit SHA — one that literally did not contain the fix the video claimed to demonstrate. An independent `/er` adversarial evidence review caught this by running `git diff <burned-in-sha> <fix-sha> -- mvp_site/frontend_v1/app.js` and finding the fix absent at the burned-in SHA — a real FAIL verdict, not a nitpick, per evidence-standards' explicit "pre/post SHA mismatch → FAIL" anti-pattern.

**How to apply:** before trusting or committing any evidence video/screenshot that burns in a git SHA, run `git status --porcelain` at capture time and refuse (or explicitly label) any capture taken against a dirty tree. Re-run the capture script fresh after every commit that changes the demonstrated behavior — never assume a mid-session capture from before the last commit is still representative. If evidence artifacts must be re-committed across multiple docs-only follow-up commits (e.g. to fix the SHA, then to fix a checksum), each subsequent burned-in SHA is expected to drift forward (per evidence-standards' staleness-tolerance rule) — verify by confirming the *content* at the burned-in SHA matches the fix, not by chasing an exact final SHA match.

**Rule 2 (Best Practice): real captioned browser-video evidence catches production bugs that isolated unit tests structurally cannot.**

Also on PR #9831: the Python-side fix (`mvp_site/main.py`'s `spells_summary` text formatter) was fully covered by passing unit tests. But building the *video* evidence required actually clicking the real "Spells" button in a real browser against a real server response — and that surfaced a SECOND, completely independent bug: `mvp_site/frontend_v1/app.js:1513-1543` re-renders the exact same raw `class_resources` JSON field through its own separate client-side HTML-table logic, which had the identical `class_features`-treated-as-flat-resource bug, still showing `class features: ?/?` in the structured table even after the text block above it was already fixed. No Python unit test exercises this render path at all — it only exists in the browser DOM.

**How to apply:** when a fix touches a field that gets rendered by both a backend text-formatter AND separate frontend JS, don't assume unit-testing the backend is sufficient — drive the actual UI once via a real browser and visually/programmatically check every surface that consumes the same data, not just the one you already fixed.

**Also relevant this session:** running `/integrate` on a long-lived worktree found ~90 uncommitted files (`.claude/hooks`, `.github/workflows`, `AGENTS.md`, etc.) with mtimes 4-12 days stale, plus 1 unpushed commit that was a fully-superseded 170-line early draft of a module that later grew to 600+ lines through the same PR's own history. `--force` auto-stashes (tagged `"integrate.sh --force: auto-stash on <timestamp>"`) rather than discarding — reversible, safe to use once mtimes/content confirm the dirty state predates the current task and is already superseded by merged work. See `[[br-discovery-is-not-cwd-confined]]`.
