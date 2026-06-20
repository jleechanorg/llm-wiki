---
title: "Auth-file discipline harness gap"
type: concept
tags: [security, credentials, harness-gap, auth-json, tracked-config, future-pr-scope]
sources: [project-2026-06-19-minimax-key-audit-rotation-state, feedback-2026-06-18-real-history-over-gitleaksignore, project-2026-06-19-credential-discipline-4th-admin-override-merge]
last_updated: 2026-06-19
---

## Description

The credential-discipline harness fix shipped 2026-06-19 in PRs [#646](https://github.com/jleechanorg/jleechanclaw/pull/646) and [#9](https://github.com/jleechanorg/browserclaw/pull/9) covers `examples/` and `docs/examples/` files only — it does NOT extend to **tracked runtime config files** like `auth.json`, `openclaw.json`, `*.api-key`, `*-credentials.json`, or `secrets/**`.

The 2026-02-19 MiniMax leak (`a853c71da8` → `f3a995553a` → `3aac8fe80a`) was in `auth.json` and `openclaw.json`. The new discipline rules would NOT have caught it. This is a **second harness layer** that remains to be built.

## Coverage matrix

| File class | Current discipline rules | Tracked in git by default? |
|---|---|---|
| `examples/**` | ✅ Scanned by PRs #646/#9 hooks + CI | Yes |
| `docs/examples/**` | ✅ Scanned by PRs #646/#9 hooks + CI | Yes |
| `seed/`, `seed_data/`, `test_data/`, `fixtures/`, `mocks/` | ✅ Scanned | Yes |
| `*.example`, `*.sample`, `*.mock`, `*.seed`, `*.fixture` | ✅ Scanned | Yes |
| `auth.json` | ❌ Not scanned | **Yes** (until gitignored) |
| `openclaw.json`, `hermes.json` | ❌ Not scanned | **Yes** (until gitignored) |
| `*.api-key`, `*.api_key`, `*-credentials.json` | ❌ Not scanned | Yes |
| `secrets/**` | ❌ Not scanned | Yes |
| `~/.bashrc`, `~/.profile`, `~/.zshrc` | ❌ Not scanned (not in any repo by default) | Varies |
| `.env`, `.env.local` | ❌ Not scanned | Yes |

## Why the gap exists

The 2026-06-19 credential-discipline PRs (#646, #9) were scoped to example/seed/fixture files because:
1. The leak class that prompted them (`example/seed/test fixture credential discipline`) was scoped that way
2. Scanned runtime config files requires *parsing* them to detect credentials, vs the simpler pattern-match approach used for example files
3. Runtime config files like `auth.json` have legitimate non-credential content (model preferences, agent settings) — a naive grep would false-positive

## Future PR scope

**`tracked-config-credential-discipline`** — extend the credential-discipline harness to cover tracked config files. Required pieces:

1. **Path allowlist + schema-aware scanner** — different rules for `auth.json` (parse JSON, check key names like `*api_key`, `*token`, `*secret`), `openclaw.json` (same), `*.api-key` (whole-file), `secrets/**` (whole-file)
2. **Pre-commit hook** — `~/.claude/hooks/pre-commit-tracked-config-credential-scan.sh`, blocks commits that add credentials to tracked files unless path is in `.credential-discipline-allowlist`
3. **CI workflow** — `tracked-config-discipline.yml`, runs `bash tests/test_tracked_config_credential_discipline.sh` on every PR
4. **Per-repo enforcement** — same pattern as PRs #646/#9, port to jleechanclaw, browserclaw, and any other repos with `auth.json` in tree
5. **Allowlist mechanism** — for legitimate non-credential content in `auth.json` (model choices, agent metadata), an allowlist pattern (e.g. `_meta`, `_comment` keys) keeps the scanner precise
6. **Backfill test cases** — re-run against historical commits `a853c71da8`, `f3a995553a`, `3aac8fe80a` to prove the scanner catches them

## Connections

- [minimax-api-key-hardcode-leak-pr-135](minimax-api-key-hardcode-leak-pr-135.md) — the leak that exposed this gap
- [[credential-discipline-drive-4th-admin-override-merge]] — PRs #646 + #9 (covers examples/, NOT auth.json)
- [jeffrey-oracle](../syntheses/jeffrey-oracle.md) — user-side action items: rotation decisions, key revocations
- [[3aac8fe8-leak-commit-investigation]] — related leak via openclaw→hermes refactor

## Acceptance criteria for the future PR

- [ ] Scanner catches `auth.json` with live credentials at PR creation
- [ ] Scanner catches `openclaw.json` with `${ENV_VAR}` placeholders resolved to literal values
- [ ] False-positive rate < 5% on the existing corpus (legitimate `auth.json` configs without credentials)
- [ ] Pre-commit hook blocks commits to tracked files with credentials
- [ ] CI workflow fails PRs that introduce credentials to tracked files
- [ ] Per-repo enforcement active in jleechanclaw + browserclaw + hermes-agent
- [ ] Allowlist mechanism for legitimate non-credential config content
- [ ] Documentation in CLAUDE.md + AGENTS.md + Gemini + Cursor rules
- [ ] Backfill test: re-running against historical leak commits produces failures

## References

- Beads: #131 (MiniMax leak located), #130 (SEC-3 audit pending), #132 (candidate test)
- Provenance: 2026-06-19 audit during credential-discipline drive, identified during wiki-ingest of project_2026-06-19_minimax_key_audit_rotation_state.md
- Companion PRs: jleechanclaw #646, browserclaw #9 (both merged 2026-06-19T02:17Z)