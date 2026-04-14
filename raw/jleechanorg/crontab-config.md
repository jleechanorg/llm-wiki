# Crontab Configuration for WorldArchitect.AI Automation

This document describes the crontab configuration for automated PR monitoring and Codex task processing.

## Current Schedule

```bash
# Set PATH to include necessary binaries
PATH=/Users/jleechan/.pyenv/shims:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Run PR monitoring (comment-only mode) every 2 hours
0 * * * * jleechanorg-pr-monitor --max-prs 10 >> /Users/jleechan/Library/Logs/worldarchitect-automation/jleechanorg_pr_monitor.log 2>&1

# Run comment validation workflow every 30 minutes - asks AI bots to review PRs
*/30 * * * * jleechanorg-pr-monitor --comment-validation --max-prs 10 >> /Users/jleechan/Library/Logs/worldarchitect-automation/comment_validation.log 2>&1

# Run Codex automation (first 50 tasks) every hour, 15 minutes after PR monitor
15 * * * * jleechanorg-pr-monitor --codex-update >> /Users/jleechan/Library/Logs/worldarchitect-automation/codex_automation.log 2>&1

# Run Codex API automation (using API instead of browser) every hour, 30 minutes after PR monitor
30 * * * * jleechanorg-pr-monitor --codex-api --codex-apply-and-push >> /Users/jleechan/Library/Logs/worldarchitect-automation/codex_automation_api.log 2>&1

# Run orchestrated PR fixes (conflicts + failing checks) every 30 minutes
*/30 * * * * jleechanorg-pr-monitor --fixpr --max-prs 10 --cli-agent gemini,cursor >> /Users/jleechan/Library/Logs/worldarchitect-automation/jleechanorg_pr_monitor.log 2>&1

# Backup Claude conversations to Dropbox every 4 hours
0 */4 * * * "/Users/jleechan/.local/bin/claude_backup_cron.sh" "/Users/jleechan/Library/CloudStorage/Dropbox" 2>&1
```

## Workflow Descriptions

### PR Monitoring (Every 2 hours at :00)
- **Command**: `jleechanorg-pr-monitor --max-prs 10`
- **Purpose**: Comment-only mode, posts validation comments
- **Log**: `jleechanorg_pr_monitor.log`

### Comment Validation (Every 30 minutes)
- **Command**: `jleechanorg-pr-monitor --comment-validation --max-prs 10`
- **Purpose**: Requests reviews from @coderabbit-ai, @greptileai, @bugbot, @copilot
- **Log**: `comment_validation.log`

### Codex Browser Automation (Every hour at :15)
- **Command**: `jleechanorg-pr-monitor --codex-update`
- **Purpose**: Process first 50 Codex tasks via browser automation
- **Log**: `codex_automation.log`

### Codex API Automation (Every hour at :30)
- **Command**: `jleechanorg-pr-monitor --codex-api --codex-apply-and-push`
- **Purpose**: Process Codex tasks via API, apply diffs, and push to remote
- **Schedule**: Runs 15 minutes after browser automation
- **Log**: `codex_automation_api.log`

### FixPR Workflow (Every 30 minutes)
- **Command**: `jleechanorg-pr-monitor --fixpr --max-prs 10 --cli-agent gemini,cursor`
- **Purpose**: Fix PR conflicts and failing checks using AI agents
- **Log**: `jleechanorg_pr_monitor.log`

### Claude Backup (Every 4 hours at :00)
- **Command**: `claude_backup_cron.sh`
- **Purpose**: Backup Claude conversations to Dropbox
- **Log**: stderr redirected

## Package Requirements

Both automation packages must be installed from PyPI (not editable):

```bash
pip install jleechanorg-orchestration==0.1.39
pip install jleechanorg-pr-automation==0.2.124
```

**Why PyPI installation?**
- Cron jobs run in isolated environments
- Editable installs can point to wrong worktree directories
- PyPI packages have stable, versioned code

## Log Files Location

All logs are stored in:
```
/Users/jleechan/Library/Logs/worldarchitect-automation/
```

## Maintenance

### Checking Cron Status
```bash
crontab -l  # View current crontab
```

### Viewing Recent Logs
```bash
tail -f /Users/jleechan/Library/Logs/worldarchitect-automation/codex_automation_api.log
```

### Testing Before Deployment
Always test automation commands manually before adding to crontab:
```bash
jleechanorg-pr-monitor --codex-api --codex-apply-and-push --no-act
```

## Recent Changes

### 2026-02-08
- Added `--codex-api --codex-apply-and-push` workflow at :30
- Runs 15 minutes after `--codex-update` (browser automation)
- Provides API-based alternative to browser automation
- Published automation 0.2.124 with API support

### Package Versions
- orchestration: 0.1.39 (includes CLI validation)
- automation: 0.2.124 (includes --codex-api flag)
