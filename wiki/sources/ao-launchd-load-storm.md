---
name: ao-launchd-respawners-cause-load-486-storm-bootout-to-stop
description: "Machine slowness (load 486 on 14 cores) was AO/agy worker pile-up + Docker VM, fed by antigravity-loop launchd agents (300s/600s) + in-tree AO lifecycle-worker; kill alone fails, must launchctl bootout (and disable for permanence); protect cmux/claude/codex"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-a62ad
  originSessionId: d8581237-b9f7-434f-836d-f76dc907d39b
---

# AO launchd respawners cause runaway load — kill is insufficient, bootout the agents

## Context (2026-05-31)
Machine became unusable: **load average 486 / 501 / 405 on a 14-core CPU** (~35× oversubscription, 0% idle, 47GB RAM used / 248MB free, 100M+ swapins). Symptom looked like "PRs are heavy" but the PR/review work was negligible. Root cause was an **accumulated agent pile-up**.

## What was actually consuming the machine
- `com.apple.Virtualization.VirtualMachine` (Docker's Linux VM) — **255% CPU** + `com.docker.backend` 61%.
- **~44 `agy` (Antigravity/Gemini AO worker) processes** — ~423% CPU aggregate.
- `openclaw-gateway` crash-looping (etime 5–14s, ~50% CPU) — constantly respawned.
- AO `lifecycle-worker cmux` (respawns agy), plus `eloop` drivers.
- 1,496 procs / 13,152 threads / 23 user sessions.

## Root respawners (the actual culprits) — all launchd user agents
Killing `agy`/gateway alone does NOT work — they respawn within ~2 min. The respawn sources are **launchd agents** that must be `launchctl bootout`'d:

| launchd label | mechanism (verified from plist) | what it spawns |
|---|---|---|
| `com.jleechan.antigravity-loop` | `StartInterval=300` → `~/.antigravity-loop/watchdog.sh` | antigravity/agy worker loop — **primary agy spawner** |
| `ai.openclaw.antig-cmux-loop` | `StartInterval=600` → `~/.openclaw/scripts/antig-cmux-loop.sh` | antigravity cmux/agy loop |
| `com.ao-runner` / `com.ao-runner-watchdog` | `StartInterval=3600` → `~/.local/share/ao-runner/launchd-start.sh` | AO runner fleet (was already not-loaded this session) |
| `ai.worldarchitect.ao-10min-monitor` | scheduled | AO monitor (not-loaded this session) |
| `ai.hermes.ao-notifier`, `ai.hermes.schedule.ao-progress-reporter` | scheduled | AO notification/report monitors |
| `ai.hermes-watchdog` | `StartInterval=300` → `hermes-watchdog.sh` | **NOT a respawner** — only health-checks prod(8642)/staging(8643) gateways and alerts Slack if down. Booted it out anyway to cut noise, but it was not a load source. |

**Corrected understanding:** the agy storm came from the **antigravity loops** (`com.jleechan.antigravity-loop` 300s + `ai.openclaw.antig-cmux-loop` 600s) plus an in-tree AO `lifecycle-worker cmux` that respawns agy at app level, NOT from hermes-watchdog (which only alerts). Earlier guess of "120s eloop-runner / hermes meta-respawner" was wrong — verified from the actual plists.

## Solution / rule (triage protocol)
1. **Protect first**: compute cmux app tree (`pgrep -f 'cmux DEV'` + descendants) + main `bin/claude` + `codex` PIDs; never kill these.
2. **Quit Docker** (`osascript -e 'quit app "Docker"'`) — frees the ~300% VM+backend. Don't force-kill the VM.
3. **Bootout respawners BEFORE killing workers**: `launchctl bootout gui/$(id -u)/<label>` for the table above. Kill the eloop/lifecycle drivers (`pgrep -f 'eloop cmux'`, `pgrep -f lifecycle-worker`).
4. **Then drain** `agy` (TERM, then KILL survivors) and `openclaw-gateway`.
5. Stray read-only `find`/`rg`/`grep` are safe to kill anytime.

Result: load **486 → 18 → 8** within ~10 min; cmux (9 procs) + claude (5) survived.

## Reversal / persistence note
`launchctl bootout` is **session-scoped** — agents reload on next login/reboot unless the plist is also disabled (`launchctl disable gui/<uid>/<label>`) or removed from `~/Library/LaunchAgents/`. To make permanent, disable the plists; otherwise the storm returns after reboot. This is a [[ao-spawn-gate]] / spawn-storm problem (cf. CLAUDE.md "AO spawn safety — 517-session incident 2026-05-15").

## Verification
- `uptime` 486→8.05; `pgrep -xc agy`=0, `pgrep -fc openclaw-gateway`=0, `lifecycle-worker`=0, VM=0.
- Protected confirmed alive: `pgrep -fc 'cmux DEV'`=9, `pgrep -fc 'bin/claude'`=5.
- Reports: /tmp/triage_report.txt, /tmp/ao_fullstop_report.txt.

## Reusable pattern
When a dev Mac is pathologically slow with huge load avg: it's almost never the foreground task — `ps -Ao pid,%cpu,comm -r | head` + count `agy`/`node`/`codex`/tmux. If workers respawn after kill, the cause is a **launchd agent with KeepAlive/StartInterval**; `launchctl bootout` (and `disable` for permanence) is the only durable stop. Always protect cmux/claude/codex PIDs explicitly.
