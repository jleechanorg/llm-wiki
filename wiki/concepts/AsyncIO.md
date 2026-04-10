---
title: "AsyncIO"
type: concept
tags: [python, async, concurrency]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Description
Python's asynchronous I/O library used in WorldArchitect.AI's unified API to handle concurrent requests. The asyncio.to_thread() function delegates blocking operations (Firebase calls, Gemini API calls) to a thread pool, preventing event loop blocking.

## Why It Matters
Without async handling, loading a campaign would block all other requests. With asyncio.to_thread(), multiple users can interact simultaneously — one user can load campaigns while another processes game actions.

## Connection to [[Unified API]]
The unified API layer uses async functions to maintain responsiveness under load.
