# PR #8: [P1] feat(hooks): AO lifecycle hook + GitHub Actions workflow for novel entries

**Repo:** jleechanorg/ai_universe_living_blog
**Merged:** 2026-03-26
**Author:** jleechan2015
**Stats:** +738/-0 in 26 files

## Summary
Implements **P1-1** of the [Phase 2 Roadmap](docs/superpowers/plans/2026-03-26-phase2-roadmap.md) — AO Lifecycle Hooks.

- `src/hooks/event-schema.ts`: TypeScript types for `PrEvent` and `PrEventType`
- `src/hooks/ao-lifecycle.ts`: `handlePrEvent()` — triggers `branch-entry` novel pipeline on `pr_opened` / `pr_merged` / `pr_closed`; skips all other event types. Includes `buildCliArgs()` helper and `defaultRunCli()` spawn implementation.
- `tests/ao-lifecycle.test.ts`: 8 unit tests (vi.fn() mock 

## Background
The Phase 2 roadmap calls for auto-triggering novel branch entries whenever an AO worker opens, merges, or closes a PR. This PR wires that up end-to-end: GitHub Actions fires on PR events, runs `npm run dev:novel -- branch-entry ...`, and the novel engine posts a narrative entry to the blog.

## Raw Body
## Summary

Implements **P1-1** of the [Phase 2 Roadmap](docs/superpowers/plans/2026-03-26-phase2-roadmap.md) — AO Lifecycle Hooks.

- `src/hooks/event-schema.ts`: TypeScript types for `PrEvent` and `PrEventType`
- `src/hooks/ao-lifecycle.ts`: `handlePrEvent()` — triggers `branch-entry` novel pipeline on `pr_opened` / `pr_merged` / `pr_closed`; skips all other event types. Includes `buildCliArgs()` helper and `defaultRunCli()` spawn implementation.
- `tests/ao-lifecycle.test.ts`: 8 unit tests (vi.fn() mock for `runCli`) covering all trigger/skip paths, full CLI arg assembly, and error propagation
- `.github/workflows/novel-entry.yml`: GitHub Actions workflow triggered on PR `opened` / `closed` / `reopened` for `feat/` / `fix/` / `chore/` / `docs/` / `refactor/` branches

## Background

The Phase 2 roadmap calls for auto-triggering novel branch entries whenever an AO worker opens, merges, or closes a PR. This PR wires that up end-to-end: GitHub Actions fires on PR events, runs `npm run dev:novel -- branch-entry ...`, and the novel engine posts a narrative entry to the blog.

## Goals

1. `handlePrEvent()` calls novel CLI for `pr_opened`/`pr_merged`/`pr_closed` — ✅
2. `handlePrEvent()` skips `pr_review_requested`/`pr_comment`/etc. — ✅
3. GitHub Actions workflow fires on relevant branch types — ✅
4. Full /4layer evidence bundle included — ✅

## Tenets

- **TDD**: tests written first, implementation second
- **Real > fake**: novel CLI smoke-tested end-to-end (real `create_post` call, real post ID returned)
- **No breaking changes**: new files only, no modifications to existing source

## Testing

- **L1**: `npm test` — 42/42 pass (8 new ao-lifecycle tests)
- **L2**: Same suite covers novel pipeline integration
- **L3**: Real `npm run dev:novel -- branch-entry` smoke test — post `9dbb626d-836d-4c4a-ad87-7fa798ce806a` created
- **L4**: Screenshots in `docs/evidence/feat/ao-lifecycle-hooks/layer4-visual/`
- **Lint**: `npm run lint` — 0 errors
- **Typecheck**: `npm run type
