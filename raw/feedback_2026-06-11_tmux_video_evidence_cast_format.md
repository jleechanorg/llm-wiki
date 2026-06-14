---
name: tmux-video-evidence-cast-format
description: Skills/tmux-video-evidence/SKILL.md requires HTTPS-linked .cast (asciinema) or .mp4/.mov/.gif/.webm for terminal TDD evidence; text gists FAIL Gate 6/8c
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f8097264-98da-4347-9747-5a6945acc955
---

CodeRabbit + Skeptic FAIL Gate 6/8c when PR evidence is a text gist. The
`skills/tmux-video-evidence/SKILL.md` enumerates accepted formats:
`.mp4`, `.mov`, `.gif`, `.webm`, or `.cast` — all must be **HTTPS-linked**.
A GitHub Gist containing text logs does NOT satisfy this. PR #7471 (fix/
constants-fetchapi-public) hit this twice: v4 gist `b6a353dbce` was text-
only and was rejected; v5 gist `48783ce2474a0674707938844dfbcd1c` with a
live asciinema `.cast` terminal recording was accepted.

**Why:** The skill is the canonical evidence standard in the repo. Reviewers
treat text transcripts as "no provenance guarantee" — the .cast ties test
output to a specific commit via SHA bookend (pre-test == post-test
`git rev-parse HEAD`).

**How to apply:** When the lane needs Gate 6/8c evidence, record an
asciinema `.cast` via `asciinema rec --command "evidence.sh" --cols 130
--rows 50 --idle-time-limit 4 --overwrite`, then upload to a public gist
via `gh gist create <file>.cast <file>.sh README.md --public`. The
`.cast` is text-based JSON and uploads cleanly. (`.gif` is binary and
gh gist rejects it: "binary file not supported".) Replay locally with
`asciinema play <file>.cast`. Lane A fix recipe: 7-section evidence
script template at `/Users/jleechan/.claude/skills/tmux-video-evidence.md`
(Section 1 git provenance → Section 7 code invariants).
