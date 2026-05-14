# Hermes Gateway Recurring Failure Pattern

**Ingested:** 2026-05-13
**Source:** feedback_2026-05-13_hermes_gateway_troubleshooting_pattern.md
**Classification:** Critical

## Summary

Hermes gateway has experienced 9+ incidents across 4 distinct failure classes between 2026-04 and 2026-05. Each class has a known root cause, a verified fix, and a missing automated guard that would prevent recurrence.

## Failure Classes

1. **Launchd State Corruption** — `--replace` flag, zombie sessions in state.db, stale lock files
2. **Launchd Env Isolation** — API keys missing from launchd, `.env` overrides
3. **Duplicate Plist / Port Conflict** — Multiple plists with same HERMES_HOME
4. **Resource Exhaustion / WS Churn** — Event loop saturation from high concurrency

## Key Rules

- Never use `--replace` in plist ProgramArguments
- Always use `HERMES_HOME=~/.hermes_prod hermes gateway status`
- After non-graceful restart, close zombie sessions: `UPDATE sessions SET ended_at=now WHERE ended_at IS NULL`
- Route all env through `launchd-env-wrapper.sh`, delete `.env` files
- One plist per HERMES_HOME enforced by deploy.sh Stage 0

## Diagnostic Checklist

1. Process alive? `pgrep -fl "hermes gateway"`
2. Health check? `curl :8642/health`
3. CLI status with correct HOME? `HERMES_HOME=~/.hermes_prod hermes gateway status`
4. Draining? Check `gateway_state.json`
5. Zombie sessions? `SELECT COUNT(*) FROM sessions WHERE ended_at IS NULL`
6. Env vars present? `ps eww -p <PID> | grep SLACK_APP_TOKEN`
7. Messages processed? `grep "inbound message" agent.log`
8. Port holder correct? `lsof -i :8642`

## Related Concepts

- [[hermes-launchd-env-isolation]]
- [[hermes-gateway-draining-deadlock]]
- [[hermes-duplicate-plist-conflict]]
