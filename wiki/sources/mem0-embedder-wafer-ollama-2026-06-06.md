---
title: "mem0 embedder Wafer→Ollama silent-failure fix"
type: source
date: 2026-06-06
tags: [mem0, embeddings, ollama, wafer, credentials, silent-failure, config, qdrant, rca]
raw: raw/feedback_2026-06-06_mem0_embedder_wafer_ollama.md
bead: jleechan-b4a
---

# mem0 embedder silently broken by Wafer token in OPENAI_API_KEY; fixed via local Ollama nomic-embed-text

## Summary

In a 2026-06-06 dark-factory session, mem0 fact-extraction/embedding was silently
failing. Root cause was **two stacked, invisible failures** in
`~/.hermes/.claude/hooks/mem0_config.py`:

1. **Wrong provider's token in `OPENAI_API_KEY`.** The default embedder was
   `provider=openai` / `text-embedding-3-small`, keyed on `OPENAI_API_KEY`. On this
   machine that variable holds a **Wafer** token (`wfr_…`) — Wafer is an
   Anthropic-compatible gateway, not OpenAI, so the openai embedder rejected it.
2. **A config override that was a silent no-op.** `_merge_mem0_from_hermes_config()`
   parsed `~/.hermes/config.yaml` with `json.loads()`. The file is **YAML**, so
   `json.loads()` threw; the exception was swallowed (printed only under
   `MEM0_HOOKS_DEBUG=1`). The merge never applied, so the broken openai default
   always ran.

## Fix

Switched the embedder to a **local Ollama** provider: `provider=ollama`,
`model=nomic-embed-text`, `ollama_base_url=http://localhost:11434`,
`embedding_dims=768`. `nomic-embed-text` is exactly **768-dim** (probed live),
matching the existing Qdrant `hermes_mem0` collection (768) — a drop-in with **no
re-index**. mem0 is now **key-free** (`mem0_hooks_enabled()` returns `True` with
`OPENAI_API_KEY` empty); the LLM side stays on local Ollama `gemma2:2b`.

## MiniMax embeddings — researched and rejected

MiniMax offers embeddings (`embo-01`, 1536-dim, `/v1/embeddings`) but is unusable
for mem0: no `minimax` embedder provider ships with mem0; it requires
`MINIMAX_GROUP_ID` (absent from `~/.bashrc`); its request schema is non-OpenAI
(`type=db/query`) so it cannot reuse the openai shim; `MINIMAX_BASE_URL` is
Anthropic-flavored (`https://api.minimax.io/anthropic`) and OpenAI chat paths 404.

## Verification

- `m.add()` with `OPENAI_API_KEY` unset succeeded (ADD events, qdrant HTTP 200).
- Qdrant collection points confirmed at 768 dims.
- `m.search()` round-trip returned hits.
- The previously /learn-skipped /er evidence-review learning is now also saved to mem0 (2 ADD events).

## Generalizable rules

1. Never store a provider-A token in a provider-B env var (Wafer is Anthropic-shaped, not OpenAI).
2. Config loaders that swallow parse exceptions become silent no-ops — a YAML file
   parsed by `json.loads()` fails closed and invisibly. Match the parser to the file
   format and surface the error.
3. Ollama `nomic-embed-text` (768-dim) is a key-free drop-in for OpenAI
   `text-embedding-3-small` configured at 768 dims.

See also: [[CredentialValidation]], [[evidence-review-unscorable-axes-2026-06-05]]
