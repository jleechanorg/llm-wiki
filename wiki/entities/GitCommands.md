---
title: "GitCommands"
type: entity
tags: [module, security, git]
sources: [subprocess-security-vulnerabilities-copilot-utils]
last_updated: 2026-04-08
---

## Description
Module in copilot utils that provides git operations (check_merge_tree, get_current_branch, get_merge_conflicts). Originally contained shell injection vulnerability when using shell=True in subprocess calls.

## Key Methods
- check_merge_tree - checks for merge conflicts
- get_current_branch - gets current git branch
- get_merge_conflicts - retrieves merge conflicts

## Security Fix
Fixed by replacing shell=True with list-based arguments and shell=False in all subprocess.run calls.

## Related
- [[ShellInjection]]
- [[SubprocessSecurity]]
