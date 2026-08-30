---
title: Mem0HelperFiles
type: entity
tags: [mem0, helpers, qdrant, hooks, hermes]
sources: [sources/feedback-2026-07-27-mem0-qdrant-diagnosis-recipe.md, sources/feedback-2026-08-30-cloud-run-and-mem0-drift-guardrails.md]
last_updated: 2026-08-30
---

The Mem0 helper files that need to be kept on the current Python package API:

| Path | Calls | Migrations applied |
|---|---|---|
| `~/.hermes/.claude/hooks/mem0_save.py` | `m.add(message, user_id=USER_ID, infer=True)` | None — `add()` still accepts `user_id=` as a kwarg in mem0 2.x |
| `~/.hermes/.claude/hooks/mem0_recall.py` | `m.search(prompt, user_id=USER_ID, limit=TOP_K)` | 2026-07-27 → `m.search(prompt, filters={'user_id': USER_ID}, limit=TOP_K)` |
| `~/.hermes/scripts/mem0_shared_client.py` | `m.search(query, user_id=user_id, limit=k)` (and others) | 2026-07-27 → `m.search(query, filters={'user_id': user_id}, limit=k)` |
| `~/.hermes/scripts/mem0_dedup.py` | `m.get_all(user_id=user_id, limit=BATCH)` | 2026-07-27 → `m.get_all(filters={'user_id': user_id}, limit=BATCH)` |

`mem0_save.py` is the highest-traffic of the four because it runs as a Stop hook on every
session. A fail-open hook may preserve the parent operation, but it must emit bounded
diagnostics; blanket suppression masked the recall regression again on 2026-08-30.

## Migration detection

When mem0 package upgrades and stops accepting `user_id=` on a particular method, every
helper that calls that method begins to raise `ValueError: Top-level entity parameters
... are not supported in <method>()`. The Stop hook eats the exception so the only
visible symptom is silent reverts: facts stop being saved, past searches return [],
nothing complains in user-facing surfaces. When investigating, run the helpers
directly and look at stderr.

## Detection recipe

```bash
# Re-derive the helper, don't trust the gate
python3 -c "
import sys; sys.path.insert(0,'/Users/jleechan/.hermes/.claude/hooks')
from mem0_config import USER_ID
from mem0 import Memory
from mem0_config import MEM0_CONFIG
m = Memory.from_config(MEM0_CONFIG)
hits = m.search('any-query', filters={'user_id': USER_ID}, top_k=5)
print('search:', len(hits.get('results', [])))
"
# If this returns 0 (and mem0 actually has data), the helper or something in the
# call chain is on the old API.
```

The installed Mem0 2.0.14 contract observed on 2026-08-30 uses `top_k` rather than
`limit` for search. Compatibility tests must assert the installed SDK call shape, and
the live health probe must run a real read-only search rather than stop after import or
`Memory.from_config()`.

## Extraction authentication fallback

A configured `GROQ_API_KEY` is not proof that extraction works. On 2026-08-30, a real `/learn` save returned `401 invalid_api_key` and inferred writes were discarded despite presence-only enablement. jleechanclaw PR #841 (`e614e005d2ad9fe640f31a21881739a452799aab`) made that boundary report the error and preserve a bounded direct memory with `infer=False` through the local embedder and Qdrant. Two tests passed; a real fallback add returned `ADD`, and search ranked the canary first at `0.929`.

## See also

- [[Mem0QdrantDeployment]] — broader deployment recipe
- [[Mem0Server]]
- [[ExecutableDependencyHealthChecks]]
- [[SilentFailurePathPattern]]
