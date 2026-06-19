---
title: "MiniMax API key audit + rotation state — 2026-06-19"
type: source
tags: [security, credentials, MiniMax, leak, rotation, PR-135, PR-646, PR-9]
date: 2026-06-19
source_file: project_2026-06-19_minimax_key_audit_rotation_state.md
last_updated: 2026-06-19
---

## Summary

The MiniMax API key currently in `~/.bashrc` (`<minimax-api-key-redacted>`) **works** (HTTP 200) but has been **publicly leaked for ~4 months** via PR #135 (commit `f3a995553a`, 2026-03-14) which deliberately hardcoded `${ENV_VAR}` placeholders to JSON literals in `auth.json`. A user-proposed replacement (`sk-api-FsxttkDk...`) is authentic but has zero credit (HTTP 402). The durable gap is **rotation discipline** — there is no automation that rotates a key when it appears in git history.

## Key Claims

- `sk-cp-` (live) works but has 4-month leak window (2026-02-19 → 2026-06-19)
- `sk-api-FsxttkDk...` (user-pasted) is authentic, full model catalog visible, but 402 insufficient_balance_error on inference
- PR #135 commit `f3a995553a` is the smoking gun — "fix: hardcode tokens directly in openclaw.json, eliminate all ${ENV_VAR} placeholders" deliberately inlined the live key
- The 2026-02-19 leak (commit `a853c71da8`) preceded 3aac8fe8 by ~2 months and seeded the leak across `openclaw.json` → `auth.json` refactor
- The credential-discipline harness fix (PRs #646 + #9) does NOT cover runtime config files (auth.json, openclaw.json) — only `examples/` and `docs/examples/`. A second harness layer is needed.

## Key Quotes

> "fix: hardcode tokens directly in openclaw.json, eliminate all ${ENV_VAR} placeholders" — commit `f3a995553a` (PR #135, 2026-03-14 13:40:43)

> "Total exposure window: 2026-02-19 → 2026-06-19 = 4 months."

> "Would the new harness fix have caught the 2026-02-19 MiniMax leak? NO. The leak was in `auth.json` (runtime config), not in `examples/` or `docs/examples/`."

## Connections

- [[PR-135-MiniMax-Hardcode-Leak]] — the deliberate-hardcode commit (smoking gun)
- [[MiniMax-API-Key-Probe-Methodology]] — read-only probe pattern
- [[jeffrey-oracle]] — user identity (jeffrey = jleechan); context for who leaked the key
- [[Hermes-AO-MiniMax-Worker-Architecture]] — `claudem()` and `ao minimax` worker paths
- [[3aac8fe8-leak-commit-investigation]] — the related openclaw→hermes refactor that carried the key forward
- [[Credential-Discipline-4th-Admin-Override-Merge]] — PRs #646 + #9 merged 2026-06-19T02:17Z (same harness fix class, same day)
- [[Auth-File-Discipline-Harness-Gap]] — second harness layer needed (tracked-config-credential-discipline)

## Probe Methodology (READ-ONLY, no writes)

| Endpoint | Use | Interpret |
|---|---|---|
| `GET https://api.minimax.io/v1/models` | Auth check (free, no quota) | 200 + model list = valid; 401/403 = revoked; 402 = valid auth no quota; 404 = wrong endpoint |
| `POST https://api.minimax.io/anthropic/v1/messages` | Inference check (claudem path) | 200 = works; 402 = no quota; 404 = wrong endpoint |

**Critical**: `claudem()` wrapper uses `https://api.minimax.io/anthropic/v1/messages` (NOT `/v1/messages`). Base URL stays `/anthropic` because Hermes/claudem append `/v1/messages` internally.

## Live Key Status (probed 2026-06-19)

| Key | `/v1/models` (auth) | `/anthropic/v1/messages` (inference) | Status |
|---|---|---|---|
| `<minimax-api-key-redacted>` (`~/.bashrc` `MINIMAX_API_KEY`) | ✅ HTTP 200 (M3, M2.7, M2.5, M2.1, M2 + highspeed) | ✅ HTTP 200 ("Pong back! 🏓") | **Live, works, leaked** |
| `sk-api-FsxttkDk...` (user paste 2026-06-19) | ✅ HTTP 200 (full catalog) | ❌ HTTP 402 insufficient_balance_error | **Valid auth, no credit** |

## Leak Timeline

| Date | Commit | Event |
|---|---|---|
| **2026-02-19 02:11:22** | `a853c71da8` | First leak — `chore: backup ~/.openclaw snapshot` committed `auth.json` with live key |
| 2026-03-13 17:55–22:09 | `a14c33f346` / `a8ae0ea7b2` / `4e57fa8855` | Worktree debug fixes — key carried into dev branches |
| **2026-03-14 13:40:43** | `f3a995553a` | **PR #135**: "hardcode tokens directly in openclaw.json" — DELIBERATE HARDCODING |
| **2026-04-11 22:46:52** | `3aac8fe80a` | openclaw→hermes refactor carries key forward |
| 2026-04-11 22:46:58 | `f15d4d79de` | First `.gitignore` for `openclaw.json` added (too late) |
| 2026-05-14 22:31 | `563fe71569` | PR #570 merged (openclaw→hermes rename) |
| 2026-06-09 01:16:31 | `d141c7b57b` | `auth.json` formally un-tracked from git |
| 2026-06-19 | (today) | Key still live in `~/.bashrc`, still works |

**Currently NOT in `origin/main`** (gitignored + un-tracked since 2026-06-09), but in 35+ branches and 5 git blobs (`55a203d2...`, `5de2791b...`, `9a71a4d1...`, `fdd2b0a9...`, `f1379920...`).

## Other LLM Keys in Same Leaked `auth.json` (NOT yet probed)

- OpenAI codex: OAuth JWT — refresh-token-rotation, not API key
- OpenRouter `<openrouter-api-key-redacted>` — leaked 2026-02-19, status unknown
- ZAI/GLM `<zai-glm-api-key-redacted>` — leaked 2026-02-19, status unknown
- Wafer `<wafer-api-key-redacted>` — leaked 2026-02-19, status unknown
- DeepSeek: same OpenRouter key (likely copy-paste)
- Groq `<groq-api-key-redacted>` — STILL VALID (confirmed 2026-06-18) — needs user-side revocation at https://console.groq.com/keys

## Ubuntu bashrc Update — DECISION PENDING

`/linux` is a real slash command (`~/.claude/commands/linux.md` → `~/.claude/skills/linux-remote/SKILL.md`). SSH alias `jeff-ubuntu` → 192.168.254.128, user jleechan, key `~/.ssh/id_jeff_ubuntu`, Ubuntu 24.04.

Three options for which key to mirror to Ubuntu:
- **A** — Mirror working `sk-cp-` to Ubuntu (recommended, lowest risk)
- **B** — Fresh key rotation on both boxes (requires user to generate new key)
- **C** — Use `sk-api-FsxttkDk...` for Ubuntu only — NOT viable, 402 on every call

**As of 2026-06-19, Ubuntu bashrc update has NOT been executed.**

## Harness Gap Identified

The credential-discipline harness fix (PRs #646 + #9 merged 2026-06-19T02:17Z) covers `examples/` and `docs/examples/` only. It would NOT have caught the 2026-02-19 MiniMax leak (which was in `auth.json`). Tracked runtime config files (`auth.json`, `*.api-key`, `*-credentials.json`, `openclaw.json`) still have no pre-commit hook coverage.

**Future PR scope**: `tracked-config-credential-discipline` — extend scan to gitignored runtime config files + tracked credential JSON.

## Risk Summary

| Risk | Key | Current status |
|---|---|---|
| 🔴 HIGH | `sk-cp-` (MiniMax) | 4-month leak window, still live, not rotated |
| 🔴 HIGH | `<groq-api-key-redacted>` (Groq from 3aac8fe8) | 2+ month leak window, still valid |
| 🟡 MEDIUM | `xapp-1-...` (Slack app) | Value matches 3aac8fe8 — may or may not have been rotated post-leak |
| 🟢 LOW | `AIzaSy...` (GCP/Firebase from 45836c8) | Controls locked down — near-zero exploitable value |
| ⚪ INFO | `sk-api-FsxttkDk...` (user paste) | Valid auth but 402 no-balance; treat as compromised due to chat log |

## Provenance

- Source: live shell probes 2026-06-19 + `git log --all -S "<minimax-api-key-redacted>` across `~/.hermes` repo
- Cross-ref: `project_2026-06-18_investigation_3aac8fe8_leak_commit.md` (3aac8fe8 specifics), `feedback_2026-06-18_real_history_over_gitleaksignore.md` (history-scrub vs revocation), `project_2026-06-19_credential_discipline_4th_admin_override.md` (PRs #646 + #9)
- claude.md policies invoked: "Example / seed / test fixture credential discipline", "Verify before reporting", "Real history over gitleaksignore"