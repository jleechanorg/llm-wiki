---
name: mem0-historical-failure-dim-mismatch-and-groq-fix
description: mem0 was silently broken for months — qdrant collection at 1536 dims vs embedder at 768; switched LLM to Groq and added idempotent dim-recovery
metadata: 
  node_type: memory
  type: project
  bead: rev-jb53t
  originSessionId: 971c0ede-d782-4657-b676-352757cca104
---

# mem0 fixed: dim mismatch (1536→768) + Groq LLM + idempotent recovery

## What was wrong (RED)

`python3 ~/.hermes/scripts/mem0_shared_client.py add ...` failed every time with:

```
qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 400 (Bad Request)
b'{"status":{"error":"Wrong input: Vector dimension error: expected dim: 1536, got 768"}}'
```

Two stacked root causes:

1. **Qdrant collection `hermes_mem0` was sized at 1536 dims** (from when mem0 used
   an OpenAI embedder, leftover from the `openclaw_mem0` era). The current config
   uses Ollama `nomic-embed-text` @ 768 dims. Every insert failed dim validation.
2. **mem0 LLM provider was Ollama `gemma2:2b`** — slow, flaky, and per a
   2026-06-09 memory entry ("mem0 client currently broken (`groq` import error)"),
   the historical recovery path was Groq (the `groq` Python package was never
   installed in either `~/.local/orch-venv` or `~/.hermes/.venv`).

User hint was correct: "i think i am supposed to use groq key/". `GROQ_API_KEY`
was already exported in shell env.

## What I changed (GREEN)

1. **Installed `groq`** in both `~/.local/orch-venv` and `~/.hermes/.venv`
   (`pip install groq` → 1.5.0). mem0 ships a Groq LLM provider at
   `mem0.llms.groq.GroqLLM` — it just needs the pip package.

2. **`~/.hermes/.claude/hooks/mem0_config.py`** — switched the LLM block from
   Ollama to Groq:
   ```python
   "llm": {
       "provider": "groq",
       "config": {
           "model": os.environ.get("MEM0_GROQ_MODEL", "llama-3.3-70b-versatile"),
           "api_key": os.environ.get("GROQ_API_KEY", ""),
           "temperature": 0,
       },
   }
   ```
   Embedder stays Ollama `nomic-embed-text` @ 768 dims (free, local, fast).

3. **Recreated the qdrant `hermes_mem0` collection at 768 dims**:
   ```bash
   curl -X DELETE http://127.0.0.1:6333/collections/hermes_mem0
   curl -X PUT http://127.0.0.1:6333/collections/hermes_mem0 \
     -H "Content-Type: application/json" \
     -d '{"vectors": {"size": 768, "distance": "Cosine"}, "on_disk_payload": true}'
   ```
   Collection had 0 points at the time (orphaned from the dim change). All
   historical data was already gone.

4. **`~/.hermes/scripts/mem0_shared_client.py`** — added idempotent
   dim-mismatch auto-recovery:
   - `_recreate_collection_at_embedder_dim()` — drops + recreates the collection
     at the embedder's declared `embedding_dims`, then resets the cached
     `Memory` instance.
   - Wrapped `m.add(...)` so a `qdrant_client.http.exceptions.UnexpectedResponse`
     triggers a one-shot recreate + retry. One-shot guard via `_DIM_RECREATE_DONE`
     prevents infinite loops if the embedder config itself is mis-sized.

5. **`~/.hermes/scripts/mem0_health_check.py`** (new) — 5-check smoke test:
   `groq package` + `qdrant dim == 768` + `mem0 LLM == groq` +
   `add_memory(infer=True)` + `search_memory()`. Returns exit 0 if all 5 pass.

## Verified (GREEN output)

```
[PASS] groq python package importable
[PASS] qdrant hermes_mem0 dim == 768  (size=768)
[PASS] mem0 LLM provider == groq  (api_key=set)
[PASS] mem0 add (LLM extract + embed + vector store)  ({"id": "cb81b70c-...", "memory": "test add with new fact 17821...")
[PASS] mem0 search returns at least one result  ([0.681] User's health check revealed a red-green smoke fact
[0.440] test add with new fact 1782169871429889000 ...)
Result: 5/5 passed
```

## Performance note (informational, not a blocker)

End-to-end `add_memory(..., infer=True)` now takes ~60-180s because of:
- Groq API call for fact extraction (~30-60s, network latency to Groq)
- mem0 creating its internal `mem0migrations` collection on first init
  (PUT index requests take ~1-2s each)
- Ollama embed (~50-200ms)
- qdrant insert (~5-50ms)

The smoke test uses a 300s timeout to absorb the first-run init cost. Subsequent
runs should be faster.

## Why this fixes "always failing historically"

The dim mismatch is a one-time fix (collection recreated). The Groq LLM switch
removes the silent-drop bug that local Ollama `gemma2:2b` was hitting. The
idempotent dim-recovery wrapper means any future embedder dim change can
self-heal on the next write — no more "mem0 broken, no one knows why" mode.

## Files changed

- `~/.hermes/scripts/mem0_health_check.py` (new) — red-green smoke test
- `~/.hermes/scripts/mem0_shared_client.py` — `_DIM_MISMATCH_EXC`,
  `_recreate_collection_at_embedder_dim()`, wrap `m.add` with retry
- `~/.hermes/.claude/hooks/mem0_config.py` — `MEM0_CONFIG["llm"]` → groq
- qdrant `hermes_mem0` collection — recreated at 768 dims
- venv `groq` package — installed in `~/.local/orch-venv` and `~/.hermes/.venv`

## Related

- [[mem0-path-hermes-not-openclaw]] — mem0 helpers live at `~/.hermes/...`,
  not `~/.openclaw/...`
- `project_2026-06-09_dark_factory_spec_gen_dispatch.md` — earlier memory entry
  that flagged "mem0 client currently broken (`groq` import error)"
- `~/.hermes/scripts/auto_fact_capture.py` — has its own Groq path that also
  needed the `groq` pip package (now installed)
