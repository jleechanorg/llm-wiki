# PR #9: feat(hooks): add worker-poster auto-posting for AO lifecycle events [P1] (jleechan-yl5g)

**Repo:** jleechanorg/ai_universe_living_blog
**Merged:** 2026-03-26
**Author:** jleechan2015
**Stats:** +465/-0 in 14 files

## Summary
Implements **P1-3: Worker Auto-Posting** from the phase2 roadmap.

- `src/hooks/worker-poster.ts` — `postEvent()` posts `create_post` JSON-RPC calls to the blog MCP server on AO lifecycle events
- `src/hooks/index.ts` — exports `postEvent` and `WorkerEvent` for easy consumption
- `tests/worker-poster.test.ts` — 4 unit tests using `vi.fn()` mock for fetch

## Raw Body
## Summary

Implements **P1-3: Worker Auto-Posting** from the phase2 roadmap.

- `src/hooks/worker-poster.ts` — `postEvent()` posts `create_post` JSON-RPC calls to the blog MCP server on AO lifecycle events
- `src/hooks/index.ts` — exports `postEvent` and `WorkerEvent` for easy consumption
- `tests/worker-poster.test.ts` — 4 unit tests using `vi.fn()` mock for fetch

## TDD

- Write failing test first → module not found (expected)
- Implement `postEvent()` → all 4 tests pass
- Full suite: **38/38 tests passing**

## Testing

- Unit tests: `npm test -- tests/worker-poster.test.ts` (4 passing)
- Full suite: `npm test` (38 passing)
- Typecheck: `npm run typecheck` (clean)
- Lint: `npm run lint` (clean)
- Live API smoke test: blog server on localhost:19999 — health, create_post, list_posts all confirmed working

## Evidence

Full /4layer evidence bundle at `docs/evidence/feat/worker-poster/`:
- L1: unit test output (4 passing)
- L2: full integration suite (38 passing)
- L3: live API call artifacts (health, create_post, list_posts)
- L4: screenshot of unit tests passing

## Note

The plan spec describes `tools/call` JSON-RPC format (MCP standard). The live blog server routes methods directly (`create_post`). `worker-poster.ts` uses the MCP standard format. Integration with the live server requires either updating the blog server to support `tools/call` dispatch, or a future PR to adapt `worker-poster.ts` to the direct routing format.

Closes jleechan-yl5g

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds new outbound JSON-RPC posting logic (timeouts and error parsing) that could affect reliability and error propagation once wired into lifecycle flows, but is currently isolated and covered by focused unit tests.
> 
> **Overview**
> Adds a new `worker-poster` hook (`postEvent`) that posts AO lifecycle events to the blog MCP server by calling `create_post` over JSON-RPC (`POST /mcp`), with inject
