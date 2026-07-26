---
name: electron-app-auto-installs-via-ao-start-invoked-by-hermes-launchd-jobs
description: "`ai.hermes.schedule.beads-conflict-resolver` and other Hermes cron jobs call `ao start <project>` whenever `ao session ls -p <project>` returns empty; legacy `ao start` (and Go `ao-go start`) always fetches the Electron app from GitHub releases and `ditto -x -k`-unpacks it with original timestamps, so the app re-installs itself without any user action."
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 45b33467-2f54-4132-9b73-d44567e3e9e3
---

# Context

User (jleechan) had a long-running frustration: `/Applications/Agent Orchestrator.app` (the Electron desktop app) kept coming back after every `rm -rf`, sometimes within hours, sometimes after a day. User said they never clicked the Dock icon or ran `open`, and the app should not even be installed (the desired setup is headless `ao-go` daemon + Web UI only, no GUI).

# Technical detail

The Electron app is fetched+unpacked by **any** `ao start` invocation on macOS:

- **Legacy TS CLI** (`/Users/jleechan/.nvm/versions/node/v22.22.0/bin/ao` — symlinked from `@composio/ao-cli` global npm package → `@jleechanorg/ao-cli@0.1.3`): `start.go` does `ditto -x -k` to extract the GitHub release zip. Bundled daemon timestamps are **preserved** (not regenerated), which is why `~/.ao/app-state.json`'s `installedAt` field kept snapping back to `2026-07-12T20:07:33.388Z` (the original install date).
- **Go CLI** (`/Users/jleechan/.local/bin/ao-go`): also has `start.go` with `fetchAppDarwin` (same `ditto` + GitHub release fetch). The Go CLI's `ao spawn` is safe; only `ao start` is dangerous.
- The Electron app's own `frontend/src/main/auto-updater.ts` + `frontend/src/main.ts:writeAppStateOnLaunch()` rewrites `~/.ao/app-state.json` on every launch — this is why the file mtime updates even when nothing else is calling `ao`.

# Smoking gun (the actual trigger)

`/Users/jleechan/.hermes/scripts/beads-conflict-resolver.launchd.sh:38-45`:

```bash
if ! ao session ls -p worldarchitect >/dev/null 2>&1; then
  echo "[$(date ...)] WARN: AO not running, attempting to start worldarchitect project..."
  ao start worldarchitect >/dev/null 2>&1 &
  sleep 5
fi
```

Launchd job `ai.hermes.schedule.beads-conflict-resolver` runs this script every cycle. When `ao session ls -p worldarchitect` is empty (which it almost always was — worldarchitect had 30+ sessions stuck in `no_signal`), the script runs `ao start worldarchitect` which:
1. Calls legacy `ao start` (the script prepends `NVM_BIN` to PATH, so the legacy TS CLI on `~/.nvm/versions/node/v22.22.0/bin/ao` wins over `~/bin/ao`)
2. Legacy CLI's `start.go` sees no app at `/Applications/Agent Orchestrator.app` → downloads latest release from `releases/download` → `ditto -x -k` unpacks it (preserves original Jul 12 timestamps) → opens it
3. Electron main launches → `writeAppStateOnLaunch()` rewrites `app-state.json` with `installedAt: 2026-07-12T20:07:33.388Z`

Same pattern in:
- `/Users/jleechan/.hermes/scripts/ao-manager.sh` (only `ao start` in comments, no exec)
- `/Users/jleechan/.hermes/scripts/validate-state.sh` (only `ao start` in pgrep pattern, no exec)
- `/Users/jleechan/.hermes/scripts/beads-conflict-resolver.sh` (only logs the suggestion)

# Solution / Rule

**FIX (applied 2026-07-24):**
- `launchctl bootout gui/501/ai.hermes.schedule.beads-conflict-resolver` + plist moved to `~/.ao/.disabled-launchagents/`
- `launchctl bootout gui/501/ai.hermes.schedule.daily-repo-export` + plist moved (its target script `standard_ao_jobs.py` is missing anyway, but the plist was live)

**Defensive guidance for this user:**
- If `ao start` must run, it MUST be after explicit consent, and `rm -rf` of the bundle is not a durable uninstall because launchd-side `ao start` will redownload.
- `rm -rf /Applications/Agent Orchestrator.app` is a TEMPORARY uninstall; the durable uninstall is to disable the launchd job(s) that call `ao start`.
- `ai.hermes.ao-notifier` is safe — it calls `ao spawn`, not `ao start`. Keep it on.
- `ai.agento.health.plist` (calls `ao-health.sh` which calls `ao start <anchor>`) is also a vector — already disabled in the same `~/.ao/.disabled-launchagents/` dir from a prior session.

# Verification

After the fix:
```
$ ls /Applications/Agent Orchestrator.app
ls: /Applications/Agent Orchestrator.app: No such file or directory
$ ps aux | grep Agent.Orchestrator.app | grep -v grep
(empty)
$ ls /Users/jleechan/.ao/.disabled-launchagents/
ai.agento.health-guardian.plist
ai.agento.health.plist
ai.hermes.schedule.beads-conflict-resolver.plist
ai.hermes.schedule.daily-repo-export.plist
```

Electron app stayed gone for the remainder of the session (multiple "delete + 30s watch + still gone" cycles).

# References

- `~/.hermes/scripts/beads-conflict-resolver.launchd.sh:38-45` — the trigger (now disabled)
- `~/.hermes/scripts/ao-manager.sh:152,173` — also has `ao start` calls (currently in comments only, but risk)
- `~/.hermes/scripts/validate-state.sh:35` — references `ao start` in pgrep pattern only
- `/Users/jleechan/projects/agent-orchestrator/backend/internal/cli/start.go:18` — `releaseRepo` is the GitHub source for the bundle
- `/Users/jleechan/projects/agent-orchestrator/backend/internal/cli/start.go:152-160` — `ditto -x -k` (the timestamp-preserving extraction)
- `/Users/jleechan/projects/agent-orchestrator/frontend/src/main.ts:1458` — `writeAppStateOnLaunch` (the app-side `app-state.json` rewriter)
- `/Users/jleechan/projects/agent-orchestrator/frontend/src/main/auto-updater.ts:79-82` — `escalationTimer` / `automaticUpdateTimer` / `retirementPollTimer` (30-min cadences; only run while the app is open, so not a background re-installer)
- `/Users/jleechan/.npmrc` — has `npm_REDACTED` token (user-only; not a hermes-managed artifact)

# Reusable pattern

When the user says "the Electron app should not even be installed":

1. `ls /Applications/Agent Orchestrator.app` to confirm
2. `pgrep -f '/Applications/Agent Orchestrator.app'` for processes
3. If gone: `grep -rln 'ao start' /Users/jleechan/.hermes/scripts/` and inspect each match for actual `subprocess.Popen` / `&` invocation (not just comments)
4. Cross-check `launchctl list | grep ai.` and find jobs whose `ProgramArguments` invoke any script that calls `ao start`
5. For each match: `launchctl bootout` + `mv <plist> ~/.ao/.disabled-launchagents/`
6. Delete the bundle, watch for 30s, repeat if it returns

The pattern: **a launchd job calling `ao start` is a silent auto-installer for the Electron app on macOS**, regardless of whether the user wants the GUI.
