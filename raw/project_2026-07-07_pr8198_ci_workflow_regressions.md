---
name: pr8198-ci-workflow-regressions
description: Two workflow-syntax regressions broke CI repo-wide on all branches until PR
metadata: 
  node_type: memory
  type: project
  bead: rev-j9so3 (closed)
  originSessionId: cfee38e7-2623-45d6-b7e1-87ba5e3a8d31
---

Two independent one-file CI bugs landed on `main` within a day of each other and broke CI **repo-wide, on every branch** (workflow files are always loaded from `main`'s copy for `issue_comment`/`workflow_dispatch` triggers). Fixed together in [PR #8198](https://github.com/jleechanorg/worldarchitect.ai/pull/8198), merged 2026-07-07T03:18:05Z at commit `42b963099b92cabe187659e005b2c7565372395e`. Bead `rev-j9so3` (closed).

**Bug 1 — `#` comment inside a GitHub Actions `if: >-` expression is a parse error, not a comment.**
Introduced in `0586722c2b` (PR #8192, "block GitHub App bots from auto-firing /smoke"). `.github/workflows/mcp-smoke-tests.yml` line 48 had `#` comment lines placed *inside* the multi-line `if: >-` folded-scalar expression body. GitHub Actions expression syntax has no comment support, so the `#` character is parsed as literal expression text → lexer error → the entire workflow fails to start (`startup_failure`) on **every** branch, since `issue_comment`/`workflow_dispatch` triggers always load the workflow definition from `main`. This starved Green Gate Gate 8 (smoke) fleet-wide.
- **Why:** `#` is a valid YAML comment marker only in the surrounding YAML; once inside the string content of an `if: >-` folded scalar, it becomes part of the expression that the Actions expression lexer must parse, and that lexer has no comment syntax at all.
- **Verification:** `actionlint .github/workflows/mcp-smoke-tests.yml` → `got unexpected character '#' while lexing expression, expecting 'a'..'z', ... [expression]` at line 48 on the broken main copy; clean on the fixed branch.
- **Fix:** move the comments above the `if:` key (outside the expression), byte-identical expression otherwise.

**Bug 2 — reusable workflow inheriting `${{ github.workflow }}-${{ github.ref }}` self-cancels its own parent under `workflow_call`.**
Introduced in `2545575c82` (PR #8175, a 21-workflow-wide concurrency-group rollout). `.github/workflows/deploy-dev.yml` is the one workflow in that batch that is also invoked via `workflow_call` (from `auto-deploy-dev.yml`). Inside a `workflow_call`, `github.workflow` resolves to the **caller's** workflow name, not the callee's — so the reusable `deploy-dev.yml` and its caller `auto-deploy-dev.yml` ended up sharing one `cancel-in-progress` concurrency group. The nested (callee) run's start event cancelled its own in-progress parent run. Every Auto-Deploy Dev run since 2026-07-05T22:29:14Z failed with the `deploy` job silently absent from the job list and `smoke-tests` skipped (regression confirmed via run-history diff: pre-#8175 run 28403965704 green with a `deploy` job present; post-#8175 runs 28757060652/28769882561/28837876526 missing the job entirely).
- **Why:** `github.workflow` is caller-scoped by design under `workflow_call` — a concurrency-group expression built from it is only safe on workflows that are never called by another workflow. #8175 applied the same 21-workflow pattern uniformly without auditing which of the 21 were `workflow_call`-able.
- **Fix:** literal group name `deploy-dev-${{ github.ref }}` (drops the caller-polluted `github.workflow` token) — keeps #8175's intended superseded-run cancellation for direct dispatches without colliding with the parent's group.
- **Audit note:** deploy-dev.yml was confirmed as the *only* `workflow_call`-able workflow among the 21 touched by #8175, so no sibling workflow has the same collision — this was a single-file fix, not a repo-wide follow-up.

**How to apply going forward:**
1. Never place `#` inside an Actions expression string (`if:`, `env:` value expressions, etc.) — comments must sit on their own YAML line outside the expression body. `actionlint` catches this; run it on any workflow touching multi-line `if: >-` blocks before merge.
2. Before applying a blanket concurrency-group pattern across many workflows, grep for `workflow_call:` in each target file — any reusable workflow needs a literal (non-`github.workflow`) group name, or an explicit `${{ inputs.xxx }}`-based discriminator, to avoid caller/callee collision.
3. Workflow-file bugs merged to `main` are repo-wide outages, not branch-scoped — `issue_comment`/`workflow_dispatch` triggers always read `main`'s copy regardless of which branch/PR fired them. Treat any `.github/workflows/**` change as prod-critical and actionlint-verify before merge.

See also [[project_2026-07-07_jeff_ubuntu_oom_runner_starvation]] and [[feedback_2026-07-07_sidekick_branch_scoped_state_and_commit_often]] from the same overnight session.
