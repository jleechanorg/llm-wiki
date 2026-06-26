---
title: "Capture vs Modify Mode Architecture"
type: concept
tags: [llm-inspector, architecture, design-contract, observe-vs-modify, proxy-modes]
date: 2026-06-26
---

# Capture vs Modify Mode Architecture

**Definition**: `llm-inspector` operates in two architectural layers — **Capture** (observe-only, no body modifications) and **Modify** (body-mutating transforms). The `toolMode` field on the proxy command selects which behaviors are enabled per request. This is the project's pre-existing design contract, formalized 2026-06-24 and reconfirmed in the 2026-06-26 capture-chain session.

## The two layers

### Layer 1 — Capture (observe-only)

- `toolMode: "observe"` (default)
- Captures full HTTP request/response bytes to `docs/raw-http/` or capture file
- Never touches request body, response body, or headers (except for `Authorization` redaction in capture file)
- Pure passthrough proxy: bytes in = bytes out
- Safe to use on production traffic for forensic / observability purposes

### Layer 2 — Modify (body-mutating)

- `toolMode` contains one or more of: `lean`, `on-demand`, `wafer-fix`
- Each modifier transforms the request/response body in-flight
- Modifications are gated behind mode flags at the proxy handler (e.g. `proxy.ts:520, 542, 553, 580, 589`)
- All modifiers are composable (comma-separated): `lean,on-demand,wafer-fix`

| Modifier | What it does | File / line |
|---|---|---|
| `lean` | Strips tool definitions from request body to reduce input token count | `src/filters.ts:13-20` (`parseModeFeatures`) |
| `on-demand` | Replaces on-demand resources with stubs and re-issues with full schema when the model asks for them | `src/proxy.ts:520-580` |
| `wafer-fix` | Patches GLM-5.1 responses that report `input_tokens: 0` after cache hits | `src/proxy.ts:553-589` |

## Why this matters

The two-layer separation lets the same proxy serve two very different use cases:

1. **Production observability** — run with `toolMode: "observe"` on real traffic to log every byte
2. **Token-cost optimization** — run with `toolMode: "lean,on-demand,wafer-fix"` for development sessions where token savings matter

Mixing the two without separation would conflate "what we observed" with "what we mutated" in the capture files. The design intentionally keeps them orthogonal so capture files can be replayed through a clean proxy to verify forward behavior.

## Invariants

1. Capture mode MUST NOT modify any byte the upstream receives (capture-file bytes must be byte-equal to the upstream-received bytes).
2. Modify mode MUST preserve header forwarding exactly except for documented transformations (e.g. hop-by-hop headers stripped per RFC 7230 §6.1).
3. The `toolMode` flag is the single source of truth; no code path should branch on the flag in a way that creates a hidden fourth behavior.

## Verification evidence

- `src/proxy.ts:520, 542, 553, 580, 589` — every modification gated behind mode flag
- `src/filters.ts:13-20` — `parseModeFeatures()` is the canonical parser
- `src/proxy.test.ts` — vitest tests verify each mode independently (lean strips tools, on-demand stubs and re-issues, wafer-fix patches input_tokens)
- `scripts/test-side-by-side.mjs` — side-by-side observe vs lean,on-demand measures savings %

## Related concepts

- [[ServiceDiscrimination]] — a separate concern, but the same architectural discipline (separating "what we look at" from "what we act on")
- [[llm_inspector]] — the project where this design contract lives
- Memory file: `~/.claude/projects/-Users-jleechan-projects-other-llm-inspector/memory/project_2026-06-24_capture-vs-modify-mode-architecture.md`