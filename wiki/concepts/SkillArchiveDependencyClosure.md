---
title: "Skill Archive Dependency Closure"
type: concept
tags: [agent-skills, dependency-analysis, archival, migration-safety]
date: 2026-08-27
last_updated: 2026-08-27
sources:
  - ../sources/feedback-2026-08-27-skill-archive-dependency-and-migration-closure.md
---

## Definition

**Skill Archive Dependency Closure** means inactivity evidence may nominate a package for archival but cannot authorize the move. Every retained active command, skill contract, policy pointer, and test must be checked for dependency on the candidate.

## Migration contract

An installed-home archive migration must remove discovery, preserve a recoverable sibling archive, preflight destinations and parents, serialize and avoid clobbering, verify exact filesystem identity, roll back partial work, release locks on interruption, and pass BSD/macOS plus GNU/Linux parity tests.

## Canonical incident

PR #376 initially nominated ten commands. Active skill contracts still invoked `/efficiency`, `/engplan`, and `/evidence-coverage`, so the final archive retained those three and archived seven commands. Exact-head review also drove the installer from shape checks to transactional identity verification.

## Connections

- [[SkillStaleness]]
- [[AgentSkills]]
- [[EvidenceBasedVerification]]
- [[ModuleDependencyValidation]]

