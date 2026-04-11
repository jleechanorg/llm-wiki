---
title: "Claude Commands Export 2026-03-14: Directory Exclusions Applied"
type: source
tags: [github, pr, jleechanorg-claude-commands]
sources: []
date: 2026-03-14
pr_url: https://github.com/jleechanorg/claude-commands/pull/270
pr_number: 270
pr_repo: jleechanorg/claude-commands
---

## Summary
**🚨 AUTOMATED EXPORT** with directory exclusions applied per requirements.

## 🎯 Directory Exclusions Applied
This export **excludes** the following project-specific directories:
- ❌ `analysis/` - Project-specific analytics and reporting
- ❌ `claude-bot-commands/` - Project-specific bot implementation
- ❌ `coding_prompts/` - Project-specific AI prompting templates
- ❌ `prototype/` - Project-specific experimental code

## ✅ Export Contents
- **📋 242 Commands**: Complete workflow orchestration sys...

## Key Changes
- 14 commit(s) in this PR
- 31 file(s) changed
- Large diff (20+ files)
- Merged: 2026-03-14

## Commit Messages
1. Fresh Claude Commands Export 2026-03-14
  
  🚨 DIRECTORY EXCLUSIONS APPLIED:
  - Excluded: analysis/, claude-bot-commands/, coding_prompts/, prototype/
  - These project-specific directories are filtered from exports per requirements
  
  ✅ EXPORT CONTENTS:
  - 📋 Commands: 242 command definitions with content filtering
  - 📎 Hooks: 50 Claude Code hooks with nested structure
  - 🚀 Scripts: 19 reusable automation scripts (scripts/ directory)
  - 🧠 Skills: 90 shared knowledge references (.claude/skills/)
  - ⚙️  Workflows: 21 GitHub Actions workflow examples (require integration)
  - 🤖 Orchestration: Multi-agent task delegation system (core components only)
  - 📚 Documentation: Complete README with installation guide and adaptation examples
  
  🔄 CONTENT TRANSFORMATIONS:
  - mvp_site/ → $PROJECT_ROOT/ (generic project paths)
  - worldarchitect.ai → your-project.com (generic domain)
  - jleechan → $USER (generic username)
  - TESTING=true vpython → TESTING=true python (generic test commands)
  
  Starting MANUAL INSTALLATION: Copy commands to .claude/commands/ and hooks to .claude/hooks/
  
  ⚠️ Reference export - requires adaptation for other projects
  🤖 Generated with Claude Code CLI
2. Fix auth wrapper Firebase project and environment variable mismatches
  
  - auth-worldai.mjs: Pass --project worldarchitecture-ai flag and use VITE_FIREBASE_* env vars
  - auth-aiuniverse.mjs: Pass --project ai-universe-b3551 flag and use VITE_AI_UNIVERSE_FIREBASE_* env vars
  
  Both wrappers now correctly authenticate against their intended Firebase projects by:
  1. Passing the --project flag to auth-cli.mjs so it uses the correct project config
  2. Setting environment variables with the correct prefix that auth-cli.mjs expects
3. [copilot] fix: address bot review comments on PR #270
  
  - auth-cli.mjs: correct path in usage examples from scripts/ to .claude/scripts/
  - auth-cli.mjs: fix help text to show ai-universe-b3551 (not ai-universe) matching KNOWN_PROJECTS keys
  - auth-cli.mjs: replace nonexistent setup-firebase-config.sh reference with env var instruction
  - ralph.md: add numeric validation for iteration count arg (matching pair.md pattern)
  - codex_cli_tasks.py: log diff byte count instead of content to prevent code leaking into CI logs
  - workflows/hook-tests.yml: update step name from hardcoded "Python 3.11" to generic "Set up Python"
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
4. [copilot] fix: resolve CRITICAL/BLOCKING PR #270 review comments
  
  - codex_cli_tasks.py: wrap _remote_branch_exists call at line 931 in
    try/except to prevent uncaught RuntimeError aborting PR creation on
    transient network failures (greptile #2934498097, cursor #2934755557)
  - auth-worldai.mjs: fix placeholder error message to "World Architecture AI"
    (greptile #2934498122)
  - auth-cli.mjs: fix refresh token Content-Type to x-www-form-urlencoded
    per Firebase REST API spec (coderabbit #2934497160)
  - auth-cli.mjs: add ai-universe alias to KNOWN_PROJECTS (coderabbit #2934497154)
  - ralph_benchmark_parallel.md: remove duplicate -p flag from claudem calls
    (coderabbit #2934497144, #2934497149)
  - pair.md: fix non-Claude CLI path to use ~/ralph/ralph-pair.sh
    (coderabbit #2934497139, cursor #2934755549)
  - test_exportcommands.py: remove f-prefix from strings with no placeholders
    to fix F541 lint violations (coderabbit #2934497150, #2934497152)
  - coderabbit-ping-on-push.yml: add timeout-minutes: 10 to job
    (coderabbit #2934510774)
  - mcp-smoke-tests.yml: add timeout-minutes: 10 to preview-smoke-tests job
    and align step timeout (coderabbit #2934510777)
  - README.md: disambiguate v1.1.0 archive entry from current release stats
    (coderabbit #2934510772)
  - scripts/loc_simple.sh: fix misleading All File Types wording
    (coderabbit #2934497180)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. [copilot] fix: remove --force from new-branch push to prevent race-condition overwrites
  
  When the branch does not yet exist remotely, --force would silently overwrite
  a branch created concurrently by another runner. A plain push fails fast on
  collision, letting the caller handle the race instead of losing data.
  
  Resolves CodeRabbit critical comment #2934758636 (line 689).
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
6. [copilot] fix: address bot review feedback — heredoc expansion, PYTHONPATH, worktree cleanup assertions
  
  - conversation-history-sparse.md: change <<'PY' to <<PY so $PWD expands
    in the heredoc body (cursor bot: medium severity, heredoc quoted delimiter)
  - test_packaging_integration.py: prepend new path to existing PYTHONPATH
    instead of replacing it, preventing flaky CI across setups (coderabbit: major)
  - test_codex_cli_tasks.py: add explicit worktree cleanup assertions to
    happy-path and fetch-failure test cases so regressions in cleanup logic
    are caught (coderabbit: minor x3)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
7. Fix: Wrap _remote_branch_exists call in apply_and_push with exception handler
  
  Adds try/except wrapper to _remote_branch_exists call in apply_and_push
  method to handle RuntimeError from transient network failures, matching
  the pattern already used in create_pr_from_diff. This ensures graceful
  degradation by treating the branch as new when remote check fails,
  instead of aborting the entire operation.
8. [copilot] fix: inline import removal, path consistency, placeholder text
  
  - Remove forbidden inline `import ast` from test_claude_scripts_mjs_files_are_exported
    (unused and violates module-level import policy)
  - Fix pair.md usage examples to use ~/ralph/ralph-pair.sh (matching actual
    script code on lines 64/67/72; relative path was misleading)
  - Fix auth-worldai.mjs JSDoc header: replace "Your Project" placeholder with
    "World Architecture AI"
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
9. [copilot] chore: add .claude/scheduled_tasks.lock to .gitignore
10. [copilot] fix: project-aware MCP URL and correct skills path in loc_simple
  
  - auth-cli.mjs: add mcpUrl to each project config; resolve productionMcpUrl
    from ACTIVE_PROJECT.mcpUrl so testMcp() hits the right backend when
    --project worldarchitecture-ai is used instead of hardcoded AI Universe URL
  - loc_simple.sh: change ./skills/ to ./.claude/skills/ so Skills & Tooling
    bucket counts files that actually exist
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
11. [copilot] fix: replace --force with --force-with-lease in apply_and_push fallback path
  
  The apply_and_push method used --force when branch_on_remote=True but updated_existing=False
  (the "fell back to new branch" path). This could blindly overwrite concurrent changes. Switch
  to --force-with-lease which fails safely if remote ref has moved since last fetch.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
12. [copilot] fix: plug debug log leak, custom project mcpUrl fallback, auth HTML branding
  
  - codex_cli_tasks.py: replace diff content preview log with byte-count only on retry failure, consistent with the policy comment already present for the first failure path
  - auth-cli.mjs getProjectConfig: add mcpUrl field to custom project objects so line 121 productionMcpUrl fallback uses a project-specific URL instead of the hardcoded ai-universe-backend URL
  - auth-cli.mjs getAuthHtml: replace hardcoded "AI Universe" strings in title, h1, and description with ACTIVE_PROJECT.name so all projects get correct branding
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
13. [copilot] fix: move inline import re to module level, clarify hook-tests Python step name
  
  Comment: https://github.com/jleechanorg/claude-commands/pull/270#discussion_r2934774642
  Comment: https://github.com/jleechanorg/claude-commands/pull/270#discussion_r2934494092
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
14. [copilot] fix: correct test mock for temp worktree cleanup path, simplify duplicate push_cmd
  
  - test_success_without_conflicts: remove spurious git-worktree-remove mock entry and
    fix last-call assertion; temp codex worktrees use shutil.rmtree, not subprocess
  - create_pr_from_diff push_cmd: collapse duplicate if/else branches into single
    force-with-lease command when branch_on_remote is True
  
  Comment: https://github.com/jleechanorg/claude-commands/pull/270#discussion_r2934806005
  Comment: https://github.com/jleechanorg/claude-commands/pull/270#discussion_r2934806006
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.claude/commands/exportcommands.py`
- `.claude/commands/pair.md`
- `.claude/commands/ralph.md`
- `.claude/commands/ralph_benchmark_parallel.md`
- `.claude/commands/ralph_iteration.md`
- `.claude/commands/ralph_pair_iteration.md`
- `.claude/commands/tests/test_exportcommands.py`
- `.claude/hooks/git-header.sh`
- `.claude/scripts/auth-aiuniverse.mjs`
- `.claude/scripts/auth-cli.mjs`
- `.claude/scripts/auth-worldai.mjs`
- `.claude/skills/conversation-history-sparse.md`
- `.gitignore`
- `CLAUDE.md`
- `README.md`
- `automation/jleechanorg_pr_automation/jleechanorg_pr_monitor.py`
- `automation/jleechanorg_pr_automation/openai_automation/codex_cli_tasks.py`
- `automation/jleechanorg_pr_automation/tests/test_codex_cli_tasks.py`
- `automation/jleechanorg_pr_automation/tests/test_dirty_repo_handling.py`
- `automation/jleechanorg_pr_automation/tests/test_model_parameter.py`
- `automation/jleechanorg_pr_automation/tests/test_packaging_integration.py`
- `automation/pyproject.toml`
- `orchestration/pyproject.toml`
- `scripts/loc_simple.sh`
- `workflows/README.md`
- `workflows/coderabbit-ping-on-push.yml`
- `workflows/coverage.yml`
- `workflows/hook-tests.yml`
- `workflows/mcp-smoke-tests.yml`
- `workflows/self-hosted-mvp-shard1.yml`
- `workflows/test.yml`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: review paused by coderabbit.ai -->

> [!NOTE]
> ## Reviews paused
> 
> It looks like this branch is under active development. To avoid overwhelming you with review comments due to an influx...

2. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details
gh pr view 270 --repo jleechanorg/claude-commands --json state,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,comments,reviews,title,...

4. <h3>Greptile Summary</h3>

This PR delivers an automated export of Claude commands with several meaningful improvements to the underlying codebase: a new multi-project Firebase browser-based auth CLI (`auth-cli.mjs` + two project-specific wrappers), git/worktree automation hardening in `codex_cli_ta...

5. [AI responder]
## Copilot Response - All Serious Comments Addressed

**Coverage:** 6/6 CRITICAL/BLOCKING bot comments resolved
**CI status:** CodeRabbit PASS, Greptile PASS, Cursor Bugbot NEUTRAL (skipping)
**Commit:** 1b676962

### CRITICAL/BLOCKING Fixes

**1. auth-worldai.mjs / auth-aiuniverse.mj...

6. [AI responder]
## Copilot Response - All Comments Addressed

**Coverage:** 18/44 comments addressed (11 fixed in code, 5 deferred/architecture, 28 acknowledged)
**Files modified:** 10 files in commit 3f69422a
**CI status:** Greptile=pass, CodeRabbit=pass, Cursor Bugbot=skipping

---

### CRITICAL/BL...

7. [AI responder]
## Copilot Response - Follow-up Pass

**New issues found:** 1 Critical (CodeRabbit #2934758636, posted 05:42Z, not addressed in prior pass)
**Fixed:** 1 (committed ec79e734)
**CI status:** CodeRabbit=pending, Cursor Bugbot=pending, Greptile=pending (all reviews in progress on new push...

8. [AI responder]
## Copilot Response - Follow-up Pass

**New issues found:** 8 (across coderabbit, cursor, greptile bots)
**Fixed:** 3 (actionable IMPORTANT-severity items)
**CI status:** pending (Cursor Bugbot + Greptile Review still running)

### Fixes implemented (commit 5fff9620)

| File | Issue |...

9. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 270 --repo jleechanorg/claude-commands --json state,m...

11. [AI responder]
## Copilot Response - Pass 20260313

**New issues addressed:** 9 comments reviewed
**Fixed:** 3 | **Deferred:** 2 | **Not Done (invalid):** 4
**CI:** Checks pending (f25fd8ed merged by Cursor agent before this pass)

### Fixes (commit 70e44d4e)

**1. Forbidden inline import removed** ...

12. [AI responder]
## Copilot Response - Pass 20260313-2309

### New comments since last pass (after 2026-03-14T06:05:35Z)

All 4 new bot comments were from the 05:55–05:57 cycle (before last AI response timestamp). Addressed below:

---

### Fixes implemented (commit 425d7216)

| File | Issue | Action ...

13. [AI responder] Addressed 3 new inline review comments (commit 584b6460):

**cursor[bot] - codex_cli_tasks.py:649 (Low)** - Debug log on retry failure path leaked diff content (first 500 chars) contradicting the policy comment at line 627. Replaced with byte-count-only log consistent with stated poli...

14. [AI responder]
## Copilot Response - All Comments Addressed

**Coverage:** 53/53 comments addressed (14 fixed, 7 deferred, 2 acknowledged, 30 not-done/invalid)
**This run:** 35 new, 18 carried forward from prior runs
**Files modified:** `automation/jleechanorg_pr_automation/openai_automation/codex_c...

15. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 270 --repo jleechanorg/claude-commands --json state,m...

17. [AI responder]
## Copilot Response - Pass 20260314 (Final)

**Coverage:** 37/37 new comments addressed (1 fixed, 27 not-done/already-fixed, 6 deferred, 4 acknowledged) + 18 carried forward from prior runs
**This run:** 37 new comments processed; 18 carried forward (all previously Fixed/Acknowledged)...

18. [AI responder]
## Copilot Response - Follow-up (4 new comments since last summary)

**New comments processed:** 4 (posted after 06:22Z)
**Fixed:** 2 | **Deferred:** 2
**Files modified:** `automation/jleechanorg_pr_automation/tests/test_codex_cli_tasks.py`, `automation/jleechanorg_pr_automation/opena...

19. [AI responder]
## Copilot Response - All New Comments Addressed

**Coverage:** 7/7 new comments addressed (1 fixed [prior run], 0 deferred, 2 deferred [carried forward], 4 not done [already implemented])
**This run:** 7 new, 54 carried forward from prior runs
**Files modified:** None (all new commen...

20. @coderabbit all good?

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 270 --repo jleechanorg/claude-commands --json state,m...

22. @coderabbit all good?

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 270 --repo jleechanorg/claude-commands --json state,m...

24. [AI responder]
## Copilot Response - Pass 20260314-pass2 (4 new comments)

**New comments processed:** 4 | **Resolved:** 4 | **Commit:** 7a71c238

### BLOCKING Issues Fixed

| File | Line | Issue | Status |
|------|------|-------|--------|
| `tests/test_codex_cli_tasks.py` | 924 | `git worktree remo...

