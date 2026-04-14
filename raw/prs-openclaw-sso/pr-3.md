# PR #3: [openclaw_sso] fix: SSO architecture and missing features

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-03-31
**Author:** jleechan2015
**Stats:** +194/-17 in 13 files

## Summary
(none)

## Raw Body
[antig]

Fix Firebase Auth token resolution to use Redis and internal secrets. Resolve streaming status code concurrency issues. Introduce basic SDUI configuration route and add Dockerfiles for Gateway and Relay components.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> Touches authentication/token validation (relay node registration) and changes error propagation semantics across agent→relay→gateway streaming, which can impact security and client compatibility.
> 
> **Overview**
> Improves end-to-end error handling for streamed inference requests: the agent now converts any upstream HTTP `>=400` response into an `ErrorMessage` (parsing a capped JSON error body), and gateway/relay streaming paths now include `statusCode` inside NDJSON error payloads when headers were already sent.
> 
> Adds a new authenticated `GET /v1/sdui/config` endpoint in the gateway that returns a basic UI config, plus new Dockerfiles to build/run the `gateway` and `relay` services.
> 
> Hardens infrastructure behavior: the gateway rate limiter Lua script now restores missing Redis TTLs to avoid stuck “full bucket” keys, the gateway relay client handles response stream errors, and relay WS tests are updated to register nodes via Redis `node:{endpointId}` records with SHA-256 token hashes (reflecting Redis-backed token resolution).
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 88782157c1aa9d466e80ae94c6f60019cb247a9a. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->
