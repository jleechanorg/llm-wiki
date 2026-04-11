---
title: "Beads Development Container"
type: source
tags: [beads, devcontainer, development-environment, go, vscode]
sources: []
source_file: beads-.devcontainer-readme.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

The beads Development Container provides a fully-configured development environment for the beads project (a distributed git-backed graph issue tracker). Supports both GitHub Codespaces and VS Code Remote Containers with Go 1.23, bd CLI installation from source, and automatic git hooks setup.

## Key Claims

- **Go 1.23 Environment**: Full Go development environment with version 1.23
- **bd CLI Installation**: Automatically built from source (`go build ./cmd/bd`) and installed to `/usr/local/bin/bd`
- **Git Hooks Auto-Install**: Git hooks from `examples/git-hooks/` are installed automatically
- **Dual Deployment Options**: Works with both GitHub Codespaces and VS Code Remote Containers
- **Non-Interactive Setup**: Uses `bd init --quiet` for non-interactive initialization

## Verification Commands

```bash
bd --version   # Check bd is installed
bd ready       # Check for ready tasks
bd stats       # View project stats
```

## Connections

- [[Beads]] — the project this devcontainer configures
- [[Development Environment]] — related to MacBook dev setup

## Contradictions

None identified.