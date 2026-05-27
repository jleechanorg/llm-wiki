---
name: github-rest-graphql-rate-limits-separate
description: GitHub REST and GraphQL rate limits are SEPARATE independent 5000/hr pools — switch to GraphQL when REST is exhausted
type: feedback
bead: none
---

## Rule

GitHub REST Core and GraphQL have **separate independent** 5,000/hr rate limit pools.

- **REST Core** (`core`): `gh api /repos/...` direct REST calls
- **GraphQL** (`graphql`): `gh pr list --json`, `gh pr view N --json`, `gh pr checks`

When `core` is 0/5000: use `gh pr view` / `gh pr list` (GraphQL — separate pool).
When `graphql` is 0/5000: use `gh api /repos/.../pulls/N` (REST — separate pool).

**Why**: On 2026-05-27 agent incorrectly claimed they shared a pool and told user to wait. In fact GraphQL had 4583/5000 remaining while REST was 0. User corrected immediately.

**How to apply**: Always check both pools before declaring "rate limited":
```bash
gh api rate_limit | python3 -c "import sys,json; d=json.load(sys.stdin); print('REST:', d['resources']['core']['remaining'], 'GraphQL:', d['resources']['graphql']['remaining'])"
```

## References
- https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
