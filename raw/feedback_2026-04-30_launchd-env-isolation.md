---
name: launchd env-isolation AO workers
description: Launchd does not source .bashrc — MINIMAX_API_KEY must be explicitly passed to AO lifecycle-workers via plist EnvironmentVariables
type: feedback
bead: none
originSessionId: c48d7942-fc75-4976-af82-3e8b1a562d89
---
# Feedback: Launchd env-isolation for AO lifecycle-workers

## Context

AO workers for `jleechanorg/worldarchitect.ai` and other projects were failing with:
```
"login fail: Please carry the API secret key in the 'Authorization' field"
"model may not exist or you may not have access to it"
```

The tmux sessions spawned by lifecycle-workers appeared alive but couldn't authenticate with MiniMax.

## Technical detail

- Lifecycle-workers are spawned by `launchd` via `ai.agento.lifecycle-all.plist`
- Launchd services do NOT source `.bashrc`, `.bash_profile`, or `.profile`
- The minimax plugin reads `process.env.MINIMAX_API_KEY` in `getEnvironment()` (line 28 of `Agent-minimax/src/index.ts`)
- Inside the lifecycle-manager Node.js process, `process.env.MINIMAX_API_KEY` was `undefined` — the key was not inherited from the parent shell
- The plugin set `ANTHROPIC_API_KEY` only when `apiKey` (from `process.env.MINIMAX_API_KEY`) was truthy — since it was undefined, the env var was not set
- Spawned tmux sessions inherited no `ANTHROPIC_API_KEY` → all MiniMax API calls failed silently

## Solution

Added to `agent-orchestrator/launchd/ai.agento.lifecycle-all.plist.template`:
```xml
<key>MINIMAX_API_KEY</key>
<string>@MINIMAX_API_KEY@</string>
<key>MINIMAX_BASE_URL</key>
<string>@MINIMAX_BASE_URL@</string>
<key>MINIMAX_MODEL</key>
<string>@MINIMAX_MODEL@</string>
```

Added sed substitutions in `agent-orchestrator/scripts/setup-launchd.sh`:
```bash
-e "s|@MINIMAX_API_KEY@|$(escape_sed "$MINIMAX_API_KEY")|g" \
-e "s|@MINIMAX_BASE_URL@|$(escape_sed "${MINIMAX_BASE_URL:-https://api.minimax.io/anthropic}")|g" \
-e "s|@MINIMAX_MODEL@|$(escape_sed "${MINIMAX_MODEL:-MiniMax-M2.7}")|g" \
```

## Verification

```bash
# Installed plist check
grep MINIMAX_API_KEY ~/Library/LaunchAgents/ai.agento.lifecycle-all.plist
# → <string>sk-cp-Rg64V...(real key)</string>

# Running worker check
ps eww -p $(pgrep -f "lifecycle-worker") | grep MINIMAX_API_KEY
# → MINIMAX_API_KEY=sk-cp-Rg64V...(non-empty)

# Automated verification
bash scripts/test-launchd-env.sh
# → All env var checks passed
```

## References

- Commit: `jleechanorg/agent-orchestrator@893fae999` (fix, main)
- Commit: `jleechanorg/jleechanclaw@9152536ec` (CLAUDE.md guard, main)
- Template: `agent-orchestrator/launchd/ai.agento.lifecycle-all.plist.template`
- Script: `agent-orchestrator/scripts/setup-launchd.sh`
- Test: `agent-orchestrator/scripts/test-launchd-env.sh` (new)
- Skill update: `~/.claude/skills/harness-engineering/SKILL.md` (added launchd env-isolation failure class)

## Pattern

Any secret or config that lives in `.bashrc`/`.bash_profile` will silently disappear when a process moves from interactive shell to launchd. The fix is to explicitly add the env var to the plist's `EnvironmentVariables` dict AND to the `setup-launchd.sh` sed substitution block.

Rule: When adding AO lifecycle-worker plist entries, always audit runtime dependencies — any `.bashrc`-sourced secret must be explicitly propagated.