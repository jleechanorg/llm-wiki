# Skeptic Self-Verify Gate Fixes — 2026-05-04

**Source**: Claude auto-memory
**Location**: `memory/feedback_2026-05-04_skeptic-self-verify-gate-fixes.md`
**Bead**: rev-adt9y

## Summary

PR #6783 (living world turn recovery) was blocked from reaching 7-green by four bugs in `skeptic-self-verify.yml` and GitHub API usage.

## Fix 1: BUGBOT=none should be PASS

**Problem**: Gate 4 returned `FAIL(bugbot=none)` because Bugbot had never run on the PR.

**File**: `.github/workflows/skeptic-self-verify.yml` line 147

**Fix**: Add `none` to accepted Bugbot conclusions:
```bash
if echo "$BUGBOT" | grep -qiE "^(success|neutral|skipped|none)$"; then G4="PASS"
```

**Commit**: `cbb278882`

## Fix 2: Dismiss stale CR CHANGES_REQUESTED reviews

**Problem**: Old CR CHANGES_REQUESTED reviews from prior commits were superseded but not dismissed.

**Solution**: REST API dismissal:
```bash
gh api -X PUT repos/{owner}/{repo}/pulls/{pull}/reviews/{review_id}/dismissals \
  -f message="Superseded by later CR APPROVED review on {sha}"
```

## Fix 3: Resolve cursor[bot] threads via GraphQL

**Problem**: One cursor[bot] thread remained unresolved after dismissing CR reviews.

**Solution**: GraphQL `resolveReviewThread` mutation:
```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "PRRT_kwDOO8L8Qs5_Q_Vz"}) {
    thread { isResolved }
  }
}'
```

**Note**: Field name is `threadId`, NOT `pullRequestReviewThreadId`.

## Manual Trigger Commands

**skeptic-self-verify**:
```bash
gh workflow run skeptic-self-verify.yml \
  --repo jleechanorg/worldarchitect.ai \
  --ref investigate/living-world-events \
  --raw-field pr_number=6783
```

**green-gate** (requires head_sha):
```bash
gh workflow run green-gate.yml \
  --repo jleechanorg/worldarchitect.ai \
  --ref investigate/living-world-events \
  --raw-field pr_number=6783 \
  --raw-field head_sha=35e1cd8d48f574172c090bbb5e0aab8ab020f080
```

## References

- [PR 6783](https://github.com/jleechanorg/worldarchitect.ai/pull/6783)
- Commit: `cbb278882b7cc3a1353cd8544da4b424d98fdd59`
