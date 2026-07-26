---
title: "Nextsteps — worldarchitect.ai fleet /green+/er drive — 2026-07-11"
type: source
tags: [worldarchitect, pr-fleet, green-gate, coderabbit, sidekick, nextsteps]
date: 2026-07-11
source_file: ~/roadmap/nextsteps-2026-07-11-fleet-green-er-drive.md
---

## Summary

A multi-day, multi-pass drive across all open non-draft PRs on `jleechanorg/worldarchitect.ai`, aimed at getting every PR to a green-CI + CodeRabbit-approved + `/er`-verified state without merging anything without explicit human approval. A morning pass (~06:00-10:25Z) reached a "workflow-gate terminal state" that later self-corrected when local `/er` review found several of its claimed-green PRs were actually FAIL/INCONCLUSIVE. A later same-day pass (~19:00-21:30Z) fixed 6 real bugs (5 CI/infra + one genuine production bug in a god-mode adjuster), refreshed stale evidence on 3 PRs, and ran a full 41-agent read-only review of the entire fleet, categorizing every PR by the exact action that closes it out.

## Key Claims

- Of 41 open non-draft PRs reviewed: 7 (17%) were genuinely ready for a human merge decision, 15 (37%) were CI-green but blocked purely on a stale-or-missing CodeRabbit review at the current head SHA, 15 (37%) were under active external `fixpr`/codex automation and should not be touched, 3 needed a specific CI gate fixed (beads-validation format, Evidence Gate, Green Gate root-cause), and 1 needed a rebase.
- CodeRabbit review staleness — not code defects — is the dominant blocker class across the fleet. The same failure mode (an APPROVED review recorded at an old commit, with real commits landing afterward) recurred on at least 5 separate PRs this session (#7977, #8309, #8286, #8318, #8299).
- Fixing an "evidence gap" on PR #8292 surfaced a genuine production bug: a shipping SUPPRESSION-category god-mode XP-downgrade adjuster was silently defeating a real, pre-existing E2E regression test, because `world_logic.py` hardcodes `agent_mode='god'` for every `GOD_MODE_UPDATE_STATE:` request with no way to distinguish a narrative directive from a raw structured patch. Fixed by disabling the adjuster (`active=False`) and restoring the original tested behavior, rather than fabricating evidence to paper over the discrepancy.
- PR #8195 uncovered a systemic Green Gate bug — legitimate `cancelled` conclusions (from `cancel-in-progress: true` reruns) were misclassified as blocking failures, creating a self-perpetuating false-negative loop. The fix had already independently landed on `main` via a sibling PR (#8314); the agent correctly detected the duplicate and deduped rather than landing redundant code.
- Same-day mission-tracking drift: at least 3 overlapping tracking artifacts (this nextsteps doc, bead `rev-lq4j8`, bead `rev-pr1vn`) existed for the same drive with no single source of truth, and two separate sidekick `STATE.md` checkpoint files were lost to `/tmp` cleanup mid-session — the same "phantom bead" failure mode recurring at the mission-tracking layer itself.
- The `/sidekick` skill's default mode changed as of a 2026-07-11 user directive: sidekicks now spawn as named in-session Agent-Team teammates (visible, `SendMessage`-addressable) rather than external tmux processes by default; tmux remains the fallback for missions that must outlive the session.

## Key Quotes

> "Live re-check always wins over any prior snapshot" — the core operating rule reapplied throughout, after a competing mission-tracker's 12:40Z verdict claiming #8323/#8290/#8286 as "full-green" was found stale against this session's live re-check (both genuinely CI-red, one still actively churning).

## Connections

- [[GreenGateWorkflow]] — the 6-gate CI mechanism this whole drive is measured against; PR #8195's fix and the GATE-3 status-only fallback (bead rev-s7vs6) both modify this workflow's behavior.
- [[CodeRabbitStaleLineRefs]] — closely related staleness pattern; this drive found the analogous "stale APPROVED review at an old commit" failure mode recurring across 15 of 41 PRs.
- [[CodeRabbitDismissedPattern]] — related CodeRabbit-reliability theme.
- [[SevenGreenQueue]] — the drive's target end-state definition (7-green + CR approved + evidence).
- [[WorldArchitectAI]] — parent project.
- [[EzGhaDaemon]] — the self-hosted runner fleet this drive's CI checks execute against; runner saturation was a recurring root cause of "unstable" mergeable_state noise distinct from genuine code defects.
