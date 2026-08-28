---
title: "Skill archive dependency and migration closure"
type: source
tags: [agent-skills, archival, dependency-closure, transactional-migration, cross-platform]
date: 2026-08-27
source_file: raw/feedback_2026-08-27_skill_archive_dependency_and_migration_closure.md
last_updated: 2026-08-27
sources:
  - https://github.com/jleechanorg/jleechan-skills/pull/376
---

## Summary

PR #376 established that observed zero-use is only a candidate filter: retained active skill contracts can still depend on apparently unused slash commands. Moving installed packages out of discovery is a transactional migration requiring dependency closure, collision preflight, serialization, exact destination identity, rollback, interrupt cleanup, and BSD/GNU parity.

## Key Claims

- Scan retained active skills and commands for dependencies before archival.
- Completion requires archived names to be absent from active discovery roots and preserved recoverably.
- Verify that the exact source filesystem identity reached the exact destination.
- Exercise platform differences explicitly when BSD and GNU flags differ.

## Key Quotes

> "Historical zero-use is only the first filter; dependency closure is the ship gate."

## Connections

- [[SkillArchiveDependencyClosure]] — archive-selection and migration discipline.
- [[SkillStaleness]] — instruction catalogs can drift from live mechanisms.
- [[AgentSkills]] — the discovery surface affected by archival.
- [[EvidenceBasedVerification]] — exact-head and cross-platform proof.

