---
title: "Requests API Design"
type: concept
tags: [canonical, python, api-design, requests, simplicity]
sources: [canonical-code-repos/requests]
last_updated: 2026-04-14
---

## Summary

The `requests` library (Python) is the gold standard for simple, correct, elegant API design. Its core insight: HTTP libraries should do 20 things extremely well, not 200 things adequately. Every public function is a one-liner that composes toward a single core. The API surface is almost perfectly flat — `get()`, `post()`, `put()`, `patch()`, `delete()`, `options()`, `head()` all delegate to one `request()` function.

## Key Patterns

### Flat API with Single Core
```python
# Every HTTP verb is a one-liner
def get(url, params=None, **kwargs):
    return request("get", url, params=params, **kwargs)

def post(url, data=None, json=None, **kwargs):
    return request("post", url, data=data, json=json, **kwargs)
```

The entire public API for HTTP verbs is 6 one-liners. No hierarchy, no classes to instantiate, no ceremony.

### Single Core that Composites Cleanly
```python
def request(method, url, **kwargs):
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)
```

The core `request()` function: opens a session, calls `session.request()`. That's it. Resources are always cleaned up via context manager (`with`).

### Excellent Docstrings
Every function has: description, param docs with types, return type, usage example. Docstrings are the complete API contract.

### Explicit is Better Than Implicit
- `params` for query string, `data` for body, `json` for JSON-serialized body — distinct params for distinct HTTP concepts
- `timeout` as explicit float or tuple `(connect, read)` — no magic
- `allow_redirects` defaults to `True` but is explicit — not hidden behavior

### Resource Cleanup by Default
```python
with sessions.Session() as session:  # always closed
    return session.request(...)
```

Every session is used inside a context manager. No sockets left open.

## Connections

- [[FastAPIErrorHandling]] — FastAPI follows the same "explicit params, typed exceptions" philosophy
- [[tRPCTypeSafety]] — tRPC takes the opposite approach (types instead of runtime params) but shares the "minimal surface" tenet
- [[VerificationLoop]] — the `request()` pattern of "one clear input → one clear output" is verification-friendly

## What This Means for Code Generation

When generating API client code: a flat, one-liner-per-verb structure is nearly always correct. If your generated API wrapper has nested classes or multi-line verb functions, it's overengineered.
