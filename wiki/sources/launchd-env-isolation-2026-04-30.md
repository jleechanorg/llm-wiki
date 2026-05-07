# Launchd Env-Isolation — AO Lifecycle-Worker Auth Failure

## Source

Raw file: `~/llm_wiki/raw/feedback_2026-04-30_launchd-env-isolation.md`

## Summary

AO lifecycle-workers failed authentication with MiniMax API because **launchd does NOT source `.bashrc`** — `MINIMAX_API_KEY` was undefined when `lifecycle-manager` Node.js process was spawned by `ai.agento.lifecycle-all.plist`. Workers appeared alive in `tmux` but all MiniMax API calls silently failed with `"login fail: Please carry the API secret key"`.

## Root Cause

- Launchd services do not inherit shell environment variables
- `minimax` plugin reads `process.env.MINIMAX_API_KEY` in `getEnvironment()` (line 28 of `Agent-minimax/src/index.ts`)
- The plist had no `MINIMAX_API_KEY` in its `EnvironmentVariables` dict
- Spawned `tmux` sessions inherited no `ANTHROPIC_API_KEY` → auth failed silently

## Fix Applied

**plist template** (`agent-orchestrator/launchd/ai.agento.lifecycle-all.plist.template`):
```xml
<key>MINIMAX_API_KEY</key>
<string>@MINIMAX_API_KEY@</string>
<key>MINIMAX_BASE_URL</key>
<string>@MINIMAX_BASE_URL@</string>
<key>MINIMAX_MODEL</key>
<string>@MINIMAX_MODEL@</string>
```

**setup script** (`agent-orchestrator/scripts/setup-launchd.sh`):
```bash
-e "s|@MINIMAX_API_KEY@|$(escape_sed "$MINIMAX_API_KEY")|g" \
-e "s|@MINIMAX_BASE_URL@|$(escape_sed "${MINIMAX_BASE_URL:-https://api.minimax.io/anthropic}")|g" \
-e "s|@MINIMAX_MODEL@|$(escape_sed "${MINIMAX_MODEL:-MiniMax-M2.7}")|g" \
```

**Verification** (`agent-orchestrator/scripts/test-launchd-env.sh`):
```bash
ps eww -p $(pgrep -f "lifecycle-worker") | grep MINIMAX_API_KEY
# → MINIMAX_API_KEY=sk-cp-Rg64V...(non-empty)
```

## Pattern

> Any secret or config that lives in `.bashrc`/`.bash_profile` will silently disappear when a process moves from interactive shell to launchd. The fix is to explicitly add the env var to the plist's `EnvironmentVariables` dict AND to the `setup-launchd.sh` sed substitution block.

## References

- Commit: `jleechanorg/agent-orchestrator@893fae999` (fix, main)
- Commit: `jleechanorg/jleechanclaw@9152536ec` (CLAUDE.md guard, main)
- Template: `agent-orchestrator/launchd/ai.agento.lifecycle-all.plist.template`
- Script: `agent-orchestrator/scripts/setup-launchd.sh`
- Test: `agent-orchestrator/scripts/test-launchd-env.sh` (new)
- Skill update: `~/.claude/skills/harness-engineering/SKILL.md` (added launchd env-isolation failure class)
