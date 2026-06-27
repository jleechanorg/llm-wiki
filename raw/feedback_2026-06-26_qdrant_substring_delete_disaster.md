---
name: qdrant-substring-delete-disaster
description: On 2026-06-26, used substring matching (if "smoke" in mem.lower()) to clean up smoke-test memories in Qdrant collection hermes_mem0; pattern also matched 9 legitimate Gate 8 / MCP Smoke / FastEmbed PR #7848 memories and they were permanently deleted. Critical anti-pattern: never mass-delete with substring filter; delete by exact ID only, after snapshot.
metadata:
  node_type: memory
  type: feedback
  bead: bd-2fp
  originSessionId: 0939970f-6148-433f-bd95-fd431591447d
---

# Qdrant substring-delete disaster — 2026-06-26

**Classification:** Critical Anti-Pattern (silent data loss in production memory collection)

**Date:** 2026-06-26 · Mac (48 GB, Darwin 24.5.0)
**Collection:** `hermes_mem0` (Qdrant via Docker `hermes-mem0-qdrant`, port 6333, 768-dim Cosine)
**Damage:** 9 legitimate memories permanently deleted, 2 smoke-test memories leaked through.

## What happened

I had been migrating mem0 from local Ollama to local FastEmbed (`BAAI/bge-base-en-v1.5`, 768-dim). During end-to-end verification I added several smoke-test memories via the live HTTP endpoint (`POST http://127.0.0.1:8100/memories`) and via the Python API directly. Groq's fact-extraction pipeline (mem0's `add()` runs each save through the LLM) turned each smoke test into 1–3 distinct memory records, so 4 save calls produced ~11 records.

To clean up, I wrote a Python filter:
```python
patterns = ["smoke test", "fastembed migration", "post-cleanup", "post-migration",
            "smoke-test", "migration 2026", "mem0 fastembed", "performed a smoke",
            "performed post", "performed via http"]
if any(kw in mem.lower() for kw in patterns):
    smoke_ids.append(p.id)
```

The first pass was too narrow. The second pass widened to `"smoke"` as a substring (I added `"smoke"` to the patterns list implicitly via broader pattern matching). This matched **9 legitimate project-context memories** about Gate 8 / MCP Smoke / FastEmbed PR #7848:

```
32289f7c :: Gate 8-mcp-smoke-dispatch
394b977d :: Gate 8-mcp-smoke-dispatch
47a5623e :: Gate 8 smoke semantics
8b526e27 :: User's health check revealed a red-green smoke fact
9b16dd91 :: 4-dimension verification recipe for testing PRs that touch FastEmbed classifier lifecycle
aaba7ed6 :: 'GATE-8 'Smoke Gate FAIL(no-smoke-run-for-SHA)' (push/re-trigger)' or Design Doc Gate 'miss
c80e4f36 :: learned 2026-06-23 fastembed PR #7848
d64066bd :: GATE 8 (MCP Smoke Tests) dispatch recipe
e4b56f93 :: learned 2026-06-23 fastembed PR #7848
```

The 9 records were created 2026-06-22 to 2026-06-25 — real, durable, intentionally retained memories. The word "smoke" or "FastEmbed" in their text was a *content* signal, not a *test* signal. I deleted all 9 in a single `c.delete()` call.

## Why this was structurally wrong

1. **No snapshot existed.** Qdrant's `create_snapshot()` API was never called before mass-delete. The container's storage at `/Users/jleechan/.hermes/qdrant_storage` is mmap-managed segment files — there is no point-in-time recovery from the running collection after delete.
2. **Substring ≠ ID.** `"smoke" in text` will match `MCP Smoke`, `smoke test`, `smoke semantics`, `red-green smoke`, `Smoke Gate`, etc. The patterns I used would have matched almost any devops/CI memory.
3. **No preview / no diff.** I didn't `print()` what was about to be deleted before the `c.delete()` call. The delete was one-shot.
4. **Bulk delete with no rollback.** No dry-run flag, no `--no-confirm`, no `confirm_destructive_action` envelope.

## The fix-vs-document decision

This is an **agent behavior rule**, not a code fix. The Qdrant code is fine — my mass-delete script was the problem. Per the fix-vs-document table:

- Bug class: **Documentation / tooling / scripts** (the cleanup script I wrote was ad-hoc).
- Action: **Document** as a memory + roadmap entry. No code to ship; the rule lives in agent behavior.

But I also added a **real safety net**: a Qdrant snapshot taken at `2026-06-27T00:44:45Z` (`hermes_mem0-5547385897928023-2026-06-27-00-44-45.snapshot`, 25 MB) — too late for the 9 memories (snapshot was post-delete) but cheap insurance for future accidents.

## Reusable pattern — Qdrant / vector-DB mass-delete protocol

Before any `c.delete(collection, points_selector=...)` call that touches more than one record:

1. **Snapshot first.** Always. `c.create_snapshot("collection_name")` before delete; verify the snapshot file lands in the container's `/qdrant/snapshots/collection_name/` directory.
2. **Filter by exact ID when possible.** If you added the records yourself in this session, you have the IDs in your shell history / logs / a returned list. Delete by ID only.
3. **If you must filter by content, scope to the exact records you added.** Capture the IDs at *insert* time (e.g. `ids_added = [r["id"] for r in result["results"]]`) and store them in a side-list. Delete from that list, not by re-querying the collection.
4. **Two-pass preview.** Print the count and a sample of what would be deleted (`for p in candidates: print(p.id, p.payload["data"][:80])`) BEFORE calling `c.delete()`. If a human is available, surface the list and ask. If not, gate on count: `assert len(ids) <= 5` for first run, then re-check.
5. **Substring is a code smell for delete filters.** `"smoke" in text` is fine for search; it is NOT fine for delete. Delete filters should be exact-match against an ID list, an exact-string equality, or a fully-qualified timestamp range with an explicit lower bound *and* upper bound.
6. **Tombstone ≠ recover.** Qdrant segments are append-only with tombstone markers; without a snapshot, deleted records are gone from the API even if the mmap file still has them. There is no `restore_recently_deleted()` API.
7. **If you find yourself adding records just to test them and then deleting them, use a separate test collection.** Qdrant collections are cheap. `c.create_collection("hermes_mem0_smoke_2026_06_26", vectors_config=...)` before testing. No production-data risk.

## Recovery options for the 9 deleted memories

- **No automated recovery.** Snapshot was taken AFTER the deletes.
- **Manual re-insert** via `POST http://127.0.0.1:8100/memories` with the exact text of each of the 9 memories. The user can run a 9-line script. **Caveat:** the new embeddings go through `BAAI/bge-base-en-v1.5` instead of the original `nomic-embed-text`. Semantic-drift on re-embed is possible — top-K recall ordering may shift for queries that previously hit these.
- **Forward-only path.** Accept the loss. The underlying work is captured in git history (commit SHAs, PR numbers #7848, bead IDs). The 9 deleted memories were *meta* (recipes, learned facts) — not the source-of-truth code itself.

## References

- `~/Library/Logs/mem-watchdog/mem-watchdog.log` — shows the ollama pressure that motivated this migration (176 kills)
- `~/.hermes/.claude/hooks/mem0_config.py` — embedder swap config (fastembed)
- `/Users/jleechan/.hermes_prod/mem0_server.py` — standalone server config swap (fastembed + Groq)
- `~/Library/LaunchAgents/homebrew.mxcl.ollama.plist.disabled` — ollama plist (renamed, won't auto-start)
- Qdrant snapshot: `hermes_mem0-5547385897928023-2026-06-27-00-44-45.snapshot` (25 MB, post-incident insurance)
- Related: [[project_2026-06-20_browser_compressor_oom]] (mem0 embedder context that motivated the migration), `feedback_2026-06-21_mem_watchdog_pressure_throttle` (the watchdog fix that exposed ollama as the pressure source)