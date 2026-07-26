---
title: "Electron app auto-installs via `ao start` invoked by Hermes launchd jobs — `rm -rf` is not durable"
type: source
tags: [ao, agent-orchestrator, electron-app, launchd, hermes, ditto, fix-on-discovery, anti-pattern]
date: 2026-07-24
source_file: raw/feedback-2026-07-24-electron-app-auto-install-trigger.md
---

## Summary

Any Hermes launchd job that calls `ao start` (legacy TS CLI or Go CLI) silently re-fetches and re-installs the `/Applications/Agent Orchestrator.app` Electron desktop app from GitHub releases via `ditto -x -k` (preserves original bundle timestamps). The actual trigger was `~/.hermes/scripts/beads-conflict-resolver.launchd.sh:38-45` which ran `ao start worldarchitect` whenever `ao session ls -p worldarchitect` was empty. `rm -rf` is not durable — disable the launchd job instead.

## Key Claims

- **`ao start` is the silent Electron app installer.** Both the legacy TS CLI (`/Users/jleechan/.nvm/versions/node/v22.22.0/bin/ao` → `@composio/ao-cli` global npm package → `@jleechanorg/ao-cli@0.1.3`) and the Go CLI (`/Users/jleechan/.local/bin/ao-go`) implement `start.go` with `fetchAppDarwin` that downloads the latest macOS release from GitHub and `ditto -x -k` unpacks it into `/Applications/`. Bundle timestamps are preserved (not regenerated), so the `installedAt` field in `~/.ao/app-state.json` always snaps back to the original `2026-07-12T20:07:33.388Z` value (the original install date).
- **The smoking gun.** `~/.hermes/scripts/beads-conflict-resolver.launchd.sh:38-45`:
  ```bash
  if ! ao session ls -p worldarchitect >/dev/null 2>&1; then
    echo "[$(date ...)] WARN: AO not running, attempting to start worldarchitect project..."
    ao start worldarchitect >/dev/null 2>&1 &
    sleep 5
  fi
  ```
  This pre-check fires whenever the worldarchitect project has no active sessions — which was almost always the case (30+ sessions stuck in `no_signal`).
- **Why my first fix didn't stick.** I disabled `ai.agento.health.plist` (calls `ao-health.sh` → `ao start <anchor>`) but missed `ai.hermes.schedule.beads-conflict-resolver`. Both have the same `ao start <project>` pattern. Lesson: **search the entire `.hermes/scripts/` for any `ao start` invocation, not just `ai.agento.*` plists.**
- **`ao spawn` is safe; only `ao start` is dangerous.** The Go CLI's `spawn` command doesn't fetch the app; only `start` does. So `ai.hermes.ao-notifier.py` (which calls `ao spawn`) is fine. But scripts that call `ao start <project>` for "session recovery" are silently reinstalling the desktop app on every tick.
- **The Electron app's own `writeAppStateOnLaunch()` rewrites `app-state.json` on every launch** (`/Users/jleechan/projects/agent-orchestrator/frontend/src/main.ts:1458`). This makes the file mtime misleading — it changes every time the app starts, regardless of what triggered the install.
- **`ditto -x -k` is the key piece** that explains why the bundle's mtime always reverts to the original Jul 12 timestamp after reinstall. Plain `unzip` would corrupt the code signature (`backend/internal/cli/start.go:152-160` says "ditto preserves the .app code signature; plain unzip corrupts it").
- **Re-install detection fingerprint:** `app-state.json` with `installedAt` set to the original install timestamp (e.g. `2026-07-12T20:07:33.388Z`) after a `rm -rf` is diagnostic of a `ditto -x -k` re-extract, not a fresh `time.Now()` write.

## Key Quotes

> "The user said they didn't click on it. and it should not even be installed. something else is installing it prob from launchd or the AO golang repo" — user message after the 4th reinstall cycle

> "// ditto preserves the .app code signature; plain unzip corrupts it (spec §6.3)." — `backend/internal/cli/start.go:159`

> "if ! ao session ls -p worldarchitect >/dev/null 2>&1; then
>   echo \"[$(date '+%Y-%m-%dT%H:%M:%S%z')] WARN: AO not running, attempting to start worldarchitect project...\"
>   ao start worldarchitect >/dev/null 2>&1 &" — `~/.hermes/scripts/beads-conflict-resolver.launchd.sh:39-41`

## Connections

- [[jleechanorg-agent-orchestrator]] — the source repo for the Go CLI whose `start.go` does the fetch
- [[Ao]] — the legacy TS CLI package that has the same `start` behavior; installed globally as `@composio/ao-cli`
- [[AgentOrchestratorDoctorShV2]] — `ao doctor` checks include port checks; the desktop app's bundled daemon is the canonical production `ao` per `app-state.json`'s `installSource: "npm-bootstrap"`
- [[ao-worker-liveness]] — both `ao start` and `ao worker liveness` are recovery actions; this learning only applies to `start`
- [[AO-Split-Brain]] — different problem (concurrent daemons), but related: a stale worldarchitect session list + a fired `ao start` could re-create the split-brain state
- Hermes / `ai.hermes.schedule.*` launchd jobs — broader class of cron actions that can have hidden side effects

## Fix (applied 2026-07-24)

| Action | Result |
|---|---|
| `launchctl bootout gui/501/ai.hermes.schedule.beads-conflict-resolver` | exit 0 |
| `mv ai.hermes.schedule.beads-conflict-resolver.plist ~/.ao/.disabled-launchagents/` | plist out of LaunchAgents |
| `launchctl bootout gui/501/ai.hermes.schedule.daily-repo-export` | exit 0 (target script was already missing) |
| `mv ai.hermes.schedule.daily-repo-export.plist ~/.ao/.disabled-launchagents/` | plist out of LaunchAgents |
| `pkill -9 -f '/Applications/Agent Orchestrator.app'` + `rm -rf /Applications/Agent Orchestrator.app` | bundle gone |

Verified clean: 30 s watch confirmed no respawn.

## Reusable pattern (debugging checklist)

When user reports "the Electron app should not be installed but it came back":

1. `ls /Applications/Agent Orchestrator.app` and `pgrep -f '/Applications/Agent Orchestrator.app'` for the smoking gun
2. `stat -f '%SB %Sm' /Applications/Agent Orchestrator.app/Contents/_CodeSignature/CodeResources` — if birth time matches the original install date, the bundle was re-extracted by `ditto -x -k`, NOT freshly created
3. `cat ~/.ao/app-state.json` — if `installedAt` is the original timestamp (e.g. `2026-07-12T20:07:33.388Z`), the full installer pipeline ran
4. `grep -rln 'ao start\b' /Users/jleechan/.hermes/scripts/` — find every script that calls `ao start`; cross-check `launchctl list | grep ai.` to find which ones are running launchd jobs
5. For each match: `launchctl bootout` + `mv <plist> ~/.ao/.disabled-launchagents/`
6. Delete the bundle, watch for 30 s, repeat if it returns

**Defensive guidance:** If the user has explicitly said the desktop app should not exist, the durable uninstall is to disable every launchd job whose `ProgramArguments` chain leads to `ao start`. `rm -rf` is temporary — the next launchd tick of the trigger will reinstall it.
