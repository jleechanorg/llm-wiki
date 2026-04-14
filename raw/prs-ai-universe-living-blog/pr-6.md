# PR #6: [P2] feat: daily novel summary cron for ai_universe_living_blog

**Repo:** jleechanorg/ai_universe_living_blog
**Merged:** 2026-03-26
**Author:** jleechan2015
**Stats:** +210/-3 in 4 files

## Summary
Implement a daily GitHub Actions cron job that generates and posts the community novel daily summary for `jleechanorg/ai_universe_living_blog`. The cron fires at 23:30 UTC each evening and is gated on having at least 3 posts for the day — preventing noisy low-signal summaries.

Part of phase 2 roadmap (bead: jleechan-nxjw).

## Background
Implement a daily GitHub Actions cron job that generates and posts the community novel daily summary for `jleechanorg/ai_universe_living_blog`. The cron fires at 23:30 UTC each evening and is gated on having at least 3 posts for the day — preventing noisy low-signal summaries.

Part of phase 2 roadmap (bead: jleechan-nxjw).

## Raw Body
## Background

Implement a daily GitHub Actions cron job that generates and posts the community novel daily summary for `jleechanorg/ai_universe_living_blog`. The cron fires at 23:30 UTC each evening and is gated on having at least 3 posts for the day — preventing noisy low-signal summaries.

Part of phase 2 roadmap (bead: jleechan-nxjw).

## Goals

- [x] GitHub Actions cron fires daily at 23:30 UTC
- [x] workflow_dispatch trigger for manual / backfill runs
- [x] `shouldRunDailySummary` gate prevents summary when < 3 posts exist
- [x] 6 unit tests for `shouldRunDailySummary` — all passing

## Tenets

- TDD: write test first, watch it fail, implement minimal code to pass
- No mocks for the test assertions — mock only the `BlogStorage` interface
- Configurable min-posts threshold (hardcoded to 3, matching DEFAULT_NOVEL_CONFIG)

## Changes

### `src/novel/daily-generator.ts`
Added `shouldRunDailySummary(storage, date, repoKey)`. Calls `fetchDailyPosts` and returns `true` if >= 3 posts, logs a warning and returns `false` otherwise. Reuses existing `fetchDailyPosts` pagination to avoid missing posts from older days.

### `tests/daily-generator-cron.test.ts` (new)
6 unit tests covering: >= 3 posts (true), > 3 posts (true), < 3 posts (false), 0 posts (false), wrong date (false), wrong repo (false).

### `.github/workflows/daily-summary.yml` (new)
- `schedule`: `cron: '30 23 * * *'`
- `workflow_dispatch`: optional `date` input (YYYY-MM-DD)
- Uses `npm run dev:novel -- daily-summary --repo=jleechanorg/ai_universe_living_blog --session=daily-$GITHUB_RUN_ID`

## Testing

- Unit tests: `npm test -- tests/daily-generator-cron.test.ts` — **6/6 pass**
- TypeScript: `npm run typecheck` — **pass**
- Full suite: `npm test` — 43/44 pass (pre-existing `install.test.ts` failure unrelated to this PR)

## Testing (smoke — HTTP services)

The workflow calls `npm run dev:novel -- daily-summary` which invokes `runDailySummaryPipeline`. In GitHub Actions, this uses `MemoryBlogStorage` (zero-c
