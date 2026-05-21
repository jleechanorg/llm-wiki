---
name: plist-template-drift-anti-pattern
description: "Plist templates drift silently when: (1) placeholder names not in setup-launchd.sh's sed substitution list, (2) installed plists have no repo template, (3) vars sourced from .bashrc land after the interactive guard"
metadata: 
  node_type: memory
  type: feedback
  bead: orch-oxdm
  originSessionId: 8740d484-1020-4e44-a28f-13a5a1a2eddd
---

# Plist Template Drift Anti-Pattern

Discovered 2026-05-19 during deep audit of all Hermes launchd jobs. Three classes of silent breakage — each invisible until the service fails at runtime.

## Class 1: Unrecognized placeholder syntax

`setup-launchd.sh`'s `_install_plist()` only substitutes exactly 4 placeholders:

| Placeholder | Value |
|---|---|
| `@HOME@` | `$HOME` |
| `@HERMES_BIN@` | resolved hermes binary path |
| `@REPO_ROOT@` | `$HERMES_REPO` (= `~/.hermes`) |
| `@HERMES_EXTRA_PATH@` | empty string (stripped) |

Any other placeholder format — `@NODE_BIN_DIR@`, `__HOME__`, `${HOME}` — is silently left as a literal string in the installed plist. The service loads with the literal placeholder as a path, fails at runtime.

**Broken files found:**
- `ai.hermes.lifecycle-manager.plist.template` used `@NODE_BIN_DIR@` in PATH → PATH was literal `@NODE_BIN_DIR@:/usr/local/bin:...` → `ao` binary not found at runtime
- `com.hermes.mem0-watchdog.plist` used `__HOME__` (double-underscore format) → StandardOutPath was literal `__HOME__/.hermes/logs/...` → log file never created

**Fix:** Only use the 4 recognized `@UPPER_CASE@` placeholders. Never invent new ones without adding the corresponding `sed -e` line to `_install_plist()`.

## Class 2: Orphaned installed plists (no repo template)

3 plists were installed in `~/Library/LaunchAgents/` with hardcoded `/Users/jleechan/` paths but had no corresponding template in `~/.hermes/launchd/`:

- `ai.hermes.ao-notifier.plist` → script path hardcoded
- `ai.hermes.schedule.gh-actions-cost-monitor.plist` → hardcoded home
- `ai.hermes.schedule.spend-alert-daily.plist` → hardcoded home

These plists **cannot be re-installed** by any automation — they only exist in LaunchAgents. On a fresh machine, they'd be missing. On a re-install, `setup-launchd.sh --apply` would skip them.

**Fix:** Every installed plist MUST have a corresponding `.plist.template` in `~/.hermes/launchd/` and be listed in `CORE_PLISTS` or `SCHEDULE_PLISTS` in `setup-launchd.sh`. Audit with:

```bash
diff <(ls ~/Library/LaunchAgents/ | grep ai.hermes | sort) \
     <(ls ~/.hermes/launchd/ | sed 's/\.template$//' | sort)
```

## Class 3: MINIMAX vars behind .bashrc interactive guard

`~/.bashrc` has an interactive guard at line 283:
```bash
case $- in
  *i*) ;;
  *) return ;;
esac
```

`MINIMAX_API_KEY` and `MINIMAX_BASE_URL` are exported at line 894 — **after** the guard. They never reach launchd processes via normal `.bash_profile` → `.bashrc` chain.

**`_extract_bashrc_var` pattern** (added to `launchd-env-wrapper.sh`):
```bash
_extract_bashrc_var() {
  local var="$1"
  [ -n "${!var:-}" ] && return  # skip if already set
  local val
  val=$(grep -m1 "^export ${var}=" "$HOME/.bashrc" 2>/dev/null \
    | sed "s/^export ${var}=//;s/^['\"]//;s/['\"]$//" \
    | tr -d '\n')
  [ -n "$val" ] && export "$var=$val"
}
_extract_bashrc_var MINIMAX_API_KEY
_extract_bashrc_var MINIMAX_BASE_URL
_extract_bashrc_var ANTHROPIC_API_KEY
_extract_bashrc_var OPENAI_API_KEY
```

This greps the raw file rather than sourcing it, bypassing the guard entirely.

**Root fix (user action needed):** Move `MINIMAX_API_KEY` and `MINIMAX_BASE_URL` from line 894 to before line 283 in `.bashrc`, next to the other "before interactive guard" exports at line 267.

## Class 4: `source .bashrc` inside bash -c in ProgramArguments

Lifecycle-manager plist had:
```xml
<string>/bin/bash</string>
<string>-c</string>
<string>source @HOME@/.bashrc
# ... script ...</string>
```

This fails for the same interactive guard reason — and additionally, `source` is a bash builtin that's only reliable in bash, not `/bin/sh`. The `bash -c` is spawned as a non-interactive shell.

**Fix:** Use `launchd-env-wrapper.sh` as the ProgramArguments entry point, then call `bash -c`:
```xml
<string>/bin/bash</string>
<string>@REPO_ROOT@/scripts/launchd-env-wrapper.sh</string>
<string>/bin/bash</string>
<string>-c</string>
<string># ... script without source .bashrc ...</string>
```

## deploy.sh race conditions found and fixed

- **`sleep 1` after bootout** → `sleep 3`: bootout is async; port binding on 8642 isn't released for ~2s. Bootstrap with `sleep 1` → service tries to bind already-occupied port → crash-loop.
- **Stage 0 partial auto-disable**: Only `ai.hermes.gateway` was auto-renamed to `.disabled`; other duplicate labels left on disk → re-loaded on next login/reboot → port conflict. Fixed to auto-disable ALL non-canonical duplicates.
- **Missing plist existence check before bootstrap**: `launchctl bootstrap` error when plist file missing is cryptic. Added explicit check + `die`.
- **Missing `mkdir -p logs` before bootstrap**: Gateway crashes immediately on startup if logs dir doesn't exist.

## Reusable pattern: Plist template audit command

```bash
# Find installed plists with no corresponding repo template:
diff \
  <(ls ~/Library/LaunchAgents/ | grep -E "^(ai\.hermes|com\.hermes)" | sed 's/\.disabled$//' | sort -u) \
  <(ls ~/.hermes/launchd/ | sed 's/\.template$//' | sort -u)

# Find templates with unrecognized placeholders:
grep -r "@[A-Z_]*@" ~/.hermes/launchd/*.template \
  | grep -v "@HOME@\|@HERMES_BIN@\|@REPO_ROOT@\|@HERMES_EXTRA_PATH@"
```

## References

- PR [#584](https://github.com/jleechanorg/jleechanclaw/pull/584) — merged 2026-05-19
- Commits: `ab684908be`, `c9ec204d68`, `0c68b9c094` on `fix/setup-launchd-dryrun`
- Files fixed: `scripts/setup-launchd.sh`, `scripts/deploy.sh`, `scripts/launchd-env-wrapper.sh`, `launchd/ai.hermes-staging.plist`, `launchd/ai.hermes.lifecycle-manager.plist.template`, `launchd/com.hermes.mem0-watchdog.plist`
- Files created: `launchd/ai.hermes.ao-notifier.plist.template`, `launchd/ai.hermes.schedule.gh-actions-cost-monitor.plist.template`, `launchd/ai.hermes.schedule.spend-alert-daily.plist.template`, `launchd/ai.hermes-mem0-server.plist.template`
- [[hermes-launchd-meta-pattern]], [[feedback-2026-04-30-launchd-env-isolation]]
