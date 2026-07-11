---
name: sidekick-default-in-session-teammate-not-tmux
description: "/sidekick + /swarm default = named in-session Agent-Team teammates visible in the user's panel (\"I want it in this session\"); external tmux sessions are FALLBACK only; durability = STATE.md + P1 bead + commit-often, not process persistence"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-m69ke (mission runbook; skill-fix captured here)
  originSessionId: 72ef9675-6c75-40f9-a0be-e8d19699ef6c
---

**Context**: 2026-07-11, worldarchitect.ai PR-fleet session. Three sidekicks were
launched as external `tmux new-session` Claude processes. To the user they read as
"we still didn't start the real claude team" — nothing appeared in their panel, and
the tmux teams were only visible via `tmux attach`/screenshots of other windows. User
corrected explicitly: "i dont wanna use separate tmux sessions i wanna use a real
/team-claude an the sidekick is a teammate i can see here" and "modify the /sidekick
and /swarm commands to make it more clear I want it in this session".

**Rule**: When the user asks for /sidekick, /swarm, or a "real claude team", the
DEFAULT is named in-process teammates of the CURRENT session's Agent Team —
`Agent({name, model: "sonnet", run_in_background: true})` — visible in the user's
panel and SendMessage-addressable both ways. External tmux sidekick sessions are the
FALLBACK only (must-survive-conversation-exit missions, or Agent Teams unavailable),
and require up-front disclosure of panel invisibility + the attach command.

**Why**: visibility IS the product for the user — an invisible worker is
indistinguishable from no worker. Durability is achievable without process
persistence: STATE.md checkpoints + P1 resumption bead + commit-often make a fresh
session's respawn cost one Agent() call.

**FIX (applied 2026-07-11)**: `~/.claude-wa/skills/sidekick/SKILL.md` (new "DEFAULT
MODE: in-session teammate" section; tmux content demoted to fallback),
`~/.claude-wa/skills/swarm/SKILL.md` (default-mode note in Sidekick durability
layer), `~/.claude-wa/commands/sidekick.md` (title + default banner),
`~/.claude-wa/commands/swarm.md` (default note). Live migration executed same
session: tmux sidekick checkpointed STATE.md, session killed, same-named teammates
(sidekick, lane-8286, lane-8322) respawned in-session against the same STATE.md.

**Verification**: in-session team spawned and visible (`sidekick@session-30a1dd26`
etc.); old tmux session `sidekick-worldarchitect-prompt-discipline-bugs` killed; 3
remaining sidekick tmux sessions belong to OTHER conversations (left untouched).

**Reusable pattern**: for any long-running worker primitive, "where does the user
SEE it" is a first-class requirement, not cosmetics. If a durable-worker design
makes the worker invisible to the user's normal UI, either surface it in that UI or
expect the user to conclude it doesn't exist. Related: [[tui-sidekick-stalls-alive-on-ratelimit-modal]]
(the invisible-stall variant of the same visibility problem).
