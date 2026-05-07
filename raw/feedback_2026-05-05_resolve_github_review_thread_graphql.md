---
name: Resolve GitHub review threads via GraphQL resolveReviewThread mutation
description: Unresolved PR review threads (Gate 5) can be resolved programmatically via gh api graphql with resolveReviewThread mutation using thread node ID
type: feedback
bead: none
originSessionId: 157386e1-1e16-474f-88a6-ad9e18acd729
---
## Learning

Gate 5 (all inline comments resolved) failed on PR #6796 due to an unresolved thread with ID `PRRT_kwDOO8L8Qs5_2SPB` on `game_state.py`.

**Fix**: Use `gh api graphql` with the `resolveReviewThread` mutation:
```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "PRRT_kwDOO8L8Qs5_2SPB"}) {
      thread {
        isResolved
      }
    }
  }
'
```

**Result**: `isResolved: true` — Gate 5 passes.

**How to find thread IDs**: Use the `/polish` GraphQL query for `reviewThreads`:
```bash
gh api graphql -f query='
  query($owner:String!, $name:String!, $pr:Int!) {
    repository(owner:$owner, name:$name) {
      pullRequest(number:$pr) {
        reviewThreads(first:100) {
          nodes { id isResolved }
        }
      }
    }
  }
' -f owner=jleechanorg -f name=worldarchitect.ai -F pr=6796
```

**Note**: The node ID prefix `PRRT_` indicates a PR Review Thread. This is stable across API calls.

**When to use**: When Gate 5 fails with "unresolved threads" and the comment has been addressed in code but the thread wasn't clicked "resolved" in the UI. Do NOT use to bypass legitimate unaddressed review comments.

## References
- PR [#6796](https://github.com/jleechanorg/worldarchitect.ai/pull/6796)
- Thread resolved: `PRRT_kwDOO8L8Qs5_2SPB`
- GraphQL mutation: `resolveReviewThread`
