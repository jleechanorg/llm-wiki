---
name: hermes-gateway-troubleshooting-pattern
description: Recurring Hermes gateway failures follow 4 failure classes; diagnostic checklist and harness guards to prevent
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: ff29bf22-7f57-4c45-92d2-7990b6b3caec
---

# Hermes Gateway Recurring Failure Pattern (2026-04 to 2026-05)

Four distinct failure classes have caused repeated Hermes gateway outages. Each has a specific diagnostic and a missing harness guard.

## Failure Class 1: Launchd State Corruption (3 incidents)

**Symptoms:** Gateway process is alive, health check passes, Slack WS "connected", but zero messages processed.

**Root causes:**
- `--replace` flag in plist → gateway enters "draining for shutdown" deadlock (2026-05-13)
- Zombie sessions in `state.db` with `ended_at=NULL` → gateway sees "active agents" and blocks (91 sessions, 2026-05-13)
- Stale `gateway.lock` / `gateway.pid` with `start_time: null` → CLI reports wrong state

**Fix:**
1. Never use `--replace` in plist ProgramArguments (removed from `install.sh` line 583)
2. After any non-graceful restart, close zombie sessions: `UPDATE sessions SET ended_at=now, end_reason='gateway_restart' WHERE ended_at IS NULL`
3. Always use `HERMES_HOME=~/.hermes_prod hermes gateway status` — without it, CLI reads staging dir and reports wrong state

**Missing guard:** No automated check that zombie sessions don't accumulate. `doctor.sh` and `monitor-agent.sh` don't check `state.db` for `ended_at IS NULL`.

## Failure Class 2: Launchd Env Isolation (2 incidents)

**Symptoms:** Gateway starts but LLM calls fail with 401/403. Or: specific env vars silently undefined.

**Root causes:**
- Launchd doesn't source `.bashrc` → API keys from shell profile are missing at runtime
- `.env` files override `launchd-env-wrapper.sh` sourced tokens (2026-05-11)
- `MINIMAX_API_KEY` undefined in lifecycle-worker plist (2026-04-30)

**Fix:**
- Route ALL env through `launchd-env-wrapper.sh` (sources `.bash_profile` → `.bashrc`)
- Delete `.env` files in `HERMES_HOME` dirs — they silently override launchd wrapper
- Verify with `ps eww -p <PID> | grep MINIMAX_API_KEY` after any plist change

**Missing guard:** No automated check that gateway process has required env vars at runtime.

## Failure Class 3: Duplicate Plist / Port Conflict (2 incidents)

**Symptoms:** Gateway crashes on startup with "address already in use". Multiple instances compete for same port.

**Root causes:**
- `ai.hermes.gateway` + `ai.hermes.prod` with same `HERMES_HOME` (migration leftover, 2026-04-29)
- Staging + prod plists with same Slack bot token (2026-04-12)
- Orphan plists from incomplete uninstalls

**Fix:**
- `deploy.sh` Stage 0 enforces one plist per `HERMES_HOME`
- Staging uses separate Slack app (`A0APZAC659P`) and bot token
- Staging disabled between deploys: `launchctl disable gui/$U/ai.hermes-staging`

**Missing guard:** `doctor.sh` checks plist uniqueness but doesn't verify Slack app-token scope locks at `~/.local/state/hermes/gateway-locks/`.

## Failure Class 4: Resource Exhaustion → WS Churn (2 incidents)

**Symptoms:** `SlackWebSocket:N > 5` in logs, canary fails (rc=4), gateway becomes unresponsive.

**Root causes:**
- `timeoutSeconds × maxConcurrent > 3000` saturates event loop → WS pong starvation
- RAM exhaustion (load 84+) causes both gateways to crash (2026-05-13)

**Fix:**
- Approved values: `timeoutSeconds=600`, `maxConcurrent=10`, `subagents.maxConcurrent=10`
- Disable staging between deploys to reduce RAM contention
- `doctor.sh` enforces exact-match for protected keys

**Missing guard:** No alert when system load exceeds threshold. No automated restart when `SlackWebSocket:N > 5`.

## Diagnostic Checklist (for any "Hermes not responding" report)

1. `pgrep -fl "hermes gateway"` — is the process alive?
2. `curl -s -m 5 http://127.0.0.1:8642/health` — does it respond?
3. `HERMES_HOME=~/.hermes_prod hermes gateway status` — what does the CLI report? (NOT bare `hermes gateway status`)
4. `cat ~/.hermes_prod/gateway_state.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['gateway_state'], d['active_agents'], d['platforms']['slack']['state'])"` — is it draining?
5. `python3 -c "import sqlite3; c=sqlite3.connect('$HOME/.hermes_prod/state.db'); print(c.execute('SELECT COUNT(*) FROM sessions WHERE ended_at IS NULL').fetchone()[0], 'zombie sessions')"` — zombie session count
6. `ps eww -p <PID> | grep SLACK_APP_TOKEN` — does the process have the Slack token?
7. `grep "inbound message" ~/.hermes_prod/logs/agent.log | tail -3` — any messages processed at all?
8. `lsof -i :8642` — who holds the port? Does PID match gateway?

## References

- [[feedback-2026-05-13-hermes-replace-flag]] — --replace deadlock
- [[feedback-2026-05-13-staging-disabled]] — staging resource contention
- [[feedback-2026-05-12-plist-uniqueness]] — duplicate plist conflicts
- [[feedback-2026-05-11-env-override-root-cause]] — .env override
- [[feedback-2026-04-30-launchd-env-isolation]] — env isolation
