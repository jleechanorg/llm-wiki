---
name: feedback_2026-06-06_mem0_embedder_wafer_ollama
description: mem0 embedder silently broken by a Wafer token sitting in OPENAI_API_KEY; the intended ~/.hermes/config.yaml override never applied because the loader parsed YAML with json.loads() and swallowed the exception. Fixed by switching to a local Ollama nomic-embed-text (768-dim) embedder — a key-free drop-in matching the existing Qdrant collection.
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-b4a
  date: 2026-06-06
  classification: best-practice / anti-pattern (silent-failure RCA + config fidelity)
  originSessionId: 96237b72-565c-4c2d-b265-b151de9c2353
---

# mem0 embedder silently broken by Wafer token in OPENAI_API_KEY; fixed via local Ollama nomic-embed-text

## Context

2026-06-06, dark-factory session. The mem0 hooks (`~/.hermes/.claude/hooks/mem0_config.py`)
were failing to extract/embed facts silently — `m.add()` appeared to run but no real
embedding occurred. Two stacked failures, both invisible by default.

## Technical detail / root cause (two stacked failures)

1. **Provider-A token in a provider-B env var.** The base `MEM0_CONFIG` default embedder
   was `provider=openai`, model `text-embedding-3-small`, keyed on `os.environ["OPENAI_API_KEY"]`.
   On this machine `OPENAI_API_KEY` holds a **Wafer** token (`wfr_…`). Wafer is an
   Anthropic-compatible gateway, **not** OpenAI — so the OpenAI embedder endpoint rejects
   the credential and mem0 fact-extraction/embedding silently fails.

2. **Config loader that fails closed and invisibly.** The intended override,
   `_merge_mem0_from_hermes_config()`, reads `~/.hermes/config.yaml` with `json.loads()`.
   That file is **real YAML**, so `json.loads()` raises; the exception is swallowed (it only
   prints under `MEM0_HOOKS_DEBUG=1`), so the merge is a **silent no-op**. The broken
   OpenAI default therefore always ran — the "override" never applied even when present.

## The fix

Switched the embedder to a **local Ollama** provider:

- `provider=ollama`, `model=nomic-embed-text`
- `ollama_base_url=http://localhost:11434`
- `embedding_dims=768`

`nomic-embed-text` is exactly **768-dim** (probed live), which matches the existing
Qdrant `hermes_mem0` collection (768) — a true drop-in with **no re-index** required.
mem0 is now **key-free**: `mem0_hooks_enabled()` returns `True` with `OPENAI_API_KEY`
empty. The LLM side stays on local Ollama `gemma2:2b`.

## Research conclusion — MiniMax embeddings (rejected)

MiniMax **does** offer embeddings (`embo-01`, 1536-dim, `/v1/embeddings`) but is
**unusable for mem0**:
- mem0 ships **no `minimax` embedder provider**.
- It requires `MINIMAX_GROUP_ID`, which is **absent from `~/.bashrc`**.
- Its request schema is non-OpenAI (`type=db/query`), so it cannot reuse the openai
  embedder shim.
- `MINIMAX_BASE_URL` is Anthropic-flavored (`https://api.minimax.io/anthropic`);
  OpenAI chat paths 404.

## Verification

- End-to-end `m.add()` with `OPENAI_API_KEY` unset **succeeded** (ADD events, qdrant HTTP 200).
- Qdrant collection points confirmed at **768 dims**.
- `m.search()` round-trip returned hits.
- The previously /learn-skipped `/er` evidence-review learning (see cross-link below) is now
  **also saved to mem0** (2 ADD events).

## Reusable rules / pattern

1. **Never store a provider-A token in a provider-B env var.** Wafer is Anthropic-shaped,
   not OpenAI. A `wfr_…` value in `OPENAI_API_KEY` is a misconfiguration that fails at the
   embedder, not at the gateway.
2. **Config loaders that swallow parse exceptions become silent no-ops.** A YAML file parsed
   by `json.loads()` fails closed and invisibly. Match the parser to the file format and
   **surface the error** (don't gate it behind a debug flag).
3. **For local embeddings, Ollama `nomic-embed-text` (768-dim) is a key-free drop-in** for
   OpenAI `text-embedding-3-small` configured at 768 dims — same dimensionality, no re-index.

## References

- File: `~/.hermes/.claude/hooks/mem0_config.py` (`MEM0_CONFIG`, `_merge_mem0_from_hermes_config`, `mem0_hooks_enabled`)
- Config (YAML, mis-parsed): `~/.hermes/config.yaml`
- Qdrant collection: `hermes_mem0` (768-dim)
- Local models: Ollama `nomic-embed-text` (embedder), `gemma2:2b` (LLM)
- Bead: `jleechan-b4a` (CLOSED)
- Cross-link: [[feedback_2026-06-05_evidence_review_unscorable_axes]] — the /er evidence-review learning whose mem0 save was originally skipped; now saved.
