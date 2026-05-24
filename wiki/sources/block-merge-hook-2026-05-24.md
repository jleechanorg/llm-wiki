# block-merge.sh — Hard Block on All Claude Merge Paths

**Date**: 2026-05-24  
**Project**: worldarchitect.ai  
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/7066

## Summary

`.claude/hooks/block-merge.sh` is a PreToolUse hook that hard-blocks all merge API calls from Claude. Human must run `! gh pr merge <N> --squash` directly.

## Blocked patterns

- `gh pr merge ...`
- `gh api repos/.../pulls/N/merge`
- `curl/wget .../pulls/N/merge`

AskUserQuestion + command call still triggers the block — the check is on command text, not conversation context.

## Rule

After `/green` confirms all gates PASS, output:
> "Run `! gh pr merge <N> --squash` in your terminal."

Then stop. Do not retry any merge path.

## Why

PRs #6161 and #6240 were merged by agents without human approval. The hook prevents polish/automation loops from auto-merging.

## See also

- [[worldai-test-cache-default-read-write]]
