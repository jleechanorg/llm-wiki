---
title: "PR #7: [P0] feat(storage): FirestoreBlogStorage + storage factory (P0-1)"
type: source
tags: [ready-for-review, review-request]
date: 2026-03-27
source_file: raw/prs-/pr-7.md
sources: []
last_updated: 2026-03-27
---

## Summary
- Add `createStorage()` factory in `src/blog/storage-factory.ts` with `memory` and `firestore` type support
- Add `FirestoreBlogStorage` implementation in `src/blog/storage-firestore.ts` using `@google-cloud/firestore`
- Wire `--storage` flag (env `STORAGE_TYPE`) in `src/blog/server.ts` and `src/novel/cli.ts`; defaults to memory for zero-config dev
- Add `@google-cloud/firestore` dependency
- 47 tests pass (6 skipped — require `FIRESTORE_EMULATOR_HOST`)

## Metadata
- **PR**: #7
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +266/-50 in 14 files
- **Labels**: ready-for-review, review-request

## Connections
