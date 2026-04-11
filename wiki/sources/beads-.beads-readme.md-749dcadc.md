---
title: "Beads - AI-Native Issue Tracking"
type: source
tags: [beads, issue-tracking, ai-development, git-integration, cli-tools]
sources: []
source_file: .beads/readme.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Beads is an AI-native issue tracking tool that lives directly in your codebase alongside your code. Perfect for AI coding agents and developers who want issues close to their code — no web UI required, everything works through the CLI and integrates seamlessly with git.

## Key Claims

- **Git-Native Storage**: Issues stored in `.beads/issues.jsonl` and synced like code
- **AI-Friendly CLI**: Built specifically for AI-assisted development workflows
- **Branch-Aware**: Issues can follow your branch workflow
- **Auto-Sync**: Automatically syncs with your commits
- **Offline Capable**: Works offline, syncs when you push

## Essential Commands

```bash
# Create new issues
bd create "Add user authentication"

# View all issues
bd list

# View issue details
bd show <issue-id>

# Update issue status
bd update <issue-id> --status in_progress
bd update <issue-id> --status done

# Sync with git remote
bd sync
```

## Why Beads for AI Development?

- CLI-first interface works seamlessly with AI coding agents
- No context switching to web UIs
- Issues live in your repo, right next to your code
- Fast, lightweight, and stays out of the way
- Automatic sync with git commits
- Intelligent JSONL merge resolution

## Connections

- [[WorldArchitect.AI]] — could use Beads for issue tracking instead of current system
- [[AI-Usage-Tracker]] — similar CLI-first AI development tool pattern

## Contradictions

None — this is a new tool entry with no conflicting wiki content.