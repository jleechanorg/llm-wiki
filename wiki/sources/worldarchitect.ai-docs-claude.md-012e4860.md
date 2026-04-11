---
title: "CLAUDE.md - Directory Documentation Standards"
type: source
tags: [documentation, standards, adr, process, development]
sources: []
source_file: worldarchitect.ai-docs-claude.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

A comprehensive documentation standard guide covering directory documentation structure, writing guidelines, lifecycle management, and integration with development workflows. This document serves as the root documentation reference for the WorldArchitect.AI project, referencing project-wide conventions and providing templates for feature documentation, API documentation, and archival management.

## Key Claims

- **Documentation Inheritance**: Documents inherit from root project documentation via `../CLAUDE.md` references
- **Structural Organization**: Docs organized into ADRs, feature development evidence (tdd_evidence, campaign_creation_evidence), process documentation (branch-guidelines, skills), and technical specifications (PR-specific directories)
- **Five Documentation Standards**: Clarity (for new developers), Evidence-Based (screenshots/logs/examples), Actionable (specific steps/commands), Version Control (dated changes), Cross-References (linked related docs)
- **Feature Documentation Pattern**: requirements.md, implementation.md, testing_evidence/, performance_metrics.md, lessons_learned.md structure
- **Documentation Lifecycle**: Creation (pre-merge), Updates (breaking changes), Review (code review), Archival (outdated docs)
- **Quality Assurance**: Links validated in CI/CD, screenshots updated on UI changes, code examples tested, coverage tracked
- **Archive Management**: Quarterly review, screenshot updates, broken link fixes, redundancy consolidation

## Key Quotes

> "See also: [../CLAUDE.md](../CLAUDE.md) for complete project protocols and development guidelines."

## Connections

- [[Slash Commands Documentation]] — references slash command documentation standards
- [[GitHub Actions Cost Optimization]] — CI/CD documentation cost analysis
- [[LLM-First State Management Plan]] — feature development evidence pattern
- [[Visual Content Validation - E2E Data Flow]] — testing evidence documentation pattern

## Contradictions

- None identified — this is meta-documentation about standards, not conflicting claims