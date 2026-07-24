---
title: "llm-inspector"
type: entity
tags: [project, typescript, http-proxy, llm-api, capture, observability, claude-code, anthropic]
date: 2026-06-26
repo: https://github.com/jleechanorg/llm_inspector
local_path: /Users/jleechan/projects_other/llm_inspector
---

# llm-inspector

**Definition**: A TypeScript HTTP capture proxy that intercepts LLM API calls (Claude Code → Anthropic, Codex → OpenAI, etc.), captures full request/response bytes to disk for forensic analysis, and optionally applies token-saving transformations (lean, on-demand, wafer-fix). Listens on port 9000 by default; routes to upstream (ccproxy-api at port 8000 by default, or any direct LLM endpoint via `--upstream`).

## Origin

- **Repo**: https://github.com/jleechanorg/llm_inspector
- **Local checkout**: `/Users/jleechan/projects_other/llm_inspector`
- **Tech stack**: TypeScript, Node.js 18+, vitest for tests
- **First commit (this repo)**: 2026-06-22 (initial scaffold, capture-proxy.ts)
- **First production-grade milestone**: 2026-06-25 (PR #9 proxy tests merged, PR #12 gzip fix + SHA-256 oracle merged)

## Architecture (two layers)

See [[CaptureVsModifyModeArchitecture]] for the full design contract.

- **Layer 1 — Capture** (`toolMode: "observe"`): passthrough proxy + byte capture to `docs/raw-http/`
- **Layer 2 — Modify** (`toolMode: "lean" | "on-demand" | "wafer-fix" | <combo>`): body-mutating transforms for token savings

## Key files

| File | Purpose |
|---|---|
| `src/proxy.ts` (940+ LOC) | Main HTTP proxy handler — request forwarding, response streaming, capture writing, mode-gated modifications |
| `src/filters.ts` | `parseModeFeatures()` — canonical parser for the `toolMode` flag |
| `src/cli.ts` (321 LOC) | CLI entrypoint — `start`, `stop`, `status`, `_proxy-worker` subcommands |
| `src/analyzer.ts` (391 LOC) | Post-hoc analyzer for captured payloads (context window estimation) |
| `src/utils.ts` (263 LOC) | Shared utilities (size guards, byte helpers) |
| `scripts/llm-inspector-install.sh` | macOS installer (launchd plists, port collision check) |
| `scripts/test-side-by-side.mjs` | Side-by-side observe vs lean,on-demand comparison |
| `scripts/test-reproduction.mjs` | Connection-hang / duplicate-chunk reproduction |
| `docs/raw-http/` | Raw HTTP captures from mitmproxy and real Claude Code sessions |
| `docs/evidence/` | Evidence bundles with SHA-256 checksums |

## CLI surface

```bash
npm run build                    # Compile TypeScript
npm run start -- --upstream http://127.0.0.1:8001
# or
node dist/cli.js start --upstream http://127.0.0.1:8000
node dist/cli.js status
node dist/cli.js stop
node dist/cli.js _proxy-worker --port 9000   # launched by launchd directly
```

## Capture chain

```
Claude Code → llm-inspector :9000 → ccproxy-api :8000 (OAuth injection) → api.anthropic.com
```

Full chain documented in [[CaptureChainEndToEnd20260626]].

## Notable PRs (jleechanorg/llm_inspector)

- **PR #7** — test reproduction script for connection hangs / duplicate chunks (MERGED 2026-06-24)
- **PR #9** — proxy integration tests for observe, lean, on-demand, wafer-fix modes (MERGED 2026-06-24)
- **PR #10** — headersSent race + listener leak fix in proxy.ts (MERGED 2026-06-24)
- **PR #11** — GitHub Actions CI workflow (MERGED 2026-06-24)
- **PR #12** — reIssueWithFullSchema gzip decompression + SHA-256 replay oracle (MERGED 2026-06-25)

## Known open issues

- **#66** — Capture files record `status: None` and empty response body for successful streaming requests
- **#67** — Claude Code 2.1.193 → :9000 returns 400 `context_management: Extra inputs are not permitted`

## Related entities

- [[ccproxy_api]] — OAuth-injecting upstream proxy
- [[Claude_Code]] — the primary client tool whose traffic this proxy captures
- [[mem0_server]] — FastAPI memory service that previously conflicted on port 8000

## Related concepts

- [[CaptureVsModifyModeArchitecture]] — the design contract
- [[ServiceDiscrimination]] — proxy detection pattern in `src/cli.ts`
- [[LaunchdWorkerPIDRace]] — `status` port-check fallback