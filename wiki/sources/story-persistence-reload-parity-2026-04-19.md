---
title: "Story persistence & reload parity (harness) — 2026-04-19"
type: source
tags: [worldarchitect, harness, persistence, planning_block, reload, level-up]
date: 2026-04-19
source_file: raw/story-persistence-reload-parity-2026-04-19.md
---

## Summary

A **harness-level tenet** for WorldArchitect.AI: **story/turn persistence must preserve user-visible `planning_block` and choice state across full page reload** unless a field is explicitly **session-only** and documented. Agents must not “fix” misleading UI by **`pop` / strip at save** without reload round-trip evidence. This responds to analysis of **PR #6376** (god-mode `planning_block` strip) and user correction that **reload must show the same planning UI** as the live turn.

## Key claims

- **Round-trip parity** is a product trust invariant for anything shown as choices/modals.
- **Destructive persistence workarounds** (delete structured fields to silence history confusion) default **wrong**; prefer **provenance** (`is_god_mode`, actor) + **client rendering**.
- Repo harness adds `.claude/skills/story-persistence-reload-parity.md` and a `CLAUDE.md` pointer.

## Key quotes

> "Fix misleading UI" by pop/delete/strip at persistence without a reload test is presumed wrong until proven otherwise. — harness skill

## Connections

- [[WorldArchitect.AI]] — campaign story persistence, Firestore turns
- [[Level-up]] — `planning_block` / `rewards_box` pairing debates
- [[PR 6376]] — concrete trigger for this harness (god-mode strip); verify product intent before merge
