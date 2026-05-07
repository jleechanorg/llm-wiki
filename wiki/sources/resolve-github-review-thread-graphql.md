# Resolve GitHub Review Threads via GraphQL resolveReviewThread Mutation

**Date**: 2026-05-05  
**Type**: feedback/Best Practice  
**Source**: PR #6796 Gate 5 resolution

## Summary

Gate 5 unresolved PR review threads can be resolved programmatically using `gh api graphql` with the `resolveReviewThread` mutation.

## Command

```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "PRRT_kwDOO8L8Qs5_2SPB"}) {
      thread { isResolved }
    }
  }
'
```

## Finding Thread IDs

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
' -f owner=jleechanorg -f name=worldarchitect.ai -F pr=N
```

## References

- PR [#6796](https://github.com/jleechanorg/worldarchitect.ai/pull/6796)
- Thread resolved: `PRRT_kwDOO8L8Qs5_2SPB`
