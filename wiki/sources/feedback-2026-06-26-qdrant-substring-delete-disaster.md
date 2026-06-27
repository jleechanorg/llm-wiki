---
title: "Qdrant mass-delete anti-pattern — substring matching deleted 9 real memories 2026-06-26"
type: source
tags: [qdrant, vector-db, anti-pattern, data-loss, mem0, destructive-ops, snapshot, gate, mcp-smoke]
date: 2026-06-26
source_file: ../raw/feedback_2026-06-26_qdrant_substring_delete_disaster.md
---

## Summary
On 2026-06-26 during a mem0 fastembed migration verification, an attempt to clean up smoke-test memories via Python substring matching (`if "smoke" in mem.lower()`) silently deleted 9 legitimate Gate 8 / MCP Smoke / FastEmbed PR #7848 project memories from the Qdrant `hermes_mem0` collection. No snapshot existed before the mass-delete; recovery is manual re-insertion only, with possible semantic drift because the embedder model changed (nomic-embed-text → BAAI/bge-base-en-v1.5).

## Key Claims
- Substring matching (`"smoke"`, `"fastembed"`) for memory cleanup is a code smell that conflates **content signal** (the word appears in real memories) with **test signal** (the word was added in a smoke test).
- Qdrant has no `restore_recently_deleted()` API. Without `c.create_snapshot()` called BEFORE the delete, deletion is permanent from the API surface even though mmap files may still hold the records.
- The right protocol for any vector-DB mass-delete is: (1) snapshot first and verify file lands, (2) delete by exact ID list captured at insert time, (3) two-pass preview (print candidate IDs + payload) before destructive ops, (4) use a separate test collection for verification work.
- mem0 + Groq LLM extract 1–3 distinct memory records per `add()` call. If you add N smoke tests, expect up to 3N records — you must track ALL the IDs Groq extracted, not just the ones from your immediate `add()` return.
- 9 deleted memory IDs (permanent loss): 32289f7c, 394b977d, 47a5623e, 8b526e27, 9b16dd91, aaba7ed6, c80e4f36, d64066bd, e4b56f93 — all Gate 8 / MCP Smoke / FastEmbed PR #7848 context, 2026-06-22 to 2026-06-25.

## Key Quotes
> "Substring ≠ ID. `\"smoke\" in text` will match `MCP Smoke`, `smoke test`, `smoke semantics`, `red-green smoke`, `Smoke Gate`, etc. The patterns I used would have matched almost any devops/CI memory." — anti-pattern rule

> "Tombstone ≠ recover. Qdrant segments are append-only with tombstone markers; without a snapshot, deleted records are gone from the API even if the mmap file still has them." — recovery rule

> "If you find yourself adding records just to test them and then deleting them, use a separate test collection. Qdrant collections are cheap." — prevention rule

## Connections
- [[Mem0FastEmbedMigration]] — the migration that triggered this cleanup; the embedder swap was the reason smoke tests were needed
- [[MacCompressorOOMPressureSignal]] — the original watchdog context that motivated the ollama → fastembed migration
- [project-2026-06-20-browser-compressor-oom](../sources/project-2026-06-20-browser-compressor-oom.md) — earlier memory about mem0 watchdog patterns
- bd-2fp — closed tracking bead for this lesson
- Qdrant snapshot `hermes_mem0-5547385897928023-2026-06-27-00-44-45.snapshot` (25 MB) — post-incident insurance taken 2026-06-27T00:44:45Z; too late to recover the 9 deletes but available for future accidents