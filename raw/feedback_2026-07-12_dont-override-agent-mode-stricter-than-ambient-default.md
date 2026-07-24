---
name: dont-override-agent-mode-stricter-than-ambient-default
description: "Passing mode:\"acceptEdits\" to parallel Agent() subagent calls caused a permission-prompt pileup because it is MORE restrictive than the session's actual bypassPermissions default — never override to a stricter mode than ambient when firing many parallel subagents"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 0ffd19bb-d81f-4079-804c-1cea8a822f5b
---

During a large parallel fan-out (10 simultaneous `Agent()` calls for the EXTRACT-class command migration batch), several subagents' tool calls came back as "The user doesn't want to proceed with this tool use... rejected," and the user reported being stuck watching permission prompts pile up, defeating the point of parallelization ("it hurts parallelization because I'm sitting there on a screen and not working").

**Root cause**: I had explicitly passed `mode: "acceptEdits"` to those `Agent()` calls. Investigation showed the session's actual global `permissions.defaultMode` in `~/.claude/settings.json` was already `bypassPermissions` — the most permissive setting, meaning no prompts should occur at all under the ambient default. `mode: "acceptEdits"` is a STRICTER override (it only auto-accepts file-edit prompts; Bash and other tool calls still prompt) — so explicitly setting it on subagents actively downgraded them below the session's own configured permissiveness, causing exactly the prompt pileup the user hit when 10 agents' Bash calls all needed individual approval simultaneously.

**How to apply**: before passing an explicit `mode:` to `Agent()` (or any subagent-spawning call), check what the ambient session default actually is (`permissions.defaultMode` in the relevant `settings.json`). Do not pass a stricter mode than the ambient default "just to be safe" — it silently reintroduces the exact friction the ambient config was set up to avoid. If the mission genuinely needs full unattended execution (e.g. a long-running sidekick), match or exceed the ambient permissiveness (e.g. use `--dangerously-skip-permissions` at the CLI level for an external tmux sidekick, which fully bypasses prompts) rather than an intermediate mode that's tighter than what the user already configured.
