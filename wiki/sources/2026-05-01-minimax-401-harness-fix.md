---
title: "Minimax 401 Harness Fix — 2026-05-01"
type: source
tags: [agent-orchestrator, launchd, minimax, auth, skeptic]
date: 2026-05-01
source_file: roadmap/nextsteps-2026-05-01-minimax-401-harness-fix.md
---

## Summary
Root cause of recurring MiniMax 401 auth failures in AO workers was identified and fixed. The sed substitutions for `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `MINIMAX_ANTHROPIC_BASE_URL` were missing from `setup-launchd.sh` — causing launchd to pass literal `@MINIMAX_API_KEY@` strings (expanded to empty by bash) to workers. A subsequent architectural refactor superseded the substitution approach with `launchd-launcher.sh` which sources secrets from the shell profile at runtime.

## Key Claims
- `setup-launchd.sh` was missing 4 sed substitution lines for MINIMAX env vars
- The installed plist had literal `@MINIMAX_API_KEY@` which bash expanded to empty string → 401 on every MiniMax API call
- Commit `893fae999` only added a verification call, not the actual substitution lines — making it look fixed when it wasn't
- The `launchd-launcher.sh` approach eliminates the entire substitution approach: secrets flow from shell profile via `bash -ic 'declare -x'` filtering
- PR #514 fixed the skeptic `--trigger-type cron` bug (CLI flag passed but never implemented)
- All 3 original requirements verified: npm binary, script launchd, skeptic on PR #6748

## Key Quotes
> "PR #510 was APPROVED with all checks green but was never actually merged (merged: false)." — context explaining why the same pattern recurred
> "The sed substitutions for MINIMAX_API_KEY... were missing from setup-launchd.sh" — root cause
> "This eliminates the need for plists to duplicate secrets via sed substitution." — launchd-launcher.sh design goal

## Connections
- [[launchd-lifecycle-worker]] — the service this fix repairs
- [[minimax-401]] — the recurring auth failure pattern
- [[skeptic-trigger-type-bug]] — PR #514 fixing the unsupported CLI flag
- [[ao-cli-path-fork]] — the two-layer binary resolution mismatch
- [[jleechanorg/agent-orchestrator]] — the repo containing all affected code

## Fix Chain
| Problem | Fix | PR/Commit |
|---|---|---|
| MiniMax 401 (sed gap) | Add substitutions | #510 (merged) then superseded by launcher.sh |
| launchd missing | Consolidated `ai.agento.lifecycle-all.plist` | multiple commits |
| skeptic `--trigger-type` | Remove unsupported CLI flag | #514 (merged) |
| AO_CLI_PATH fork mismatch | Set `AO_CLI_PATH` env var in plist | #510 (merged) |
| @VAR@ harness gap | Add fail-fast check to test-launchd-env.sh | #512 (OPEN) |

## Key Files
- `scripts/launchd-launcher.sh` — sources shell profile via `bash -ic 'declare -x'`
- `scripts/setup-launchd.sh` — generates plist from template
- `scripts/start-all.sh` — `_ao_bin()` uses global npm `command -v ao`
- `packages/core/src/skeptic-reviewer.ts` — `--trigger-type` removed line 145
