# PR #2: [agento] living blog + novel engine: full Phase 1 implementation

**Repo:** jleechanorg/ai_universe_living_blog
**Merged:** 2026-03-26
**Author:** jleechan2015
**Stats:** +567/-353 in 23 files

## Summary
Issue orch-yn4 tasked building the living blog + novel engine into ai_universe_living_blog. This PR delivers Phase 1.

## Background
Issue orch-yn4 tasked building the living blog + novel engine into ai_universe_living_blog. This PR delivers Phase 1.

## Raw Body
## Background

Issue orch-yn4 tasked building the living blog + novel engine into ai_universe_living_blog. This PR delivers Phase 1.

## Testing
- npm run build: TypeScript compiles clean
- npm test: 33/33 tests pass

## What's Changed

Blog MCP server: HTTP + JSON-RPC 2.0 with 7 tools (create/get/list/update_post, get/list_threads, health_check).
Novel engine: multi-pass pipeline with 15-bead story system and Claude Sonnet top-level editor.
Install script for portability into any repo.
33 unit tests.

Closes #orch-yn4

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Medium risk because it changes core identifiers (`encodeRepoKey`) and thread auto-creation behavior in `create_post`, which can affect indexing/thread linkage and cross-repo isolation. Also refactors install/deploy workflows and CLI daily-summary behavior, which may break existing integrations if they relied on previous paths/flags.
> 
> **Overview**
> **Core behavior changes:** `create_post` now auto-creates a thread whenever `threadId` is missing *or* when an explicit `threadId` doesn’t exist (while rejecting cross-repo thread attachment), and storage updates now forbid mutating `id` as well as `repoKey`/`threadId` on posts/threads.
> 
> **Data/indexing + novel reliability:** repo indexing switches to `encodeURIComponent`-based `repoKey` encoding, daily-summary fetching paginates through all posts (and fixes chronological ordering for “morning”/“closing” POV selection), and novel config loading now validates fields (voice/date/thresholds) and the CLI enforces required flags/number parsing while dropping the `--blog-url` HTTP-fetch path.
> 
> **Packaging/ops/docs:** adds a separate `./blog-storage` export, updates Docker and GitHub Actions examples to build before running compiled CLIs, hardens installer scripts (arg parsing, cleanup, safer `~/.claude.json` merging with `jq`, and fallback `file:` dependency), and aligns docs/tests/eslint config with the new behavior and paths.
> 
> <sup>Writ
