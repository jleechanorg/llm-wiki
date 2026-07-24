---
title: "Sidekick default = in-session Agent-Team teammate, not external tmux (2026-07-11)"
type: source
tags: [sidekick, swarm, agent-teams, orchestration, harness, feedback]
date: 2026-07-11
source_file: raw/feedback_2026-07-11_sidekick_default_in_session_teammate_not_tmux.md
---

## Summary
User correction during the worldarchitect.ai PR-fleet session: externally launched tmux sidekick sessions read as "the team never started" because nothing appeared in the user's panel. The /sidekick and /swarm default is now named in-process teammates of the invoking session's Agent Team — visible in the panel, SendMessage-addressable — with external tmux demoted to fallback for must-survive-session-exit missions. Durability in the default mode comes from STATE.md checkpoints + a P1 resumption bead + commit-often, not process persistence.

## Key Claims
- Panel visibility is a first-class requirement for worker primitives: an invisible worker is indistinguishable from no worker.
- Crash-durability does not require process persistence: STATE.md + `br` runbook bead + frequent pushes make respawn cost one Agent() call.
- A live mid-mission migration (tmux → in-session) is safe: checkpoint STATE.md, shut down lanes, kill the session, respawn same-named teammates against the same STATE.md.

## Key Quotes
> "i dont wanna use separate tmux sessions i wanna use a real /team-claude an the sidekick is a teammate i can see here" — user directive, 2026-07-11

## Connections
- [[sidekick]] — the skill whose default mode this corrects
- [[swarm]] — durability-layer section updated to match
- [[agent-teams]] — the in-session primitive that provides panel visibility
- [[tui-sidekick-stalls-alive-on-ratelimit-modal]] — sibling lesson: the invisible-stall variant of the same visibility problem
