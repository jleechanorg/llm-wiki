---
title: "GraphQL resolveReviewThread is the only way to satisfy Green Gate gate 5 (codex-connector threads)"
type: source
tags: [green-gate, gate-5, graphql, resolveReviewThread, codex-connector, coderabbit, pr, github, hermes-harness]
date: 2026-06-14
source_file: ~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-06-14_green_gate_gate5_resolveReviewThread.md
bead: jleechan-5xho
---

## Summary
Green Gate `gate 5` (Comments resolved) reads GraphQL `isResolved` on review threads — not REST comment count. `gh pr comment` replies create REST review comments that do **not** flip `isResolved` and do not satisfy gate 5. CodeRabbit threads auto-resolve on CR's own confirm-fix replies (its bot author clicking "Resolve conversation" on its own thread via the resolved-marker), but codex-connector threads stay open. The only fix is an explicit GraphQL `resolveReviewThread` mutation per thread.

## Key Claims
- Gate 5's filter logic: `isResolved==false`, excludes comments authored by the PR author, excludes comments starting with `nit:` / `nitpick` (case-insensitive).
- When `LATEST_CR == APPROVED`, gate 5 is **non-blocking** even with unresolved threads (CR sign-off pre-empts unresolved noise).
- codex-connector does not emit a resolved marker, so its threads stay `isResolved=false` after a fix push.
- The fix is a 2-step GraphQL procedure: (1) list `pullRequest.reviewThreads` with `isResolved`, (2) for each unresolved thread call `mutation { resolveReviewThread(input: {threadId: $threadId}) }`.

## Distinguishing From Other CR States
- **CR DISMISSED-stuck** (variant 1): formal review `state` stays `DISMISSED` on a stale SHA, no APPROVED ever lands. Needs admin-override merge per [[coderabbit-dismissed-stuck-admin-override]] memory.
- **CR rate-limit / out-of-credits** (variant 2): formal review `state` stays `none` because CR never starts. Distinguished by literal `Review limit reached` / `usage credits` in CR's last 5 comments. Sometimes recoverable with fresh-commit push + `@coderabbitai all good?` ping.
- **CR APPROVED but threads unresolved** (this case): gate-3 PASS, but gate-5 FAIL on codex-connector threads. Use GraphQL `resolveReviewThread`.

## Key Code
```bash
# 1. List unresolved threads
gh api graphql -f query='
  query($owner: String!, $name: String!, $number: Int!) {
    repository(owner: $owner, name: $name) {
      pullRequest(number: $number) {
        reviewThreads(first: 100) { nodes { id isResolved } }
      }
    }
  }
' -f owner='jleechanorg' -F name='jleechanclaw' -F number=621

# 2. Resolve each one
for tid in PRRT_kwDORP9hos6JYBj8 ...; do
  gh api graphql -f query='
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { id isResolved }
      }
    }
  ' -f threadId="$tid"
done
```

## Connections
- [[GraphQLReviewThreads]] — broader concept page on `pullRequest.reviewThreads` and the injection-safe wrapper
- [[GreenGateCI6GatePattern]] (green-gate-ci-pattern-2026-05-14) — gate 5 of the 6-gate eligibility check
- [[coderabbit-dismissed-stuck-admin-override]] — variant 1 (DISMISSED-stuck) admin-merge path
- [[24h-drive-complete-2026-06-14]] (project_2026-06-14_24h_drive_complete) — provenance: PR #621 fix-up

## Provenance
PR [#621](https://github.com/jleechanorg/jleechanclaw/pull/621) (recovery/session-2026-06-13-lost-commits), 2026-06-14. After pushing 12a4dc99eb with all substantive fixes + replying to 5 threads via `gh pr comment`, Green Gate gate 5 still reported `3 unresolved` (3 codex-connector threads). Resolved via GraphQL → re-ran Green Gate → 7-green → admin-merged at 08:20:11Z.
