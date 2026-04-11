---
title: "Contributor Namespace Isolation Design"
type: source
tags: [beads, contributor-isolation, namespace, git-routing, issue-tracking, pr-pollution]
sources: []
date: 2025-12-30
source_file: docs/ROUTING.md (design issue bd-umbf)
last_updated: 2026-04-07
---

## Summary

Design for preventing contributor personal issues from polluting upstream PRs when using beads-the-tool on beads-the-project. The solution automatically routes issues to separate databases based on git remote URL (SSH = maintainer, HTTPS = contributor), preventing personal TODO tracking from appearing in project diffs.

## Key Claims

- **Recursion Problem**: When beads-the-project uses beads-the-tool, contributors' personal issues in `.beads/issues.jsonl` leak into PR diffs
- **Auto-Routing Solution**: Maintainers (SSH access) → `./.beads/` (project), Contributors (HTTPS fork) → `~/.beads-planning/` (personal)
- **Implementation Gap**: Role detection and routing calculation are implemented, but `bd create` still writes to `./.beads/` instead of routing to target repo
- **Four Approaches Analyzed**: Prefix-based namespaces, separate BEADS_DIR, visibility flags, and auto-routing (recommended)

## Key Quotes

> "When a contributor creates a PR, the PR diff includes their personal issues in `.beads/issues.jsonl`" — Problem statement

> "Zero-friction for contributors, automatic based on git remote inspection" — Approach 4 verdict

## Connections

- [[Beads]] — the issue tracking system this design addresses
- [[Beads Attribution — beads-merge]] — related beads infrastructure

## Contradictions

None identified — this is a new design document for a feature not yet fully implemented.