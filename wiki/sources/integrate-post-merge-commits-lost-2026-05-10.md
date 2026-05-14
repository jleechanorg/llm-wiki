# integrate.sh: Post-Merge Branch Commits Are Lost

**Ingested**: 2026-05-10  
**Type**: feedback / workflow anti-pattern  
**Classification**: Mandatory

## Summary

`integrate.sh` auto-deletes branches that have a merged PR. Any commits pushed to that branch **after** the PR merged are NOT on `main` and are permanently lost when integrate runs.

## Key Rule

Once a PR is merged, open a **new branch** for any follow-up work. Never commit improvements to the merged branch expecting them to reach main.

## Detection

```bash
gh pr list --head $(git branch --show-current) --state merged --json number --jq '.[].number'
# Non-empty output = PR merged = create new branch for improvements
```

## Incident Reference

2026-05-10: `feat/babysit-skill` Gate 5 GraphQL improvement was committed after PR #6850 merged → lost on integrate.
