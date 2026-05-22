---
name: ao-ralph-lifecycle-worker-involuntary-stop-hook-injection-respawns-after-kill
description: "lifecycle-worker ralph is NOT ralph-wiggum; it's the AO project monitor for jleechanorg/ralph, managed by launchd+watchdog, and respawns within 2 min after kill"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-3ey45
  originSessionId: 1a26ca47-1291-4f8e-a5df-a8ba4aae7ff2
---

## Context

2026-05-21: User working on PR #6958 (worldarchitect.ai) was interrupted by an
external OS process (`node packages/cli/dist/index.js lifecycle-worker ralph`,
PID 17447) injecting "Stop hook feedback:" messages into the Claude Code session
every time Claude's turn ended. The process respawned immediately after
`kill 17447`. User was unable to brainstorm.

## Technical detail

### Two separate systems share the name "ralph" — do not confuse them

**System 1 — AO lifecycle-worker for project "ralph"**

`node packages/cli/dist/index.js lifecycle-worker ralph` is the AO lifecycle
polling daemon for the AO project whose config ID is `ralph` in:

```
/Users/jleechan/projects/jleechanclaw/agent-orchestrator.yaml
```

That project config:
- repo: `jleechanorg/ralph`
- path: `~/projects/ralph`
- sessionPrefix: `ra`

The lifecycle-worker polls GitHub every 75 s (default) for PR state changes.
When it detects a session as `agent-stuck` or `agent-needs-input`, it sends the
configured `reactions:` message template via `tmux send-keys` (through
`sessionManager.send()` → `runtime-tmux sendMessage()`) to whichever tmux pane
is running a Claude Code session for that project.

These injected tmux messages ARE what the user saw as "Stop hook feedback:".
The string comes from the AO reaction message template, not from the
ralph-wiggum plugin.

**System 2 — ralph-wiggum in-session stop hook**

Plugin at:
```
~/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/
```

Activated ONLY by `/ralph-loop` command, which writes:
```
.claude/ralph-loop.local.md
```

Uses a Claude Code `Stop` hook (`hooks/stop-hook.sh`) that fires when Claude
tries to exit and returns `{"decision":"block","reason":$prompt}`. Does NOT
spawn external OS processes.

Cancelled by `/cancel-ralph` or `rm .claude/ralph-loop.local.md`.

### Why `kill <PID>` alone does not stop it

Three layers restart the process:

1. `~/Library/LaunchAgents/com.ao-runner.plist` (StartInterval=3600) runs
   `~/.local/share/ao-runner/launchd-start.sh` → calls `scripts/start-all.sh`
2. `scripts/start-all.sh` relaunches `ao lifecycle-worker <projectId>` via
   `nohup ... &` for every project in the config
3. `scripts/lifecycle-watchdog.sh` (cron every 2 min) checks `pgrep -f
   "lifecycle-worker <project>"` and bootstraps via launchd if not running

Single `kill` takes out one PID. Watchdog restores it within ~2 minutes.

## Solution / rule

**To stop the AO lifecycle-worker for a specific project:**
```bash
ao stop ralph          # SIGTERM + clears PID file
```

**To stop all lifecycle-workers:**
```bash
ao stop                # all projects
pkill -f "lifecycle-worker"   # nuclear option
```

**To prevent respawn (for an extended manual session):**
```bash
launchctl unload ~/Library/LaunchAgents/com.ao-runner.plist
# Re-enable when done:
launchctl load ~/Library/LaunchAgents/com.ao-runner.plist
```

**To cancel a ralph-wiggum in-session loop:**
```bash
/cancel-ralph
# or: rm .claude/ralph-loop.local.md
```

**To prevent AO injection when doing manual brainstorming on a PR:**
```bash
ao session kill <sessionId>   # remove session from AO tracking
# or: ao stop before the brainstorm session
```

## Verification

- `pgrep -f "lifecycle-worker ralph"` confirms the process is gone after `ao stop`
- `ao session ls` shows whether the PR session is still tracked
- Without `launchctl unload`, the worker respawns within 1-2 minutes

## Key distinction table

| What | Command | Respawns? |
|------|---------|-----------|
| AO `lifecycle-worker ralph` (project monitor) | `ao stop ralph` | YES — launchd + 2-min watchdog |
| ralph-wiggum stop hook (in-session) | `/cancel-ralph` | NO — file-based |

## References

- AO config: `/Users/jleechan/projects/jleechanclaw/agent-orchestrator.yaml` (line 421)
- Lifecycle worker source: `/Users/jleechan/project_agento/agent-orchestrator/packages/cli/src/commands/lifecycle-worker.ts`
- Stop service: `packages/cli/src/lib/lifecycle-service.ts` `stopLifecycleWorker()`
- launchd plist: `~/Library/LaunchAgents/com.ao-runner.plist`
- Watchdog: `/Users/jleechan/projects/jleechanclaw/scripts/lifecycle-watchdog.sh`
- ralph-wiggum plugin: `~/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/`
- Prior related: `feedback_2026-05-15_stop_hook_human_gate_loop.md`

## Reusable pattern

**When a Claude session is being repeatedly interrupted by injected messages:**
1. `ps aux | grep lifecycle-worker` — identify the AO worker doing it
2. `ao stop <project>` — use the AO CLI, not bare kill
3. If it respawns: `launchctl unload ~/Library/LaunchAgents/com.ao-runner.plist`
4. For brainstorming uninterrupted: `ao session kill <sessionId>` first
5. `rm .claude/ralph-loop.local.md` only applies to in-session ralph-loop, not AO
