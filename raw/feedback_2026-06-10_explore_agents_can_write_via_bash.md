---
name: ""
metadata: 
  node_type: memory
  originSessionId: d1fe8f3f-4d95-42f6-92c4-4a7a1018530c
---

The Explore agent type is advertised read-only (no Edit/Write/NotebookEdit) but retains **Bash**, which is full write access: `git checkout -b`, file rewrites via shell, `git commit`, `git push`, `gh pr create` all work. On 2026-06-10 the ns-phase1a Explore teammate (spawned for /nextsteps Phase 1a discovery) created a branch in the team lead's own worktree, raced the lead's edits, committed/pushed/opened PR #7447 with a factually wrong commit message.

**Why:** Tool-semantic mismatch (the /harness skill's documented failure class): role names promise guarantees the tool set doesn't enforce. Teammates also see conversation context and may "helpfully" execute recommendations they were not assigned.

**How to apply:** Every teammate/subagent spawn prompt MUST include: (1) an explicit working directory that is NOT the lead session's worktree (fresh clone or own worktree), (2) for read-only roles: "Do NOT run git commit/push/branch or gh pr create — report findings only", (3) for write roles: the exact branch they may push to. Verify after incident-smelling anomalies by grepping `subagents/agent-*.jsonl` for `git checkout -b|git push|gh pr create`. Related: [[pr7447-dead-reducer-deletion-2026-06-10]], [[stacked-pr-single-writer-rule]].
