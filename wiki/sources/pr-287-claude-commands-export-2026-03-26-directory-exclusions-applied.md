---
title: "Claude Commands Export 2026-03-26: Directory Exclusions Applied"
type: source
tags: [github, pr, jleechanorg-claude-commands]
sources: []
date: 2026-03-26
pr_url: https://github.com/jleechanorg/claude-commands/pull/287
pr_number: 287
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
- **📋 244 Commands**: Complete workflow orchestration sys...

## Key Changes
- 2 commit(s) in this PR
- 83 file(s) changed
- Large diff (20+ files)
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

## Files Changed
- `.claude/commands/_copilot_modules/base.py`
- `.claude/commands/automation-publish.md`
- `.claude/commands/automation.md`
- `.claude/commands/benchg-ts.md`
- `.claude/commands/benchg.md`
- `.claude/commands/browser.md`
- `.claude/commands/cerebras/extract_conversation_context.py`
- `.claude/commands/exportcommands.py`
- `.claude/commands/playwright.md`
- `.claude/scripts/start_mcp_server.sh`
- `.claude/settings.json`
- `.claude/skills/automation-audit.md`
- `.claude/skills/end2end-testing.md`
- `.claude/skills/modal-agent-pattern.md`
- `.claude/skills/testing-infrastructure.md`
- `README.md`
- `automation/AUTOMATION_SAFETY_LIMITS.md`
- `automation/JLEECHANORG_AUTOMATION.md`
- `automation/OPENCLAW_MISSION_CONTROL_INTEGRATION_DESIGN.md`
- `automation/README.md`
- `automation/comment_validation.sh`
- `automation/cron_entry.txt`
- `automation/crontab.template`
- `automation/evidence/generate_cron_workflow_evidence.sh`
- `automation/install.sh`
- `automation/install_jleechanorg_automation.sh`
- `automation/install_launchd_automation.sh`
- `automation/jleechanorg_pr_automation/__init__.py`
- `automation/jleechanorg_pr_automation/automation_safety_manager.py`
- `automation/jleechanorg_pr_automation/automation_safety_wrapper.py`
- `automation/jleechanorg_pr_automation/automation_utils.py`
- `automation/jleechanorg_pr_automation/jleechanorg_pr_monitor.py`
- `automation/jleechanorg_pr_automation/orchestrated_pr_runner.py`
- `automation/jleechanorg_pr_automation/tests/test_atomic_race_condition.py`
- `automation/jleechanorg_pr_automation/tests/test_automation_over_running_reproduction.py`
- `automation/jleechanorg_pr_automation/tests/test_automation_safety_limits.py`
- `automation/jleechanorg_pr_automation/tests/test_codex_cli_tasks.py`
- `automation/jleechanorg_pr_automation/tests/test_concurrent_limit_one.py`
- `automation/jleechanorg_pr_automation/tests/test_cursor_bot_round2_bugs.py`
- `automation/jleechanorg_pr_automation/tests/test_cursor_bot_round3_bugs.py`
- `automation/jleechanorg_pr_automation/tests/test_cursor_bug_fixes.py`
- `automation/jleechanorg_pr_automation/tests/test_fixpr_prompt.py`
- `automation/jleechanorg_pr_automation/tests/test_orchestrated_pr_runner.py`
- `automation/jleechanorg_pr_automation/tests/test_pr_monitor_eligibility.py`
- `automation/jleechanorg_pr_automation/tests/test_pr_monitor_feedback_loop.py`
- `automation/jleechanorg_pr_automation/tests/test_pr_targeting.py`
- `automation/jleechanorg_pr_automation/tests/test_regression_draft_pr_fixpr_bypass.py`
- `automation/jleechanorg_pr_automation/tests/test_safety_limits_false_rejection.py`
- `automation/jleechanorg_pr_automation/tests/test_workspace_dispatch_missing_dir.py`
- `automation/jleechanorg_pr_automation/utils.py`
- `automation/openclaw_mctrl_entry.sh`
- `automation/pyproject.toml`
- `automation/tests/test_install_native_scheduler.sh`
- `orchestration/A2A_DESIGN.md`
- `orchestration/__init__.py`
- `orchestration/a2a_agent_wrapper.py`
- `orchestration/a2a_integration.py`
- `orchestration/a2a_monitor.py`
- `orchestration/agent_monitor.py`
- `orchestration/design.md`
- `orchestration/recovery_coordinator.py`
- `workflows/README.md`
- `workflows/auto-deploy-dev.yml`
- `workflows/claude-processor.yml`
- `workflows/coderabbit-ping-on-push.yml`
- `workflows/coverage.yml`
- `workflows/daily-campaign-report.yml`
- `workflows/deploy-dev.yml`
- `workflows/deploy-production.yml`
- `workflows/doc-size-check.yml`
- `workflows/hook-tests.yml`
- `workflows/mcp-smoke-tests.yml`
- `workflows/pr-cleanup.yml`
- `workflows/pr-preview.yml`
- `workflows/presubmit.yml`
- `workflows/pypi-publish-testing-utils.yml`
- `workflows/pypi-publish.yml`
- `workflows/self-hosted-mvp-shard1.yml`
- `workflows/styleguide-compliance-gate.yml`
- `workflows/test-deployment.yml`
- `workflows/test-email-notification.yml`
- `workflows/test-self-hosted-runner.yml`
- `workflows/test.yml`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **4...

2. <h3>Greptile Summary</h3>

This PR introduces a new `exportcommands.py` tool that clones the `claude-commands` repository and publishes a filtered snapshot of the Claude Code asset directories (commands, hooks, agents, scripts, skills, orchestration, automation) with a new PR. It also refactors hard...

3. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

4. ## 🧠 Evidence Review — PR #287

**Verdict: FAIL** (Confidence: HIGH — 3 hard blockers confirmed via live API)

### Verdict Table

| Criterion | Status | Artifact |
|---|---|---|
| CI passing | ✅ STRONG | 7 check runs all SUCCESS |
| No conflicts | ⚠️ WEAK | mergeable=true, mergeable_state unstable (...

5. ## /er Evidence Review: INCONCLUSIVE (Premature)

**Reviewer**: evidence-reviewer (Claude) | **Confidence**: HIGH

### 6-Criteria Green Audit

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | CI Passing | **FAIL** | Greptile Review `in_progress` — blocking required check |
| 2 | MERGEA...

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status and mergability
gh pr view 287 --repo jleechanorg/claude-commands --json ...

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status
gh pr view 287 --repo jleechanorg/claude-commands --json title,state,mergeable,mergeStateStatus,reviewDecision,reviews,statusCheckRollup 2>...

9. ## Fixed: Critical GitHub Actions variable syntax

Fixed all 4 Critical CodeRabbit findings. The issue: `$GCP_PROJECT_ID` was used as a literal string in YAML `env:` and `with:` blocks instead of the proper `${{ vars.GCP_PROJECT_ID }}` syntax.

Files corrected (8 files, 12 changes):
- `workflows/mcp...

