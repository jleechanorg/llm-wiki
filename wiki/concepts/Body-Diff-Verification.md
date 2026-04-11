---
title: "Body-Diff Verification (Step 0)"
type: concept
tags: [jeffrey, oracle, PR-review, evidence]
sources: [jeffrey-oracle]
last_updated: 2026-04-10
---

Body-diff verification (Step 0) is the practice of comparing a PR's description claims against the actual `gh pr diff` before giving any verdict. It is the first gate in the Jeffrey Oracle — if the body doesn't match the diff, the PR is rejected regardless of CI status, size, or any other factor. A mismatch is not a minor issue; it is treated as a direct misrepresentation.

Step 0 catches three distinct failure modes: lies about what changed (e.g., claiming an operator was modified when the diff shows it unchanged), omissions where a modified file is absent from the change enumeration, and framing lies where new code is described as fixing existing code. Each is a disqualifying failure.

The oracle has caught Step 0 failures across multiple batches: PR #6130 framed a 225-line test addition as "tooling only," PR #6187 described a new 465-line script as removing a redirect from existing code, PR #6186 modified `settings.json` without listing it in production code changes, and PR #6183 claimed a `>` to `>=` change that the diff showed as unchanged — the second occurrence of that lie on the same PR.

The correct behavior is to describe every file that changes and nothing more. [[jeffrey-oracle]]
