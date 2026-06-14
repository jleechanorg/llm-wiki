---
title: "PR #7367 desktop auth-init indicator — Skeptic rounds 19-21"
type: source
tags: [auth, desktop, skeptic, evidence-iteration, pr-7367, worldarchitect-ai]
date: 2026-06-08
source_file: raw/project_2026-06-08_pr7367_evidence_iteration.md
---

## Summary
PR #7367 (fix(auth): render minimal authenticating indicator on desktop 8s timeout) Skeptic round-by-round progression. Round 19: FAIL on gates 1, 3, 4, 5, 6, 7, 8, 8c — critical bug: indicator used color:rgba(255,255,255,0.7) (light text on transparent background) — INVISIBLE on light-theme body. Round 20: PASS on 1-5, 7; FAIL on 6/8c: evidence videos were local /tmp/... paths, not hosted HTTPS URLs. Round 21: PASS on 2-7; FAIL on gate 1 (CI in flight), gate 8 (design doc N/A justification missing). Fix: added 'Design decision & tracking' section. Skeptic FAIL-suppress window (FAIL_SUPPRESS_WINDOW_SECS) creates long effective latency between iterations.

## Key Claims
- Round 19 critical bug: indicator color:rgba(255,255,255,0.7) on transparent background = INVISIBLE on light-theme body; fix = inline background-color:rgba(0,0,0,0.55) + color:#ffffff + role=status + aria-live=polite
- Round 20: hosted evidence required — Skeptic Gate 6/8c requires HTTPS media URLs tied to head SHA; local paths or gist-hosted base64 PNGs are insufficient; pattern: commit .mp4 to docs/evidence/pr-<N>/ on branch and reference as github.com blob URL
- Round 21: design doc N/A must be explicit in PR body — 'Design doc: N/A — small auth-init UX improvement on the 8s watchdog fallback path; not a design-doc-driven change'
- Skeptic FAIL-suppress window (FAIL_SUPPRESS_WINDOW_SECS) prevents re-triggering for a window after recent FAIL verdict; to iterate fast, push a new commit (new head SHA) so cron finds a missing verdict
- Code-trace + tests ≠ sufficient evidence for UI changes — Skeptic Gate 8c requires real browser video tied to the changed behavior

## Connections
- [[SkepticGate6]]
- [[SkepticGate8c]]
- [[HostedEvidence]]
- [[PR7367DesktopAuth]]
