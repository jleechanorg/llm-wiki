---
name: block-merge-hook-requires-human-run
description: block-merge.sh blocks all merge paths from Claude; human must run ! gh pr merge <N> --squash directly
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 3f10d684-e8e3-43ea-b664-00db2975d3a9
---

## block-merge.sh is a hard block on all merge API calls

`.claude/hooks/block-merge.sh` is a PreToolUse hook wired in `.claude/settings.json`. It blocks:
- `gh pr merge ...`
- `gh api repos/.../pulls/N/merge`
- `curl/wget .../pulls/N/merge`

The check is on the bash **command text**, not the conversation context. Saying "MERGE APPROVED" in chat and then trying to run the command still triggers the block.

**Rule**: After `/green` shows all gates PASS, output the instruction and stop:
> "Run `! gh pr merge <N> --squash` in your terminal to complete the merge."

Do NOT retry with `gh api`, `curl`, or any other route. All paths are blocked.

**Why**: PRs #6161 and #6240 were merged without human approval. The hook was added to prevent agentic polish loops from auto-merging.

**References**: PR #7066, `.claude/hooks/block-merge.sh`
