# GitHub REST vs GraphQL Rate Limits — Separate Independent Pools

**Source**: Claude auto-memory feedback_2026-05-27_github-rest-graphql-separate-pools.md  
**Date**: 2026-05-27  
**Type**: Operational Learning

## Key Fact

GitHub maintains **two separate, independent** primary rate limit buckets per authenticated user:

| Pool | Key | Limit | Used by |
|------|-----|-------|---------|
| REST Core | `core` | 5,000 req/hr | `gh api /repos/...` |
| GraphQL | `graphql` | 5,000 pts/hr | `gh pr list --json`, `gh pr view N --json` |

Exhausting one has **no effect** on the other.

## Check Both

```bash
gh api rate_limit | python3 -c "import sys,json; d=json.load(sys.stdin); \
  print('REST:', d['resources']['core']['remaining'], \
        'GraphQL:', d['resources']['graphql']['remaining'])"
```

## References

- https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
