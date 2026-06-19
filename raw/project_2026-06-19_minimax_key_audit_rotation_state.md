---
name: minimax-api-key-audit-rotation-state
description: MiniMax API key audit 2026-06-19 — sk-cp- working but 4-month leak; sk-api- candidate 402 no-balance; PR
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

# 2026-06-19 — MiniMax API Key Audit + Rotation State

## TL;DR

The MiniMax key currently in `~/.bashrc` as `MINIMAX_API_KEY` (`<minimax-api-key-redacted>`) **works** (HTTP 200, "Pong back! 🏓") but has been **publicly leaked for ~4 months**. A user-proposed replacement (`sk-api-FsxttkDk...`) is authentic but has zero credit (HTTP 402 insufficient_balance_error). User has chosen to leave the live key as-is for now ("seems fine"). The durable gap is **rotation discipline** — there is no automation that rotates a key when it appears in git history.

## Live key status (probed 2026-06-19)

| Key | Location | `/v1/models` (auth) | `/anthropic/v1/messages` (inference) | Status |
|---|---|---|---|---|
| `<minimax-api-key-redacted>` | `~/.bashrc` `MINIMAX_API_KEY` | ✅ HTTP 200 (M3, M2.7, M2.5, M2.1, M2 + highspeed) | ✅ HTTP 200 ("Pong back! 🏓") | **Live, works, leaked** |
| `sk-api-FsxttkDkINCgkMFNRxlr4Nwth46ZSOPkYZ-9HGpS_LmDfvvCplKyNlnQysQsiNUdTUBVtA2XTbo68qaFx8nIabnO53w3_23wQhfFTX6DtuWVet8mcEvzy_Q` | user paste 2026-06-19 | ✅ HTTP 200 (full model catalog) | ❌ HTTP 402 `insufficient_balance_error (1008)` | **Valid auth, no credit** |

## Leak timeline — `sk-cp-` key first appeared in public git history 2026-02-19

| Date | Commit | Author | Event |
|---|---|---|---|
| **2026-02-19 02:11:22** | `a853c71da8` | jleechan2015 | First leak — `chore: backup ~/.openclaw snapshot 20260219_021043` committed `auth.json` with the live key |
| 2026-03-13 17:55–22:09 | `a14c33f346` / `a8ae0ea7b2` / `4e57fa8855` | jleechan2015 / jleechan | Worktree debug fixes — key carried into multiple dev branches |
| **2026-03-14 13:40:43** | `f3a995553a` | jleechan2015 | **PR #135**: "fix: hardcode tokens directly in openclaw.json, eliminate all ${ENV_VAR} placeholders" — DELIBERATE HARDCODING commit (smoking gun) |
| **2026-04-11 22:46:52** | `3aac8fe80a` | jleechan@example.com | The 3aac8fe8 leak — refactor `~/.openclaw` → `~/.hermes` carries the key forward |
| 2026-04-11 22:46:58 | `f15d4d79de` | jleechan@example.com | First `.gitignore` for `openclaw.json` added (too late) |
| 2026-05-14 22:31 | `563fe71569` | jleechan2015 | PR #570 merged (openclaw→hermes rename migration) |
| 2026-06-09 01:16:31 | `d141c7b57b` | jleechan2015 | `auth.json` formally un-tracked from git |
| 2026-06-19 | (today) | n/a | Key still live in `~/.bashrc`, still works |

**Total exposure window: 2026-02-19 → 2026-06-19 = 4 months.**

**Currently NOT in `origin/main`** (gitignored + un-tracked since 2026-06-09), but in 35+ branches (`dev*`, `ai-orch-*`, `pr-*`, `auto/commit-pending`, all `openclaw` backup branches) and 5 git blobs (`55a203d2...`, `5de2791b...`, `9a71a4d1...`, `fdd2b0a9...`, `f1379920...`).

## PR #135 — the smoking gun

Commit `f3a995553a` (2026-03-14 13:40:43 -0700):
> "fix: hardcode tokens directly in openclaw.json, eliminate all ${ENV_VAR} placeholders"

The *intent* was a refactor to eliminate `${ENV_VAR}` placeholders (which break when env vars are undefined at runtime). The *result* was that the live `sk-cp-` key was committed to a **public repo** as a JSON literal. This is the same anti-pattern as `feedback_2026-05-12_provider_dual_registry.md` (consolidation done wrong) — a "fix" that hardcoded values where indirection would have been safer.

## API key probe methodology (READ-ONLY, no writes)

| Endpoint | Use | Interpret |
|---|---|---|
| `GET https://api.minimax.io/v1/models` | Auth check | 200 + model list = valid; 401/403 = revoked; 402 = valid but no quota |
| `POST https://api.minimax.io/anthropic/v1/messages` | Inference check (claudem path) | 200 = works; 402 `insufficient_balance_error (1008)` = valid auth, no quota; 404 = wrong endpoint |

**Critical**: `claudem()` wrapper uses `https://api.minimax.io/anthropic/v1/messages` (NOT `/v1/messages`, that 404s). Base URL stays `/anthropic` because Hermes/claudem append `/v1/messages` internally per `CLAUDE.md`.

```bash
# Auth check
curl -sS -m 10 "https://api.minimax.io/v1/models" \
  -H "Authorization: Bearer $KEY"

# Inference check (claudem path)
curl -sS -m 15 -X POST "https://api.minimax.io/anthropic/v1/messages" \
  -H "x-api-key: $KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","max_tokens":20,"messages":[{"role":"user","content":"Reply: pong"}]}'
```

## Other LLM keys in same leaked `auth.json` (NOT yet probed)

- OpenAI codex: OAuth JWT — refresh-token-rotation, not API key
- OpenRouter `<openrouter-api-key-redacted>` — leaked 2026-02-19, status unknown
- ZAI/GLM `<zai-glm-api-key-redacted>` — leaked 2026-02-19, status unknown
- Wafer `<wafer-api-key-redacted>` — leaked 2026-02-19, status unknown
- DeepSeek: same OpenRouter key (likely copy-paste)

## Groq key from 3aac8fe8 still valid (cross-ref Task #130)

`<groq-api-key-redacted>` — confirmed still valid 2026-06-18, full 17-model catalog returned. Needs user-side revocation at https://console.groq.com/keys (out of scope for autonomous session).

## Ubuntu box update — DECISION PENDING

`/linux` is a real slash command (`~/.claude/commands/linux.md` → `~/.claude/skills/linux-remote/SKILL.md`). SSH alias `jeff-ubuntu` → 192.168.254.128, user jleechan, key `~/.ssh/id_jeff_ubuntu`, Ubuntu 24.04.

User asked: "use /linux to update the bashrc for my ubuntu box" — deferred while deciding which key. Three options:

- **A — Mirror working `sk-cp-` to Ubuntu**: lowest risk, gives both machines working inference. The `sk-cp-` key is leaked anyway; one more mirror doesn't worsen the blast radius. Recommended.
- **B — Fresh key rotation, paste once, update both boxes**: cleanest security posture. Requires user to generate a new key in MiniMax console and paste it once.
- **C — Use `sk-api-FsxttkDk...` for Ubuntu only**: NOT viable, the key has no credit (402 on every inference call).

**As of 2026-06-19, Ubuntu bashrc update has NOT been executed.**

## Harness fix status (PRs #646 + #9 merged 2026-06-19T02:17Z)

The `Example/seed/test fixture credential discipline` rules shipped in both jleechanclaw and browserclaw:

- Pre-commit hook scans staged index via `git show :<path>` (not worktree) — covers `examples/` AND `docs/examples/`
- CI workflow `example-discipline.yml` runs `bash tests/test_example_placeholder_discipline.sh` on every PR push
- Global identity guard at `~/.claude/hooks/pre-commit-git-identity-example-com-guard.sh` blocks `@example.com` authors
- See `project_2026-06-19_credential_discipline_4th_admin_override.md` for merge details

**Would the new harness fix have caught the 2026-02-19 MiniMax leak? NO.** The leak was in `auth.json` (runtime config), not in `examples/` or `docs/examples/`. The discipline rules are scoped to example/seed/fixture files only. Tracked runtime config files (auth.json, openclaw.json, *.openclaw.json) are still not covered by any pre-commit hook.

**Gap**: Need a SECOND harness layer covering tracked config files (auth.json, `*.api-key`, `*-credentials.json`, openclaw.json, `secrets/**`). The current discipline rules do not extend to these paths. **Future PR scope: `tracked-config-credential-discipline` — extend scan to gitignored runtime config files + tracked credential JSON.**

## Task state (2026-06-19)

| Task | Status | Notes |
|---|---|---|
| #113 (SEC-1 GCP key rotation) | pending | LOW risk — controls locked down per #129 audit |
| #130 (SEC-3 3aac8fe8 audit) | pending | Groq key STILL VALID — user revocation needed |
| #131 (MiniMax leak source) | **completed** | PR #135 = smoking gun, full 4-month timeline documented |
| #132 (Test candidate key) | **completed** | `sk-api-FsxttkDk...` valid auth, 402 no-balance |

## Risk summary

| Risk | Key | Current status |
|---|---|---|
| 🔴 HIGH | `sk-cp-` (MiniMax) | 4-month leak window, still live, not rotated |
| 🔴 HIGH | `<groq-api-key-redacted>` (Groq from 3aac8fe8) | 2+ month leak window, still valid |
| 🟡 MEDIUM | `xapp-1-...` (Slack app) | Value matches 3aac8fe8 — may or may not have been rotated post-leak |
| 🟢 LOW | `AIzaSy...` (GCP/Firebase from 45836c8) | Controls locked down — near-zero exploitable value |
| ⚪ INFO | `sk-api-FsxttkDk...` (user paste) | Valid auth but 402 no-balance; treat as compromised due to chat log |

## Why

Future agents running on this machine will encounter the same `sk-cp-` key still in `~/.bashrc`. They need to know (1) it works but has been publicly leaked for 4 months, (2) the leak timeline so they can correlate with any anomalous activity, (3) the probe methodology so they can re-validate before each rotation, and (4) the deliberate-hardcode origin (PR #135) so they don't recreate the same anti-pattern.

## How to apply

- Before recommending `claudem()` work to a user: confirm `MINIMAX_API_KEY` in their bashrc is the `sk-cp-` value (or a freshly rotated replacement) and probe with `/v1/models` — if 200, proceed.
- If a user proposes a new MiniMax key, run the probe pattern in this file. **402 insufficient_balance_error means the key is real but the account has no credit** — do NOT swap it in.
- If the user rotates the key: update `~/.bashrc` on Mac AND `jeff-ubuntu` via `/linux` in one coordinated pass (option B above). Don't do partial updates.
- For new agents: never use `${ENV_VAR}` placeholder elimination as a reason to hardcode secrets (PR #135 anti-pattern). Indirection is the security primitive.
- Add `tracked-config-credential-discipline` to the next harness-fix iteration.

## Provenance

- Source: live shell probes 2026-06-19 + `git log --all -S "<minimax-api-key-redacted>` across `~/.hermes` repo
- Cross-ref: `project_2026-06-18_investigation_3aac8fe8_leak_commit.md` (3aac8fe8 specifics), `feedback_2026-06-18_real_history_over_gitleaksignore.md` (history-scrub vs revocation), `project_2026-06-19_credential_discipline_4th_admin_override.md` (PRs #646 + #9)
- claude.md policies invoked: "Example / seed / test fixture credential discipline", "Verify before reporting — no punting observable questions", "Real history over gitleaksignore"
