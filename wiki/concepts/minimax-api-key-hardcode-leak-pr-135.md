---
title: "MiniMax API key hardcode leak (PR #135)"
type: concept
tags: [security, credentials, MiniMax, leak, hardcode, anti-pattern, PR-135, indirection]
sources: [project-2026-06-19-minimax-key-audit-rotation-state, feedback-2026-06-19-minimax-key-probe-methodology, project-2026-06-18-investigation-3aac8fe8-leak-commit]
last_updated: 2026-06-19
---

## Description

PR #135 commit `f3a995553a` (2026-03-14 13:40:43 -0700) titled "fix: hardcode tokens directly in openclaw.json, eliminate all ${ENV_VAR} placeholders" deliberately inlined the live MiniMax API key (`sk-cp-Rg64V...`) into a JSON literal in a **public repo**. The intent was a refactor to eliminate `${ENV_VAR}` placeholders (which break when env vars are undefined at runtime). The result was a 4-month public leak (2026-02-19 first appearance → 2026-06-19).

## The anti-pattern

**"Eliminate indirection to fix a placeholder-resolution bug"** is a common but dangerous refactor pattern. Indirection is the security primitive — when `${ENV_VAR}` placeholders resolve at runtime, the actual secret never appears in source control. Hardcoding the resolved value into a JSON literal strips that indirection.

When you encounter `${ENV_VAR}` placeholders that fail to resolve, the fix is **never** to inline the resolved value. The fix is:
1. Investigate why the env var is unset (wrapper not sourced? dotfile path wrong?)
2. Add a default value or a fallback resolver
3. Use a secret manager (Vault, AWS Secrets Manager, macOS keychain)
4. Add a CI check that the placeholder is replaced before deploy, NOT before commit

## Leak chain

1. **2026-02-19** `a853c71da8` — `chore: backup ~/.openclaw snapshot 20260219_021043` first committed `auth.json` with the live key
2. **2026-03-13** `a14c33f346` / `a8ae0ea7b2` / `4e57fa8855` — worktree debug fixes carried the key forward
3. **2026-03-14** `f3a995553a` — **PR #135 deliberate hardcode** (smoking gun)
4. **2026-04-11** `3aac8fe80a` — openclaw→hermes refactor carried the key
5. **2026-04-11** `f15d4d79de` — first `.gitignore` for `openclaw.json` (too late)
6. **2026-05-14** `563fe71569` — PR #570 openclaw→hermes rename migration merged
7. **2026-06-09** `d141c7b57b` — `auth.json` formally un-tracked from git
8. **2026-06-19** — key still live in `~/.bashrc`, still works

The key currently resides in 35+ branches (dev*, ai-orch-*, pr-*, auto/commit-pending, all openclaw backup branches) and 5 git blobs (`55a203d2...`, `5de2791b...`, `9a71a4d1...`, `fdd2b0a9...`, `f1379920...`).

## Connections

- [auth-file-discipline-harness-gap](auth-file-discipline-harness-gap.md) — second-layer harness fix needed for tracked runtime config
- [[credential-discipline-drive-4th-admin-override-merge]] — same-day companion PRs #646 + #9 (covers examples/, NOT auth.json)
- [[feedback-2026-05-12-provider-dual-registry]] — same anti-pattern class: consolidation done wrong (dual registry → 401)
- [[claudem-macos-minimax-m3]] — the wrapper that consumes the leaked key
- [jeffrey-oracle](../syntheses/jeffrey-oracle.md) — user identity (the leak is by jeffrey)
- [[PR-135-MiniMax-Hardcode-Leak]] — entity stub for the PR itself

## Rules

1. **Never** inline a resolved credential into a tracked file to "fix" a placeholder bug
2. **Never** commit a `*.json` file with live credentials, even in `chore: backup` snapshots — git history is forever
3. **Always** add `auth.json`, `*.api-key`, `*-credentials.json`, `openclaw.json`, `secrets/**` to `.gitignore` BEFORE first commit
4. **Always** treat leaked credentials as compromised even if rotated; the leak window is a forensic event
5. **Always** document the leak timeline with commit SHAs so future agents can correlate with any anomalous activity

## References

- Live probes: `GET /v1/models` (auth, free) and `POST /anthropic/v1/messages` (inference, ~20 tokens)
- Source: sources/project-2026-06-19-minimax-key-audit-rotation-state.md
- Beads: #131 (leak source located), #132 (candidate key tested), #130 (3aac8fe8 audit pending)
- Provenance: PR #135 commit `f3a995553a` (2026-03-14 13:40:43)