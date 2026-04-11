---
title: "fix: GitHub Actions GCP vars use ${{ vars.GCP_PROJECT_ID }} syntax"
type: source
tags: [github, pr, jleechanorg-claude-commands]
sources: []
date: 2026-03-26
pr_url: https://github.com/jleechanorg/claude-commands/pull/288
pr_number: 288
pr_repo: jleechanorg/claude-commands
---

## Summary
## Summary
- Fixes 4 Critical CodeRabbit findings: `$GCP_PROJECT_ID` used as literal string in YAML `env:` and `with:` blocks instead of proper `${{ vars.GCP_PROJECT_ID }}` syntax
- 8 files, 12 changes total
- Shell `run:` blocks (gcloud commands) are unaffected — shell variables are correct there

## Files changed
| File | Fix |
|------|-----|
| `workflows/mcp-smoke-tests.yml` | env GCP_PROJECT |
| `workflows/auto-deploy-dev.yml` | env GCP_PROJECT |
| `workflows/pr-cleanup.yml` | env GCP_PROJEC...

## Key Changes
- 3 commit(s) in this PR
- 8 file(s) changed

- Merged: 2026-03-26

## Commit Messages
1. Fresh Claude Commands Export 2026-03-26
  
  🚨 DIRECTORY EXCLUSIONS APPLIED:
  - Excluded: analysis/, claude-bot-commands/, coding_prompts/, prototype/
  - These project-specific directories are filtered from exports per requirements
  
  ✅ EXPORT CONTENTS:
  - 📋 Commands: 244 command definitions with content filtering
  - 📎 Hooks: 52 Claude Code hooks with nested structure
  - 🚀 Scripts: 19 reusable automation scripts (scripts/ directory)
  - 🧠 Skills: 89 shared knowledge references (.claude/skills/)
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
2. fix: replace hardcoded worldarchitect references with parameterized values
  
  - Fix doubled $PROJECT_ROOT/$PROJECT_ROOT in benchg-ts.md
  - Fix default repo jleechanorg/your-project.com in base.py
  - Parameterize automation log dirs: worldarchitect-automation → ${PROJECT_NAME}-automation
  - Parameterize domain refs: worldarchitect.ai → ${PROJECT_DOMAIN:-your-project}.com
  - Parameterize project refs: worldarchitect → ${PROJECT_NAME:-your-project}
  - Fix browser.md chrome script and playwright skill paths
  - Fix playwright.md and history.md project-specific paths
  - Fix codex_cli_tasks.py and utils.py config paths
  - Fix install scripts and cron template paths
  - Fix test fixture repo references
3. fix: use \${{ vars.GCP_PROJECT_ID }} in GitHub Actions YAML contexts
  
  GCP_PROJECT_ID was used as a literal string in env: and with: blocks,
  causing Critical failures at runtime. Shell run: blocks are unaffected.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `workflows/auto-deploy-dev.yml`
- `workflows/deploy-dev.yml`
- `workflows/deploy-production.yml`
- `workflows/mcp-manual-smoke-tests.yml`
- `workflows/mcp-smoke-tests.yml`
- `workflows/pr-cleanup.yml`
- `workflows/pr-preview.yml`
- `workflows/test-email-notification.yml`

## Review Notes
1. @coderabbitai review

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **2...

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check PR status and review comments
gh pr view 288 --repo jleechanorg/claude-commands -...

6. 
### 💡 Codex Review

https://github.com/jleechanorg/claude-commands/blob/59ab6e2317213fdb9f88b78ad28eb6d900259d21/workflows/deploy-production.yml#L57
**<sub><sub>![P0 Badge](https://img.shields.io/badge/P0-red?style=flat)</sub></sub>  Export GCP_PROJECT_ID before calling gcloud config**

This step n...

7. <h3>Greptile Summary</h3>

This PR fixes 12 instances across 8 workflow files where `$GCP_PROJECT_ID` was used as a literal string in GitHub Actions `env:` and `with:` blocks instead of the proper expression syntax `${{ vars.GCP_PROJECT_ID }}`. Without this fix, the GCP project ID would be passed as...

8. @coderabbitai full review

9. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

10. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Full review triggered.

</details>

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 288 --repo jleechanorg/claude-commands --json state,r...

