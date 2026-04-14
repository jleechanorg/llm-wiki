# PR #6: Claude Commands Export 2025-09-10: Directory Exclusions Applied

**Repo:** jleechanorg/claude-commands
**Merged:** 2025-09-11
**Author:** jleechan2015
**Stats:** +9416/-3399 in 92 files

## Summary
(none)

## Raw Body
**🚨 AUTOMATED EXPORT** with directory exclusions applied per requirements.

## 🎯 Directory Exclusions Applied
This export **excludes** the following project-specific directories:
- ❌ `analysis/` - Project-specific analytics and reporting
- ❌ `automation/` - Project-specific automation scripts
- ❌ `claude-bot-commands/` - Project-specific bot implementation
- ❌ `coding_prompts/` - Project-specific AI prompting templates
- ❌ `prototype/` - Project-specific experimental code

## ✅ Export Contents
- **📋 156 Commands**: Complete workflow orchestration system
- **📎 30 Hooks**: Essential Claude Code workflow automation
- **🚀 17 Infrastructure Scripts**: Development environment management
- **🤖 Orchestration System**: Core multi-agent task delegation (WIP prototype)
- **📚 Complete Documentation**: Setup guide with adaptation examples

## Manual Installation
From your project root:
```bash
mkdir -p .claude/{commands,hooks,agents}
cp -R commands/. .claude/commands/
cp -R hooks/. .claude/hooks/
cp -R agents/. .claude/agents/
# Optional infrastructure scripts
cp -n infrastructure-scripts/* .
```

## 🔄 Content Filtering Applied
- **Generic Paths**: mvp_site/ → \$PROJECT_ROOT/
- **Generic Domain**: worldarchitect.ai → your-project.com
- **Generic User**: jleechan → \$USER
- **Generic Commands**: TESTING=true vpython → TESTING=true python

## ⚠️ Reference Export
This is a filtered reference export. Commands may need adaptation for specific environments, but Claude Code excels at helping customize them for any workflow.

---
🤖 **Generated with [Claude Code](https://claude.ai/code)**

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- New Features
  - Automated PR comment reply posting tool.
  - Revamped PR status dashboard with detailed CI analysis.
  - “Light mode” for faster Cerebras runs.
  - New Red–Green debug command and Memory command.
  - New utility scripts: coverage, LOC, worktree, push, snapshot, runner/email setup.
  
