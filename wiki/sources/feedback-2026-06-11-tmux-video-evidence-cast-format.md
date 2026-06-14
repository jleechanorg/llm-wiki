---
title: "tmux Video Evidence — .cast Format Required for Gate 6/8c"
type: source
tags: [tmux-video-evidence, gate-6, gate-8c, asciinema, cast, skeptic-gate, pr-7471]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-11_tmux_video_evidence_cast_format.md
---

## Summary
CodeRabbit + Skeptic FAIL Gate 6/8c when PR evidence is a text gist. The `skills/tmux-video-evidence/SKILL.md` enumerates accepted formats: `.mp4`, `.mov`, `.gif`, `.webm`, or `.cast` — all must be HTTPS-linked. PR #7471 (fix/constants-fetchapi-public) was rejected with text-only gist v4 (`b6a353dbce`) and accepted with asciinema `.cast` v5 (`48783ce2474a0674707938844dfbcd1c`).

## Key Claims
- Accepted formats: `.mp4`, `.mov`, `.gif`, `.webm`, or `.cast` — all HTTPS-linked.
- A GitHub Gist containing text logs does NOT satisfy Gate 6/8c.
- `.cast` is text-based JSON and uploads cleanly; `.gif` is binary and `gh gist` rejects it.
- The `.cast` ties test output to a specific commit via SHA bookend (pre-test == post-test `git rev-parse HEAD`).
- Record: `asciinema rec --command "evidence.sh" --cols 130 --rows 50 --idle-time-limit 4 --overwrite`.
- Upload: `gh gist create <file>.cast <file>.sh README.md --public`.
- Replay locally with `asciinema play <file>.cast`.
- Lane A fix recipe: 7-section evidence script template at `/Users/jleechan/.claude/skills/tmux-video-evidence.md`.

## Key Quotes
> "Reviewers treat text transcripts as 'no provenance guarantee' — the .cast ties test output to a specific commit via SHA bookend (pre-test == post-test `git rev-parse HEAD`)."

## Connections
- [[TmuxVideoEvidence]] — canonical evidence skill
- [[Gate6Evidence]] — Gate 6 evidence standard
- [[SkepticGateOps]] — Skeptic verdict integration
- [[PRGreenDefinition]] — 7-green criteria
