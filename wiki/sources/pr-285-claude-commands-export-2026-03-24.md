---
title: "Claude Commands Export 2026-03-24"
type: source
tags: [github, pr, jleechanorg-claude-commands]
sources: []
date: 2026-03-24
pr_url: https://github.com/jleechanorg/claude-commands/pull/285
pr_number: 285
pr_repo: jleechanorg/claude-commands
---

## Summary
Automated export. Source files overwrite target; target-only files preserved.

Changed:  146 files changed, 10778 insertions(+), 3558 deletions(-)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Medium risk because it replaces the export implementation with a new `exportcommands.sh` that performs git/rsync/filtering and could accidentally publish or mutate files if misconfigured. Most other changes are additive command definitions and portability tweaks.
> 
> **Overview**
> Introduce...

## Key Changes
- 1 commit(s) in this PR
- 100 file(s) changed
- Large diff (20+ files)
- Merged: 2026-03-24

## Commit Messages
1. export: 2026-03-24 —  146 files changed, 10778 insertions(+), 3558 deletions(-)

## Files Changed
- `.claude/commands/_copilot_modules/base.py`
- `.claude/commands/agento_report.md`
- `.claude/commands/agentor.md`
- `.claude/commands/antig.md`
- `.claude/commands/auton.md`
- `.claude/commands/benchg-ts.md`
- `.claude/commands/cancel-ralph.md`
- `.claude/commands/cerebras/extract_conversation_context.py`
- `.claude/commands/claw.md`
- `.claude/commands/conv.md`
- `.claude/commands/converge.md`
- `.claude/commands/copilot_inline_reply_example.sh`
- `.claude/commands/copilotc.md`
- `.claude/commands/exportcommands.py`
- `.claude/commands/exportcommands.sh`
- `.claude/commands/fixprc.md`
- `.claude/commands/gen.md`
- `.claude/commands/gene.md`
- `.claude/commands/harness.md`
- `.claude/commands/orchc.md`
- `.claude/commands/orchconverge.md`
- `.claude/commands/pairv2.md`
- `.claude/commands/plan.md`
- `.claude/commands/polish.md`
- `.claude/commands/ralph-loop.md`
- `.claude/commands/roadmap_orch.md`
- `.claude/commands/roadmapo.md`
- `.claude/commands/team-claude.md`
- `.claude/commands/testi.sh`
- `.claude/commands/tests/run_tests.sh`
- `.claude/commands/validate-e2e.md`
- `.claude/hooks/codex-notify-git-header.sh`
- `.claude/hooks/git-header.sh`
- `.claude/hooks/hooks.plugin.json`
- `.claude/hooks/pr-green-check.py`
- `.claude/hooks/protect-worktrees.sh`
- `.claude/hooks/tests/.claude/hooks/tests/test_speculation_detection.sh`
- `.claude/hooks/tests/test_git_header_statusline.py`
- `.claude/memory_templates/enhanced_memory_integration.md`
- `.claude/memory_templates/high_quality_memory_patterns.md`
- `.claude/memory_templates/quality_comparison_examples.md`
- `.claude/scripts/agento-report.sh`
- `.claude/scripts/copilot_execute.py`
- `.claude/scripts/integration/test_pair_command_execution.md`
- `.claude/scripts/integration/test_pair_real_integration.py`
- `.claude/scripts/mcp_smoke_test.sh`
- `.claude/scripts/pair_execute.py`
- `.claude/scripts/requirements-dev.txt`
- `.claude/scripts/secondo_campaign_analysis_iteration_005.md`
- `.claude/scripts/start_mcp_server.sh`
- `.claude/scripts/tests/test_pair_execute.py`
- `.claude/scripts/tests/test_pair_monitor.py`
- `.claude/scripts/tests/test_pair_orchestration.py`
- `.claude/scripts/tests/test_task_impl.py`
- `.claude/scripts/tests/test_task_smoke.py`
- `.claude/settings.json`
- `.claude/skills/agento_report.md`
- `.claude/skills/antigravity-computer-use/SKILL.md`
- `.claude/skills/ao-session-monitor.md`
- `.claude/skills/ao-spawn-gate.md`
- `.claude/skills/automation-audit.md`
- `.claude/skills/auton.md`
- `.claude/skills/claude-code-computer-use/SKILL.md`
- `.claude/skills/cmux-socket-control.md`
- `.claude/skills/design.md`
- `.claude/skills/end2end-testing.md`
- `.claude/skills/harness-engineering.md`
- `.claude/skills/mem0.md`
- `.claude/skills/modal-agent-pattern.md`
- `.claude/skills/pairv2-usage.md`
- `.claude/skills/symphony-daemon/SKILL.md`
- `.claude/skills/testing-infrastructure.md`
- `.claude/skills/tmux-video-evidence.md`
- `.claude/skills/validation-gate.md`
- `.claude/skills/verify-secrets-backup.md`
- `.claude/skills/video-caption.md`
- `README.md`
- `automation/AUTOMATION_SAFETY_LIMITS.md`
- `automation/JLEECHANORG_AUTOMATION.md`
- `automation/OPENCLAW_MISSION_CONTROL_INTEGRATION_DESIGN.md`
- `automation/README.md`
- `automation/comment_validation.sh`
- `automation/evidence/generate_cron_workflow_evidence.sh`
- `automation/install.sh`
- `automation/install_jleechanorg_automation.sh`
- `automation/install_launchd_automation.sh`
- `automation/jleechanorg_pr_automation/__init__.py`
- `automation/jleechanorg_pr_automation/automation_safety_manager.py`
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

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: failure by coderabbit.ai -->

> [!CAUTION]
> ## Review failed
> 
> Pull request was closed or merged during review

<!-- end of auto-generated comment: failure by coderabbit.ai -->

<!-- wa...

2. <h3>Greptile Summary</h3>

This is a large automated export (146 files, ~10K line delta) that primarily sanitizes project-specific strings (`worldarchitect.ai`, `/Users/jleechan/`, `mvp_site/`, etc.) into generic placeholders, and introduces several new hooks and tooling improvements.

Key changes:
...

