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
