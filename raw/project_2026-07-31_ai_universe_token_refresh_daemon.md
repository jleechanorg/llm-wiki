---
name: ai-universe-auth-refresh-daemon-launchd-never-expire-unless-google-password-changes
description: "2026-07-31 — `org.jleechanorg.auth-aiuniverse-token-refresh` launchd agent runs `auth-cli.mjs refresh` every 30 min, keeps Firebase refreshToken inside its sliding 30-day window so `/secondo` never asks for browser re-login unless the user changes their Google password"
metadata: 
  node_type: memory
  type: project
  bead: rev-eboni
  originSessionId: 2646dc53-9580-4545-943b-7c345e44c27f
  modified: 2026-07-31T11:20:26.113Z
---

## Context

Firebase user-auth tokens cannot be made literally "never expire":
- **idToken**: 1 hour (hard security policy, not configurable)
- **refreshToken**: ~30 days sliding (rotated on every use, invalidated on password change / sign-out-everywhere / account disable)

Identity Platform session cookies max at 14 days and have no console override above that. Service-account auth is a dead-end for AI Universe specifically — live probe of the Cloud Run MCP backend with a Google OAuth access token minted from `firebase-adminsdk-fbsvc@ai-universe-b3551.iam.gserviceaccount.com` returned `HTTP 401 Authentication failed` because the backend uses Firebase Admin SDK `verifyIdToken` which rejects Google OAuth access tokens.

The remaining option is to **keep the refresh token sliding indefinitely** by calling `auth-cli.mjs refresh` regularly. A launchd daemon fires every 30 minutes — well under the 1-hour idToken TTL — so:
- Any MCP call always sees a token ≤ 30 min old
- The refresh token is rotated ~48×/day, which keeps it well inside the 30-day absolute window
- The only way the chain breaks is: Mac off for 30+ days, or user changes Google password, or admin revokes sessions — all of which require explicit human action and match the user's "never expire unless I change Google password" requirement.

## Why

User wanted `/secondo` to never prompt for browser re-login. With this daemon, the prompt only fires when the user changes their Google password (or after 30+ days of Mac uptime with no daemon activity — extremely unlikely).

**How to apply:** Future agents who see `/secondo` requests for browser re-login should first check whether this daemon is running (`launchctl list | grep auth-aiuniverse-token-refresh`) before recommending manual browser OAuth.

## Deployment

| Component | Path |
|---|---|
| Plist template (owning repo) | `/Users/jleechan/.hermes/launchd/org.jleechanorg.auth-aiuniverse-token-refresh.plist.template` |
| Rendered plist | `/Users/jleechan/.hermes/launchd/org.jleechanorg.auth-aiuniverse-token-refresh.plist` |
| LaunchAgents symlink | `/Users/jleechan/Library/LaunchAgents/org.jleechanorg.auth-aiuniverse-token-refresh.plist` |
| Wrapper script | `/Users/jleechan/.local/libexec/auth-aiuniverse/refresh_token.sh` |
| Log | `/Users/jleechan/.local/state/auth-aiuniverse/refresh-token.log` |

## Cadence

`StartInterval=1800` (30 min), `RunAtLoad=true`. The 30-min cadence was chosen because:
- It's well under the 1-hour idToken TTL → any tool call always sees a fresh token
- 48 refreshes/day is negligible Firebase API cost (no rate-limit concern for one user)
- A 50-min cadence would also work, but 30 min gives a safety margin in case launchd skips a tick

## Wrapper script pattern (sourced from `~/.claude/skills/launchd/SKILL.md`)

```bash
#!/usr/bin/env bash
set -euo pipefail
if [[ -f ~/.bashrc ]]; then
  set +u
  source ~/.bashrc 2>/dev/null || true
  set -u
fi
if [[ -z "${VITE_AI_UNIVERSE_FIREBASE_API_KEY:-}" ]]; then
  echo "FATAL: VITE_AI_UNIVERSE_FIREBASE_API_KEY is not set after sourcing ~/.bashrc" >&2
  exit 2
fi
exec /usr/bin/env node /Users/jleechan/.claude/scripts/auth-cli.mjs refresh
```

Notes:
- `set +u` / `set -u` wrap around the `source` to prevent launchd aborts from unbound optional variables in `~/.bashrc`.
- The `VITE_AI_UNIVERSE_FIREBASE_API_KEY` defense-in-depth check is critical — some shells skip bashrc exports in non-interactive contexts (we hit this on jeff-ubuntu, see memory `feedback_2026-07-31_ai_universe_mcp_render_to_cloudrun_migration.md`). On mac it works because launchd runs as the user with a login-style env, but the explicit guard prevents silent failures if bashrc is later modified.
- `auth-cli.mjs refresh` (line ~592) is daemon-safe: no interactive prompts, fails loud with exit 1 if the refresh token is invalid, daemon just retries on the next tick.

## Install protocol (per launchd SKILL.md)

```bash
PLIST_SRC="/Users/jleechan/.hermes/launchd/org.jleechanorg.auth-aiuniverse-token-refresh.plist"
LABEL="org.jleechanorg.auth-aiuniverse-token-refresh"
/bin/launchctl bootout "gui/$(/usr/bin/id -u)/${LABEL}" 2>/dev/null || true
/bin/launchctl bootstrap "gui/$(/usr/bin/id -u)" "$PLIST_SRC"
/bin/launchctl list | grep "$LABEL"
```

Use `bootout` / `bootstrap` (modern), NOT `load` / `unload` (deprecated).

## Verification

```
$ /bin/launchctl list | grep auth-aiuniverse-token-refresh
-       0       org.jleechanorg.auth-aiuniverse-token-refresh

$ cat /Users/jleechan/.local/state/auth-aiuniverse/refresh-token.log
🔄 Refreshing authentication token...
✅ Token refreshed successfully!
   User: Jeff L (jleechantest@gmail.com)
   New expiration: 7/31/2026, 5:19:18 AM

$ node ~/.claude/scripts/auth-cli.mjs status
   Status: ✅ VALID
   Expires: 7/31/2026, 5:19:18 AM
```

PID 0 (just-launched, exited cleanly); daemon re-fires every 1800s.

## Failure modes

| Failure | Effect | Recovery |
|---|---|---|
| Mac off for 30+ days | refreshToken inactivity expiry → next MCP call gets HTTP 401 | Daemon catches up on next boot; if it fails too, user must browser-re-login via `auth-cli.mjs login` |
| Google password changed | refreshToken immediately invalidated by Firebase | Browser re-login required (matches user's stated requirement) |
| `~/.bashrc` modified and `VITE_AI_UNIVERSE_FIREBASE_API_KEY` unset | Wrapper script exits 2 with FATAL message | Daemon retries every 30 min; once bashrc is fixed, next tick succeeds |
| User signs out everywhere | refreshToken invalidated | Browser re-login |
| `auth-cli.mjs refresh` returns non-zero | Wrapper exits 1, daemon logs error | Daemon retries next tick; the 30-min cadence means up to 30 min of stale tokens |

## Related

- Memory: `feedback_2026-07-31_ai_universe_mcp_render_to_cloudrun_migration.md` (the migration that exposed this requirement)
- Memory: `feedback_2026-07-31_ai_universe_mcp_render_to_cloudrun_migration.md` (jeff-ubuntu bashrc env var issue — same root cause as the wrapper's defense-in-depth check)
- Skill: `~/.claude/skills/launchd/SKILL.md` (clean re-install protocol, sourced shell profile sourcing, plist template)
- Skill: `~/.claude/skills/launchd-plist-template/SKILL.md` (owning repo rule, `@HOME@` placeholders)
- Bead: `rev-eboni` (WorldAI MCP URL follow-up — separate daemon may be needed if `--project worldarchitecture-ai` is used regularly)
- Research: `/Users/jleechan/projects/worktree_fable_bulk_restored/docs/research/firebase-token-never-expire-2026-07-31.md` (full primary-source investigation)
- Precedent: `org.jleechanorg.ezgha-token-refresh.plist` (same pattern, different auth — GitHub App token refresh)