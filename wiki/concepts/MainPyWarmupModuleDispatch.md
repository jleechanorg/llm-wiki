---
title: "main.py Warmup Module Dispatch Pattern"
type: concept
tags: [architecture, worldarchitect, claude-md-rule, warmup, mvp-site]
date: 2026-06-22
---

## Summary
`mvp_site/main.py` is a pure HTTP→MCP translation layer. Startup warmup LOGIC (GCS read, in-process cache fill, FastEmbed/ONNX load, daemon thread for shared state) must live in a dedicated `mvp_site/<feature>_warmup.py` module. `main.py` *dispatches* warmups through its existing `_warm_startup_lazy_dependencies()` framework but never owns the warmup logic itself. `mcp_api.run_server` may also dispatch for standalone MCP processes (idempotent).

## Why
Production path is `gunicorn mvp_site.main:app`. The local testing_mcp harness also runs gunicorn + main.py (NOT `mcp_api.run_server`). Original PR #7778 draft dispatched warmup only from `mcp_api.run_server`'s `__main__` block — so the production serve path silently skipped the warmup. Wiring fix `bfea5b9b2f` dispatched `embed_cache_warmup.warm_in_background()` from main.py's lazy-warmup framework.

## Canonical example: `mvp_site/embed_cache_warmup.py`

```python
# mvp_site/embed_cache_warmup.py (the LOGIC)
def warm_in_background() -> None:
    """Daemon thread: loads GCS store, fills in-process LRU. Idempotent."""
    threading.Thread(target=_warm_in_background_impl, daemon=True).start()
```

```python
# mvp_site/main.py (DISPATCH only — no GCS / cache / embed code)
from mvp_site import embed_cache_warmup

def _warm_startup_lazy_dependencies() -> None:
    if _EMBED_CACHE_WARMUP_ENABLED:
        embed_cache_warmup.warm_in_background()
```

## When to apply
Trigger if you're about to add any of these to `main.py` or `mcp_api.py`'s `__main__` block:
- GCS read at startup
- In-process cache fill at startup
- FastEmbed/ONNX load at startup
- Firestore admin client init at startup
- Long-lived daemon thread for shared state

→ Extract to `mvp_site/<feature>_warmup.py` and dispatch from `main.py:_warm_startup_lazy_dependencies()`.

## Refactor rule
If you find warmup LOGIC (GCS read, cache insert, FastEmbed call) **inlined** into `main.py` (vs. dispatched via a call to a `*_warmup.py` module), extract it into a dedicated module and have main.py dispatch it.

## Source
- `mvp_site/main.py` docstring (canonical restatement)
- `roadmap/prompt-embedding-store-warmup-2026-06-21.md` (design doc with rationale)
- `CLAUDE.md` § "Pure API Gateway"
- `AGENTS.md` (operator runbook)
- Review thread r3449331497 on PR #7778
- Commit `bfea5b9b2f` (wiring fix in PR #7778)

## Related
- [[ThreeLayerEmbedStore]]
- [[GCSStoreIdempotentPrecompute]]
- [[StartupWarmup]]
