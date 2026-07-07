---
name: ezgha fleet incident recap (2026-07-06/07)
description: Consolidated failure modes, fixes, and anti-patterns from ez-gh-actions fleet hardening session
type: feedback
bead: ez-gh-actions-2ik
---

# ezgha fleet incident recap — what went wrong and what fixed it

Session scope: Mac (6× `ez-mac-runner-b-*`) + Linux jeff-ubuntu (16× `ez-runner-b-*`), repo `jleechanorg/ez-gh-actions`, related harness PR [worldarchitect.ai #8193](https://github.com/jleechanorg/worldarchitect.ai/pull/8193).

## Failure chain (ordered)

### 1. Two different "watchdogs" (confusion + double remediation)
- **systemd `WatchdogSec`** in `ezgha.service` (`Type=notify`): kills `ezgha serve` with SIGABRT if no `sd_notify(WATCHDOG=1)` within the window. Journal: `Watchdog timeout (limit Nmin)!`
- **External `ezgha-watchdog.timer`**: runs `~/.local/bin/ezgha-fleet-watchdog.sh` every 120s to restart when managed < configured. Separate job; currently failing exit 2 on Linux.
- **Anti-pattern:** Treating fleet restarts from the external script as the same problem as SIGABRT watchdog kills.

### 2. systemd watchdog too aggressive for real work (Critical)
- `ensure_count` on 16 slots does paginated `gh api list runners`, JIT registration, 409 self-heal (another full list), and batch `docker run` — routinely **>180s** before pings covered those paths.
- `install-service` with `WatchdogSec=60` then `180` **caused** Linux flapping (not fixed it) until pings landed.
- **Fix shipped:** [`aabd822`](https://github.com/jleechanorg/ez-gh-actions/commit/aabd822) + [`045cd66`](https://github.com/jleechanorg/ez-gh-actions/commit/045cd66): `src/watchdog.rs`, pings in `github.rs`/`docker_backend.rs`, `WatchdogSec=300`.
- **Residual risk:** A stuck `gh` child can still exceed 300s; next step is ping inside `run_gh` or disable only as last resort via drop-in.

### 3. Mac `minimum_isolation=vm` on Colima (Mandatory)
- Colima = docker-in-VM, but ezgha backend isolation level is still **`container`**.
- `minimum_isolation = "vm"` in `~/.config/ezgha/config.toml` → serve **fail-closed** on daemon blips.
- **Fix:** Set `container`; codified in `config/config.toml.mac.example` ([`1f3948f`](https://github.com/jleechanorg/ez-gh-actions/commit/1f3948f)).

### 4. Hard fleet reset wedge (Anti-Pattern)
- Stop supervisor + `docker rm` all managed + wipe `slot_assignments.toml` while GitHub still has **`offline+busy`** runner registrations.
- JIT then fails: `runner name 'ez-runner-b-N' already in use` / `all 16 slots in use`.
- `gh api DELETE` on busy runners returns **422** until the workflow job is cancelled.
- **Rule:** Soft reset only (`systemctl restart` / `launchctl kickstart -k`). Wipe slot file only when doctor confirms wedge. Cancel stale in-progress runs before expecting busy flags to clear.

### 5. Transient container count dips (Best Practice)
- Ephemeral JIT runners exit when jobs complete (`docker run --rm`).
- Poll between job-end and next `ensure_count` tick (~30s) shows **15/16** — not necessarily a failure.
- Watchdog SIGABRT creates a **30s supervisor gap** → same transient dip.

### 6. Queue saturation mistaken for runner crashes (Best Practice)
- Scan of last 20 PRs: **0 runner failures** in completed self-hosted job logs.
- Symptom: stuck `queued`, tail >45–95m, 0 idle runners. Capacity backlog, not infra death.
- Safe relief: `scripts/cleanup-stuck-runs.sh --zombies` (delete >24h queued); `--tail` cancel >45m on **non-target** branches. Do not cancel in-progress or PR-under-test runs.

### 7. Stale systemd unit after binary upgrade (Mandatory)
- `cargo install` updates binary SHA (Gate 0) but **does not** refresh `ezgha.service` on remote hosts.
- Must run `ezgha install-service` after deploy so `WatchdogSec` / `Type=notify` match the binary.
- Linux drop-in `disable-watchdog.conf` was a valid **temporary** ops override until code pings shipped.

### 8. Harness Gate 2 macOS blind spot (Best Practice)
- `docs/verify-exit-criteria.sh` called `systemctl` on Mac → false FAIL.
- Fixed: launchd probe like `doctor.sh` ([`1f3948f`](https://github.com/jleechanorg/ez-gh-actions/commit/1f3948f)).

### 9. Fixes not on origin until late (Process)
- Watchdog/doctor/queue scripts were deployed via `cargo install` + rsync **before** commit — Gate 0 failed for other operators.
- Shipped: [`aabd822`](https://github.com/jleechanorg/ez-gh-actions/commit/aabd822), [`42dff7c`](https://github.com/jleechanorg/ez-gh-actions/commit/42dff7c), [`045cd66`](https://github.com/jleechanorg/ez-gh-actions/commit/045cd66), config templates [`1f3948f`](https://github.com/jleechanorg/ez-gh-actions/commit/1f3948f).

## Verification commands

```bash
# Fleet counts
ezgha status
docker ps --filter label=ezgha=managed -q | wc -l

# Linux watchdog kills
ssh jeff-ubuntu 'journalctl --user --since "10 min ago" -u ezgha.service | rg -i "watchdog|SIGABRT"'

# Doctor + harness
./doctor.sh
./docs/verify-exit-criteria.sh

# Queue tail
./scripts/queue-health.sh
```

## Reusable rules

1. **Ping anywhere `gh` or batch spawn can block** before relying on WatchdogSec.
2. **Soft reset > hard reset** for ezgha fleet.
3. **Mac Colima → `minimum_isolation=container`** always.
4. **Distinguish saturation from crash** (queued tail vs job log failures).
5. **`install-service` after every fleet binary deploy** on Linux.

**Why:** Multiple independent failure modes compounded into AMBER fleet state while runners were still executing jobs.

**How to apply:** On any ezgha fleet incident, walk the failure chain top-down: watchdog type → policy/config → reset method → GitHub busy zombies → queue saturation. Do not restart-loop.
