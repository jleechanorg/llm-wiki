# Scripts Wiki

This wiki documents the scripts found in /Users/jleechan.

---

## Script: claude_backup.sh
- **Path**: /Users/jleechan/claude_backup.sh
- **Type**: Bash
- **Purpose**: Backs up ~/.claude to Dropbox folder with device-specific naming. Runs hourly via cron and sends email alerts on failure.
- **Modified**: 2025-09-21

---

## Script: claude_backup_fixed.sh
- **Path**: /Users/jleechan/claude_backup_fixed.sh
- **Type**: Bash
- **Purpose**: Fixed version of backup script with improved error handling.
- **Modified**: 2025-09-21

---

## Script: claude_backup_test.sh
- **Path**: /Users/jleechan/claude_backup_test.sh
- **Type**: Bash
- **Purpose**: Test script for backup functionality.
- **Modified**: 2025-09-21

---

## Script: claude_backup_fix_test.sh
- **Path**: /Users/jleechan/claude_backup_fix_test.sh
- **Type**: Bash
- **Purpose**: Test script for backup fix functionality.
- **Modified**: 2025-09-21

---

## Script: daily_slack_checkin.sh
- **Path**: /Users/jleechan/daily_slack_checkin.sh
- **Type**: Bash
- **Purpose**: Daily Slack check-in for Gmail + Calendar via gog. Scheduled at 09:00, 12:00, 18:00 via cron.
- **Modified**: 2025-02-18

---

## Script: setup-github-runner.sh
- **Path**: /Users/jleechan/setup-github-runner.sh
- **Type**: Bash
- **Purpose**: GitHub Self-Hosted Runner Setup Script for Claude Bot Commands. Downloads, configures, and starts a GitHub Actions runner.
- **Modified**: 2025-02-06

---

## Script: fetch_pr_feedback.py
- **Path**: /Users/jleechan/fetch_pr_feedback.py
- **Type**: Python
- **Purpose**: Fetches PR feedback from GitHub API including issue comments.
- **Modified**: 2025-02-02

---

## Script: fetch_comments.py
- **Path**: /Users/jleechan/fetch_comments.py
- **Type**: Python
- **Purpose**: Fetches PR comments (issue comments, inline review comments, and reviews) from GitHub API.
- **Modified**: 2025-02-02

---

## Script: fetch_feedback.py
- **Path**: /Users/jleechan/fetch_feedback.py
- **Type**: Python
- **Purpose**: Fetches feedback for PR #4365 from jleechanorg/worldarchitect.ai repository.
- **Modified**: 2025-02-01

---

## Script: test_api_keys.py
- **Path**: /Users/jleechan/test_api_keys.py
- **Type**: Python
- **Purpose**: Tests all LLM API keys from bashrc against their respective APIs.
- **Modified**: 2025-11-16

---

## Script: verify_dev_setup.sh
- **Path**: /Users/jleechan/verify_dev_setup.sh
- **Type**: Bash
- **Purpose**: MacBook Development Environment Verification Script based on WorldArchitect.AI PR #1361 setup guide.
- **Modified**: 2025-08-17

---

## Script: fix-self-hosted-ci.sh
- **Path**: /Users/jleechan/fix-self-hosted-ci.sh
- **Type**: Bash
- **Purpose**: Fixes self-hosted CI runner configuration for Docker and user home directories.
- **Modified**: 2025-03-01

---

## Script: fix-self-hosted-ci-headless.sh
- **Path**: /Users/jleechan/fix-self-hosted-ci-headless.sh
- **Type**: Bash
- **Purpose**: Fixes self-hosted CI runner in headless mode.
- **Modified**: 2025-03-01

---

## Script: daily_email_summary.sh
- **Path**: /Users/jleechan/daily_email_summary.sh
- **Type**: Bash
- **Purpose**: Daily important email summary - gets important & starred unread emails via gog.
- **Modified**: 2025-02-24

---

## Script: gog_auth_helper.sh
- **Path**: /Users/jleechan/gog_auth_helper.sh
- **Type**: Bash
- **Purpose**: GOG Gmail + Calendar OAuth Setup helper script.
- **Modified**: 2025-02-14

---

## Script: merge_k_sorted_lists.py
- **Path**: /Users/jleechan/merge_k_sorted_lists.py
- **Type**: Python
- **Purpose**: LeetCode Hard Problem solution - merges k sorted linked-lists using divide and conquer approach.
- **Modified**: 2025-03-14

---

## Script: test_merge_k_sorted_lists.py
- **Path**: /Users/jleechan/test_merge_k_sorted_lists.py
- **Type**: Python
- **Purpose**: Tests for merge_k_sorted_lists.py implementation.
- **Modified**: 2025-03-14

---

## Script: test-mcp-endpoints.sh
- **Path**: /Users/jleechan/test-mcp-endpoints.sh
- **Type**: Bash
- **Purpose**: Tests MCP (Model Context Protocol) endpoints.
- **Modified**: 2025-10-15

---

## Script: ping_mcp_agents_loop.sh
- **Path**: /Users/jleechan/ping_mcp_agents_loop.sh
- **Type**: Bash
- **Purpose**: Loop script to ping MCP agents.
- **Modified**: 2024-11-04

---

## Script: gemini-with-timeout.sh
- **Path**: /Users/jleechan/gemini-with-timeout.sh
- **Type**: Bash
- **Purpose**: Runs Gemini with timeout wrapper.
- **Modified**: 2025-01-09

---

## Script: start-runner-delayed.sh
- **Path**: /Users/jleechan/start-runner-delayed.sh
- **Type**: Bash
- **Purpose**: Starts GitHub runner with a delay.
- **Modified**: 2025-02-07

---

## Script: test_bashrc.sh
- **Path**: /Users/jleechan/test_bashrc.sh
- **Type**: Bash
- **Purpose**: Tests bashrc configuration.
- **Modified**: 2025-08-17

---

## Project: projects_fake_repo

### Script: main.py
- **Path**: /Users/jleechan/projects_fake_repo/src/main.py
- **Type**: Python
- **Purpose**: Main entry point for fake repo project.
- **Modified**: (check git log)

---

### Script: analyze_git_stats.py
- **Path**: /Users/jleechan/projects_fake_repo/scripts/analyze_git_stats.py
- **Type**: Python
- **Purpose**: Analyzes git statistics.
- **Modified**: (check git log)

---

### Script: infrastructure_common.sh
- **Path**: /Users/jleechan/projects_fake_repo/infrastructure_common.sh
- **Type**: Bash
- **Purpose**: Common infrastructure setup script.
- **Modified**: (check git log)

---

### Script: run_tests_with_coverage.sh
- **Path**: /Users/jleechan/projects_fake_repo/run_tests_with_coverage.sh
- **Type**: Bash
- **Purpose**: Runs tests with coverage reporting.
- **Modified**: (check git log)

---

### Script: setup_email.sh
- **Path**: /Users/jleechan/projects_fake_repo/setup_email.sh
- **Type**: Bash
- **Purpose**: Email setup script.
- **Modified**: (check git log)

---

### Script: push.sh
- **Path**: /Users/jleechan/projects_fake_repo/push.sh
- **Type**: Bash
- **Purpose**: Push script for the repository.
- **Modified**: (check git log)

---

### Script: test_portability.sh
- **Path**: /Users/jleechan/projects_fake_repo/test_portability.sh
- **Type**: Bash
- **Purpose**: Tests script portability.
- **Modified**: (check git log)

---

### Script: setup-github-runner.sh
- **Path**: /Users/jleechan/projects_fake_repo/setup-github-runner.sh
- **Type**: Bash
- **Purpose**: GitHub runner setup for the project.
- **Modified**: (check git log)

---

### Script: loc.sh
- **Path**: /Users/jleechan/projects_fake_repo/loc.sh
- **Type**: Bash
- **Purpose**: Lines of code counter script.
- **Modified**: (check git log)

---

## Project: claude-commands

### Script: test_installation.sh
- **Path**: /Users/jleechan/claude-commands/test_installation.sh
- **Type**: Bash
- **Purpose**: Tests Claude commands installation.
- **Modified**: (check git log)

---

### Script: create_snapshot.sh
- **Path**: /Users/jleechan/claude-commands/create_snapshot.sh
- **Type**: Bash
- **Purpose**: Creates snapshots for backup/recovery.
- **Modified**: (check git log)

---

### Script: schedule_branch_work.sh
- **Path**: /Users/jleechan/claude-commands/schedule_branch_work.sh
- **Type**: Bash
- **Purpose**: Schedules branch work tasks.
- **Modified**: (check git log)

---

### Script: setup-github-runner.sh
- **Path**: /Users/jleechan/claude-commands/setup-github-runner.sh
- **Type**: Bash
- **Purpose**: GitHub runner setup for Claude commands.
- **Modified**: (check git log)

---

### Script: setup_email.sh
- **Path**: /Users/jleechan/claude-commands/setup_email.sh
- **Type**: Bash
- **Purpose**: Email setup for Claude commands.
- **Modified**: (check git log)

---

### Script: coverage.sh
- **Path**: /Users/jleechan/claude-commands/coverage.sh
- **Type**: Bash
- **Purpose**: Runs coverage reports.
- **Modified**: (check git log)

---

### Script: push.sh
- **Path**: /Users/jleechan/claude-commands/push.sh
- **Type**: Bash
- **Purpose**: Git push wrapper script.
- **Modified**: (check git log)

---

### Script: sync_branch.sh
- **Path**: /Users/jleechan/claude-commands/sync_branch.sh
- **Type**: Bash
- **Purpose**: Synchronizes git branches.
- **Modified**: (check git log)

---

### Script: resolve_conflicts.sh
- **Path**: /Users/jleechan/claude-commands/resolve_conflicts.sh
- **Type**: Bash
- **Purpose**: Resolves git merge conflicts.
- **Modified**: (check git log)

---

### Script: run_lint.sh
- **Path**: /Users/jleechan/claude-commands/run_lint.sh
- **Type**: Bash
- **Purpose**: Runs linting checks.
- **Modified**: (check git log)

---

### Script: run_tests_with_coverage.sh
- **Path**: /Users/jleechan/claude-commands/run_tests_with_coverage.sh
- **Type**: Bash
- **Purpose**: Runs tests with coverage.
- **Modified**: (check git log)

---

### Script: loc.sh
- **Path**: /Users/jleechan/claude-commands/loc.sh
- **Type**: Bash
- **Purpose**: Counts lines of code.
- **Modified**: (check git log)

---

### Script: loc_simple.sh
- **Path**: /Users/jleechan/claude-commands/loc_simple.sh
- **Type**: Bash
- **Purpose**: Simple lines of code counter.
- **Modified**: (check git log)

---

### Script: codebase_loc.sh
- **Path**: /Users/jleechan/claude-commands/codebase_loc.sh
- **Type**: Bash
- **Purpose**: Counts codebase lines of code.
- **Modified**: (check git log)

---

### Script: claude_start.sh
- **Path**: /Users/jleechan/claude-commands/claude_start.sh
- **Type**: Bash
- **Purpose**: Starts Claude session.
- **Modified**: (check git log)

---

### Script: create_worktree.sh
- **Path**: /Users/jleechan/claude-commands/create_worktree.sh
- **Type**: Bash
- **Purpose**: Creates git worktrees.
- **Modified**: (check git log)

---

## Project: claude-commands/backup-scripts

### Script: claude_backup_enhanced.sh
- **Path**: /Users/jleechan/claude-commands/backup-scripts/claude_backup_enhanced.sh
- **Type**: Bash
- **Purpose**: Enhanced Claude backup script.
- **Modified**: (check git log)

---

### Script: claude_projects_backup.sh
- **Path**: /Users/jleechan/claude-commands/backup-scripts/claude_projects_backup.sh
- **Type**: Bash
- **Purpose**: Backs up Claude projects.
- **Modified**: (check git log)

---

## Project: claude-commands/orchestration

### Script: cleanup_agents.sh
- **Path**: /Users/jleechan/claude-commands/orchestration/cleanup_agents.sh
- **Type**: Bash
- **Purpose**: Cleans up orchestration agents.
- **Modified**: (check git log)

---

### Script: install_local.sh
- **Path**: /Users/jleechan/claude-commands/orchestration/install_local.sh
- **Type**: Bash
- **Purpose**: Installs orchestration locally.
- **Modified**: (check git log)

---

### Script: monitor_agents.sh
- **Path**: /Users/jleechan/claude-commands/orchestration/monitor_agents.sh
- **Type**: Bash
- **Purpose**: Monitors orchestration agents.
- **Modified**: (check git log)

---

### Script: start_monitor.sh
- **Path**: /Users/jleechan/claude-commands/orchestration/start_monitor.sh
- **Type**: Bash
- **Purpose**: Starts agent monitoring.
- **Modified**: (check git log)

---

## Project: claude-commands/automation

### Script: install_jleechanorg_automation.sh
- **Path**: /Users/jleechan/claude-commands/automation/install_jleechanorg_automation.sh
- **Type**: Bash
- **Purpose**: Installs jleechanorg PR automation.
- **Modified**: (check git log)

---

### Script: install_launchd_automation.sh
- **Path**: /Users/jleechan/claude-commands/automation/install_launchd_automation.sh
- **Type**: Bash
- **Purpose**: Installs launchd automation.
- **Modified**: (check git log)

---

### Script: restore_crontab.sh
- **Path**: /Users/jleechan/claude-commands/automation/restore_crontab.sh
- **Type**: Bash
- **Purpose**: Restores crontab configuration.
- **Modified**: (check git log)

---

### Script: simple_pr_batch.sh
- **Path**: /Users/jleechan/claude-commands/automation/simple_pr_batch.sh
- **Type**: Bash
- **Purpose**: Simple PR batch processing.
- **Modified**: (check git log)

---

### Script: comment_validation.sh
- **Path**: /Users/jleechan/claude-commands/automation/comment_validation.sh
- **Type**: Bash
- **Purpose**: Validates PR comments.
- **Modified**: (check git log)

---

### Script: generate_cron_workflow_evidence.sh
- **Path**: /Users/jleechan/claude-commands/automation/evidence/generate_cron_workflow_evidence.sh
- **Type**: Bash
- **Purpose**: Generates cron workflow evidence.
- **Modified**: (check git log)

---

## Project: claude-commands/claude_scripts

### Script: install_mcp_servers.sh
- **Path**: /Users/jleechan/claude-commands/claude_scripts/install_mcp_servers.sh
- **Type**: Bash
- **Purpose**: Installs MCP servers.
- **Modified**: (check git log)

---

### Script: mcp_common.sh
- **Path**: /Users/jleechan/claude-commands/claude_scripts/mcp_common.sh
- **Type**: Bash
- **Purpose**: Common MCP utilities.
- **Modified**: (check git log)

---

### Script: mcp_dual_background.sh
- **Path**: /Users/jleechan/claude-commands/claude_scripts/mcp_dual_background.sh
- **Type**: Bash
- **Purpose**: Runs MCP in dual background mode.
- **Modified**: (check git log)

---

### Script: start_mcp_production.sh
- **Path**: /Users/jleechan/claude-commands/claude_scripts/start_mcp_production.sh
- **Type**: Bash
- **Purpose**: Starts MCP production server.
- **Modified**: (check git log)

---

### Script: slack_notify.sh
- **Path**: /Users/jleechan/claude-commands/claude_scripts/slack_notify.sh
- **Type**: Bash
- **Purpose**: Sends Slack notifications.
- **Modified**: (check git log)

---

### Script: secondo-cli.sh
- **Path**: /Users/jleechan/claude-commands/claude_scripts/secondo-cli.sh
- **Type**: Bash
- **Purpose**: Segundo CLI wrapper.
- **Modified**: (check git log)

---

## Project: claude-commands/claude_mcp

### Script: claude_mcp.sh
- **Path**: /Users/jleechan/claude-commands/claude_mcp.sh
- **Type**: Bash
- **Purpose**: Claude MCP launcher.
- **Modified**: (check git log)

---

## Additional Python Scripts in claude-commands

### Script: claude_md_updater.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/claude_md_updater.py
- **Type**: Python
- **Purpose**: Updates CLAUDE.md files.
- **Modified**: (check git log)

---

### Script: query_patterns.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/query_patterns.py
- **Type**: Python
- **Purpose**: Queries patterns from database.
- **Modified**: (check git log)

---

### Script: update_patterns.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/update_patterns.py
- **Type**: Python
- **Purpose**: Updates pattern database.
- **Modified**: (check git log)

---

### Script: response_enhancement.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/response_enhancement.py
- **Type**: Python
- **Purpose**: Enhances responses with AI.
- **Modified**: (check git log)

---

### Script: confidence_tracker.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/confidence_tracker.py
- **Type**: Python
- **Purpose**: Tracks confidence scores.
- **Modified**: (check git log)

---

### Script: mcp_stdio_wrapper.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/mcp_stdio_wrapper.py
- **Type**: Python
- **Purpose**: MCP stdio wrapper.
- **Modified**: (check git log)

---

### Script: auto_correction_detector.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/auto_correction_detector.py
- **Type**: Python
- **Purpose**: Detects auto-corrections.
- **Modified**: (check git log)

---

### Script: conversation_learning_integration.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/conversation_learning_integration.py
- **Type**: Python
- **Purpose**: Integrates conversation learning.
- **Modified**: (check git log)

---

### Script: pattern_extractor.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/pattern_extractor.py
- **Type**: Python
- **Purpose**: Extracts patterns from conversations.
- **Modified**: (check git log)

---

### Script: memory_learn.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/memory_learn.py
- **Type**: Python
- **Purpose**: Memory learning integration.
- **Modified**: (check git log)

---

### Script: enhanced_learn.py
- **Path**: /Users/jleechan/claude-commands/claude_scripts/enhanced_learn.py
- **Type**: Python
- **Purpose**: Enhanced learning utilities.
- **Modified**: (check git log)

---

## Utility Scripts

### Script: hello.py
- **Path**: /Users/jleechan/hello.py
- **Type**: Python
- **Purpose**: Simple test script.
- **Modified**: 2025-03-11

---

### Script: test_hello.py
- **Path**: /Users/jleechan/test_hello.py
- **Type**: Python
- **Purpose**: Test for hello.py.
- **Modified**: 2025-03-11

---
