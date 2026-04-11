---
title: "Claude Commands Export 2026-03-18: Directory Exclusions Applied"
type: source
tags: [github, pr, jleechanorg-claude-commands]
sources: []
date: 2026-03-18
pr_url: https://github.com/jleechanorg/claude-commands/pull/271
pr_number: 271
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
- **📋 243 Commands**: Complete workflow orchestration sys...

## Key Changes
- 1 commit(s) in this PR
- 90 file(s) changed
- Large diff (20+ files)
- Merged: 2026-03-18

## Commit Messages
1. Fresh Claude Commands Export 2026-03-18
  
  🚨 DIRECTORY EXCLUSIONS APPLIED:
  - Excluded: analysis/, claude-bot-commands/, coding_prompts/, prototype/
  - These project-specific directories are filtered from exports per requirements
  
  ✅ EXPORT CONTENTS:
  - 📋 Commands: 243 command definitions with content filtering
  - 📎 Hooks: 52 Claude Code hooks with nested structure
  - 🚀 Scripts: 20 reusable automation scripts (scripts/ directory)
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

## Files Changed
- `.claude/commands/_copilot_modules/commentfetch.py`
- `.claude/commands/archreview.md`
- `.claude/commands/claw.md`
- `.claude/commands/coderabbit.md`
- `.claude/commands/cr.md`
- `.claude/commands/debug-protocol.md`
- `.claude/commands/design.md`
- `.claude/commands/execute.md`
- `.claude/commands/exportcommands.py`
- `.claude/commands/goal.md`
- `.claude/commands/guidelines.md`
- `.claude/commands/learn.md`
- `.claude/commands/localexportcommands.md`
- `.claude/commands/memory.md`
- `.claude/commands/tests/test_commentreply_summary.py`
- `.claude/commands/worldai-usage-email.md`
- `.claude/hooks/git-header.sh`
- `.claude/hooks/mem0_recall.py`
- `.claude/hooks/mem0_save.py`
- `.claude/hooks/tests/test_git_header.sh`
- `.claude/hooks/tests/test_git_header_statusline.py`
- `.claude/scripts/auth-cli.mjs`
- `.claude/scripts/check-pr-status.sh`
- `README.md`
- `automation/comment_validation.sh`
- `automation/jleechanorg_pr_automation/jleechanorg_pr_monitor.py`
- `automation/jleechanorg_pr_automation/openai_automation/codex_cli_tasks.py`
- `automation/jleechanorg_pr_automation/orchestrated_pr_runner.py`
- `automation/jleechanorg_pr_automation/tests/test_codex_cli_tasks.py`
- `automation/jleechanorg_pr_automation/tests/test_comment_validation.py`
- `automation/jleechanorg_pr_automation/tests/test_packaging_integration.py`
- `codex_hooks.json`
- `codex_hooks/git-header.sh`
- `codex_hooks/mem0_recall.py`
- `codex_hooks/mem0_save.py`
- `codex_hooks/pre-exec-hook.sh`
- `codex_hooks/stop-git-header-json.sh`
- `codex_skills/ai-universe-auth/SKILL.md`
- `codex_skills/ai-universe-httpie/SKILL.md`
- `codex_skills/ai-universe-second-opinion-workflow/SKILL.md`
- `codex_skills/autonomous-execution/SKILL.md`
- `codex_skills/bashrc-credential-guard/SKILL.md`
- `codex_skills/browser-testing-ocr-validation/SKILL.md`
- `codex_skills/build-test-lint-autopilot/SKILL.md`
- `codex_skills/chrome-localhost3000-usage/SKILL.md`
- `codex_skills/chrome-superpowers-reference/SKILL.md`
- `codex_skills/claude-code-schema-validation/SKILL.md`
- `codex_skills/claude-code-settings-maintenance/SKILL.md`
- `codex_skills/code-centralization/SKILL.md`
- `codex_skills/conversation-history-sparse/SKILL.md`
- `codex_skills/copilot-pr-processing/SKILL.md`
- `codex_skills/copilot-pr-processing/tests/test_skill_md_pair_integration.py`
- `codex_skills/coverage-analysis/SKILL.md`
- `codex_skills/dice-authenticity-standards/SKILL.md`
- `codex_skills/dice-real-mode-tests/SKILL.md`
- `codex_skills/dice-roll-audit/SKILL.md`
- `codex_skills/end2end-testing/SKILL.md`
- `codex_skills/evidence-standards/SKILL.md`
- `codex_skills/file-justification/SKILL.md`
- `codex_skills/firebase-prod-campaigns/SKILL.md`
- `codex_skills/gcp-deployment/SKILL.md`
- `codex_skills/gcp-deployments/SKILL.md`
- `codex_skills/gemini-3-api/SKILL.md`
- `codex_skills/gemini-code-execution-json-mode/SKILL.md`
- `codex_skills/git-branch-tracking/SKILL.md`
- `codex_skills/github-cli-reference/SKILL.md`
- `codex_skills/integration-verification/SKILL.md`
- `codex_skills/llm-json-schema-documentation/SKILL.md`
- `codex_skills/llm-prompt-engineering/SKILL.md`
- `codex_skills/mcp-agent-mail/SKILL.md`
- `codex_skills/oracle-browser-usage/SKILL.md`
- `codex_skills/playwright-mcp-manual-interaction/SKILL.md`
- `codex_skills/pr-workflow-manager/SKILL.md`
- `codex_skills/secondo-dependencies/SKILL.md`
- `codex_skills/superpowers-using-git-worktrees/SKILL.md`
- `codex_skills/test-api-keys-ai-universe/SKILL.md`
- `codex_skills/testing-infrastructure/SKILL.md`
- `codex_skills/unified-logging/SKILL.md`
- `codex_skills/worldai-auth/SKILL.md`
- `codex_skills/worldai-browser-login/SKILL.md`
- `codex_skills/worldai-mcp-server-usage/SKILL.md`
- `codex_skills/worldarchitect-codebase-sherpa/SKILL.md`
- `codex_skills/worldarchitect-local-debugging/SKILL.md`
- `scripts/check-pr-status.sh`
- `scripts/integrate.sh`
- `scripts/loc_simple.sh`
- `workflows/coderabbit-ping-on-push.yml`
- `workflows/hook-tests.yml`
- `workflows/mcp-smoke-tests.yml`
- `workflows/pr-preview.yml`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: failure by coderabbit.ai -->

> [!CAUTION]
> ## Review failed
> 
> The pull request is closed.

<!-- end of auto-generated comment: failure by coderabbit.ai -->

<details>
<summary>ℹ️ Recen...

2. <h3>Greptile Summary</h3>

This automated export PR ships native mem0 memory integration (recall/save hooks for both Claude Code and Codex), an upstream-tracking improvement to `git-header.sh`, a `run_single_pr` helper in the orchestration runner, thread-safety improvements in the PR monitor, and a ...

