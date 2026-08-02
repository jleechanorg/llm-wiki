---
title: "PR #8602 evidence round 2: worktree identity, field-attribution, producer/verifier split"
type: source
tags: [evidence-standards, testing-infrastructure, worldarchitect-ai]
date: 2026-07-25
source_file: raw/feedback_2026-07-25_verify_server_worktree_identity_via_lsof.md, raw/feedback_2026-07-25_separate_evidence_producer_from_verifier.md, raw/reference_2026-07-25_burned_in_numeric_hud_for_video_evidence.md, raw/project_2026-07-25_paired_skill_pattern_user_story_worldai.md, raw/feedback_2026-07-25_streaming_claims_need_gunicorn_not_flask_dev.md
---

## Summary
Five follow-on lessons from the same PR #8602 (worldarchitect.ai, waitlist fail-closed UI fix) evidence effort that produced [[waitlist-fabricated-deny-and-ip-ratelimit-lockout]]. Together they extend the session's evidence-integrity theme: a running server isn't proof of what it's serving, a string match isn't proof of meaning, a producer isn't a reliable verifier of its own artifact, burned-in state turns judgment into reading, and a local dev server isn't proof of production behavior.

## Key Claims
- A local server answering on a known port is not proof it's running the branch under test — verify via `lsof -p <pid> | grep cwd` before every capture, not just at startup. Caught a lane accidentally testing against `wa_worktree_ratelimit` instead of the fix branch, rooted at `wa_worktree_waitlistui`. Confirmed in `/Users/jleechan/projects/wa_capture_staging/es_8602/MANIFEST.md`.
- A matched string is not a matched meaning: both "Social HP: 5/8" and "physical HP" claims contained the digit string "5/8", producing a false contradiction flag. Field/entity attribution must be checked before treating a string match as agreement or conflict. Extends [[grep-false-negative-is-systemic-not-occasional]] to the presence-match direction.
- The agent that produces video/screenshot evidence must not be the sole certifier of what it proves — a shooter's own PASS verdict missed a wrong-transition clip (claimed button state change, actually showed a Cancel status pill) and held back a real but mislabeled autoscroll finding. Requires a second, independent pass that re-opens raw frames against the original claim text.
- Burning numeric state (`scrollTop`, `scrollHeight`, `streamingTextLen`) directly into video frames converts a subjective motion judgment into a readable number — settled a scroll-preservation-during-streaming claim with `scrollTop` pinned at 49966 for 21s while `scrollHeight` grew 325px. Artifact: `docs/user-stories-ui/videos/scroll-position-preserved-during-streaming.mp4` on branch `docs/user-stories-ui-visual-spec`.
- Paired skill pattern: `.claude/skills/user-story-worldai/SKILL.md` (repo scope, product specifics) + `~/.claude/skills/user-story/SKILL.md` (user scope, general law), each requiring the other. Commit `68ce7dc85bc`. Routing rule: general practice up, product specifics down.
- worldarchitect.ai's local dev server runs Flask `app.run()` (`mvp_site/main.py:5671`); production runs `gunicorn -c gunicorn.conf.py` with gthread workers (`mvp_site/Dockerfile:99`). A streaming-behavior claim tested only against the dev server proves nothing about production concurrency/streaming behavior — test against gunicorn locally instead.

## Key Quotes
> "Its first GREEN run reproduced the same broken behavior as RED" — the tell that the server was rooted in the wrong worktree, not that the fix was broken.

> "Neither defect would have been caught by the shooter reviewing its own output" — on why evidence production and certification must be separate passes.

## Connections
- [[waitlist-fabricated-deny-and-ip-ratelimit-lockout]] — same PR #8602 evidence effort, same session
- [[grep-false-negative-is-systemic-not-occasional]] — sign-flipped sibling finding (presence-match vs absence-match false conclusions)
- [[evidence-standards]] — general evidence-class-must-match-claim-class discipline this extends
- [[static-gameplay-certification-miss]] — same family as burned-in-HUD fix (idle-bob/pixel-jitter defeating visual-only motion checks)
