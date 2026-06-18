---
title: "launchd"
type: concept
tags: [macos, daemon, service-manager]
sources: [openclaw-tailscale-tunnel-script]
last_updated: 2026-04-08
---

## Description
launchd is the service management framework on macOS that handles daemon and agent processes. Scripts note that launchd jobs start with a minimal PATH, requiring explicit PATH configuration.

## Connections
- [[OpenClawTailscaleTunnelScript]] — mentions launchd PATH limitations
- [[Tailscale]] — tailscaled daemon runs via launchd on macOS

## Dry-run safety pattern for install scripts

When a bash install script manages launchd plists, **all file writes must happen after the dry-run gate**. The `sed` substitution that writes to `~/Library/LaunchAgents/` is a write operation — it must not execute in dry-run mode even if `launchctl bootstrap` is skipped.

```bash
# CORRECT — gate first
if $DRY_RUN; then dry "would install: ..."; return; fi
sed -e "s|@HOME@|$HOME|g" "$src" > "$dest.tmp" && mv "$dest.tmp" "$dest"
```

See: [[setup-launchd-dryrun-2026-05-19]] (bead orch-ud0d, commit ab684908be)

## References
- Socket path on macOS: /var/run/tailscale/tailscaled.sock
- Hermes setup script: `~/.hermes/scripts/setup-launchd.sh`

## Plist template placeholder discipline (2026-05-19)

`setup-launchd.sh` substitutes exactly 4 placeholders. Any other format survives as a literal string:

| Substituted | Not substituted |
|---|---|
| `@HOME@` | `@NODE_BIN_DIR@` |
| `@HERMES_BIN@` | `__HOME__` |
| `@REPO_ROOT@` | any custom `@NAME@` not in sed list |
| `@HERMES_EXTRA_PATH@` | |

Audit command:
```bash
grep -r "@[A-Z_]*@" ~/.hermes/launchd/*.template \
  | grep -v "@HOME@\|@HERMES_BIN@\|@REPO_ROOT@\|@HERMES_EXTRA_PATH@"
```

## MINIMAX vars behind .bashrc interactive guard

`.bashrc` interactive guard at line 283 blocks exports at line 894+. `launchd-env-wrapper.sh` uses `_extract_bashrc_var` to grep `.bashrc` directly, bypassing the guard:

```bash
_extract_bashrc_var() {
  local var="$1"
  [ -n "${!var:-}" ] && return
  local val
  val=$(grep -m1 "^export ${var}=" "$HOME/.bashrc" 2>/dev/null \
    | sed "s/^export ${var}=//;s/^['\"]//;s/['\"]$//" | tr -d '\n')
  [ -n "$val" ] && export "$var=$val"
}
```

**Never use `source .bashrc` inside a `bash -c` ProgramArguments string** — hits the same guard. Use `launchd-env-wrapper.sh` as the entry point instead.

## Orphaned installed plists

Every plist in `~/Library/LaunchAgents/` must have a corresponding `.plist.template` in `~/.hermes/launchd/` and be listed in `setup-launchd.sh` CORE_PLISTS or SCHEDULE_PLISTS. Orphans can't be re-installed by automation.

See: [[plist-template-drift-2026-05-19]] (bead orch-oxdm, PR #584)

## RC sourcing isolation (2026-06-09)

When a launchd-supervised bash script needs login/interactive env (DOCKER_HOST,
NVM, PATH, GOPATH, etc.) it must `source ~/.bash_profile ~/.zprofile ~/.bashrc ~/.zshrc`.
**Two shell options must be relaxed around the sourcing block** — they are independent
failure modes:

1. **`set +u` around the rc block** — `cmux-bash-integration.bash` and similar dotfiles
   touch `$PROMPT_COMMAND` (a var the launchd shell doesn't have). A `set -u` parent
   aborts on first access. Restore `set -u` after the block.
2. **`set +e` around the rc block, do NOT restore** — many user dotfiles run
   `set -o errexit`. A `set -e` parent re-enables errexit for the rest of the
   script, which is exactly what a self-healing supervisor design wants to avoid.
   The script's design intent IS that heal-cycle failures are logged, not fatal —
   leave errexit off for the rest of the supervisor.

```bash
set +u
set +e
for _rc in "$HOME/.bash_profile" "$HOME/.zprofile" "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [ -r "$_rc" ]; then
    # shellcheck disable=SC1090
    . "$_rc" >/dev/null 2>&1 || true
  fi
done
set -u
unset _rc
```

See: [[feedback-2026-06-09-runner-supervisor-and-ops]] (PR #7271, bead rev-5ysuv)

## bootout vs kickstart-k (2026-06-09 hermes outage)

`launchctl bootout` **permanently removes the service from the bootstrap domain**.
`KeepAlive` cannot restart a service that is no longer registered.

`launchctl kickstart -k` kills and restarts the process while keeping it registered —
KeepAlive remains active.

`hermes gateway stop` calls `bootout`. **Never call it without a follow-up `hermes gateway start`.**
`hermes gateway restart` internally calls `kickstart -k` — this is the correct command for
normal restarts (no plist change).

Recovery after bootout:
```bash
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/ai.hermes.prod.plist
launchctl kickstart "gui/$(id -u)/ai.hermes.prod"
```

See: [[hermes-gateway-bootout-outage-root-cause]] (bead jleechan-26bt, PR #473)

## template-commit-prevents-orphan (2026-06-10 dual-gateway incident)

`install-launchagents.sh` gates orphan-plist cleanup on the repo template existing:
```bash
[[ -f "$REPO_DIR/launchd/$label.plist" ]] || continue  # silently skips cleanup
```

When `launchd/ai.hermes.prod.plist` was never committed, cleanup skipped removing
`ai.hermes.gateway.plist` (orphan) on every deploy — two gateways ran for months.

**Rule**: commit the `@HOME@`-placeholder template to the owning repo **before** `launchctl bootstrap`.
`/launchd` skill Step 4 is mandatory.

`deploy.sh` Stage 1b adds belt-and-suspenders: unconditionally removes `ai.hermes.gateway`
and `com.hermes.gateway` regardless of installer state.

See: [[launchd-template-orphan-prevention]] (bead jleechan-xty2, commit `ae17c1bb28`)

## StartInterval silent death (2026-06-17)

Plists using `StartInterval=N` (with `RunAtLoad=true`, `KeepAlive=false`) can silently enter `state = not running, active count = 0` — the schedule stops firing with no error in any log. This was diagnosed via `launchctl print "gui/$(id -u)/<label>"` for `com.jleechan.mcp-daemon` on 2026-06-17, after 5+ minutes had passed without the expected re-fire.

**Recovery:** `launchctl unload <plist> && launchctl load -w <plist>` re-triggers `RunAtLoad`. The `load -w` flag persists the override.

**Durable prevention:** add `KeepAlive` (respawns on crash) or pair `StartInterval` with an external watchdog that runs `launchctl kickstart -k` if the script's last-log timestamp is too old. `StartInterval` alone is fragile because launchd can throttle or stop scheduling the job without surfacing an error.

**Diagnostic tell:** the daemon script's log (`StandardOutPath`/`StandardErrorPath`) shows the last successful run's `[ready]` line, but no subsequent `[starting ... v2]` line at the expected `StartInterval` boundary. There is no other log entry to indicate failure.

See: `sources/feedback-2026-06-17-mcp-daemon-diagnosis-fixes.md` (bead rev-gu8bi, closed) for the full incident writeup.
