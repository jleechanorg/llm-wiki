---
name: Doctor.sh must tolerate minimal hermes.json configs
description: When hermes_prod/hermes.json has only channels+gateway sections, doctor.sh cascaded 14 FAILs because it expected agents.defaults/plugins/models sections. Fix: live_json_has_agents guard.
type: feedback
bead: orch-7m3l
---

## Context

Hermes prod config (`~/.hermes_prod/hermes.json`) is minimal — only `channels` and `gateway` sections. The gateway works fine on Slack because it uses built-in defaults at runtime. But doctor.sh reads the file, finds valid JSON, sets `live_json_ok=1`, then runs ALL deep invariant checks which all FAIL on empty strings.

## Technical detail

The guard at line 702 only skipped checks when `hermes.json` didn't exist AND label was `ai.hermes.prod`. When the file exists (even minimal), all checks run and fail.

8 FAILs from missing `agents.defaults` section alone: primary model, maxConcurrent, subagents.maxConcurrent, timeoutSeconds, workspace, mem0 embedder, heartbeat config (every/target/prompt), heartbeat runtime parse.

## Solution

1. **`live_json_has_agents` variable** — after `live_json_ok=1`, check `jq -e '.agents' hermes.json`. When 0, skip deep checks with pass message "env-defaults install".
2. **Slack channels."*" absent** — when wildcard config entirely missing, PASS with "Hermes defaults to listen-all" instead of FAIL on missing keys.
3. **Gateway token** — minimal config with `live_json_has_agents=0` takes the env-token install pass path.
4. **Heartbeat runtime** — `fail` → `warn` when `hermes status --json` can't parse (gateway healthy via curl).
5. **Port 18789 → 8642** — the prod port migrated from legacy 18789 to 8642. All scripts, tests, and config now use 8642.

## Verification

- `scripts/doctor.sh`: 14 FAILs → 0 FAILs (77 pass, 4 warn, 0 fail)
- `pytest`: 18 failures → 0 against minimal config (95 passed, 94 skipped)
- Gateway health: `curl -s http://localhost:8642/health` returns `{"status":"ok"}`

## References

- PR [#580](https://github.com/jleechanorg/jleechanclaw/pull/580) — merged 2026-05-18
- Beads: orch-7m3l, orch-g8hs, orch-2dst (all closed)

## Reusable pattern

**Minimal config detection pattern**: When a config file may be partial (only essential sections), always check for the presence of key sections before asserting their contents. Empty string from `jq` is not an error — it's a signal that defaults are in use. Guard pattern:

```bash
live_json_has_agents=0
if [[ "$live_json_ok" -eq 1 ]] && jq -e '.agents' "$cfg" >/dev/null 2>&1; then
  live_json_has_agents=1
fi
```
