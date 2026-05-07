# CI Auto-Commit Cycle Causes Evidence Provenance Staleness

**Date**: 2026-05-05  
**Type**: feedback/Anti-Pattern  
**Source**: PR #6796 Gate 6 failures

## Summary

Every push to a PR triggers the "Generate PR Design Docs" CI workflow which auto-commits docs, advancing HEAD beyond the SHA captured in `evidence/pr-N/metadata.json`. This causes Gate 6 provenance checks to fail.

## Pattern

Evidence captured at commit A → push → CI auto-commits docs → HEAD = A+1 → metadata.json.head_commit ≠ live HEAD → Gate 6 FAIL

## Mitigation

1. Wait for CI auto-commits to settle after final push
2. Update metadata.json `head_commit` to the settled HEAD SHA
3. Document the CI auto-commit pattern in evidence/README.md

## References

- PR [#6796](https://github.com/jleechanorg/worldarchitect.ai/pull/6796)
- CI workflow: `.github/workflows/generate-pr-design-docs.yml`
