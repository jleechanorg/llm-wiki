---
title: "Administrative State Poisoning"
type: concept
tags: [architecture, state-machine, admin, worldarchitect, anti-pattern]
---

A class of bug where administrative tools (God Mode, Template Injection, debug shortcuts) leave behind **stale state flags** from a previous modal, trapping the game session in a ghost state.

## Three-Step Mechanism

1. **Normal Flow** — When a game mode ends (combat, character creation, level-up), the system runs cleanup: `in_combat=False`, `character_creation_in_progress=False`, etc.
2. **Admin Shortcut** — Administrative features bypass the normal flow to fix or skip something. They jump over the standard state machine entry/exit protocols.
3. **Poisoning** — Because the shortcut skipped cleanup, dangling `True` flags persist. The player is trapped in a modal that no longer exists.

## Concrete Example (PR #6844)

Player is in combat (`in_combat=True`). God Mode heals them and exits. But God Mode bypassed the combat exit handler, so `in_combat=True` persists. The game is now stuck in a "combat trap" — the player can't proceed because the system thinks combat is still active.

## Why It Recurs

Developers focus on making the shortcut work (heal the player, skip character creation, inject a template) and forget the system might be in the middle of something else. Each admin override was written in isolation without considering which other modals might be active.

## Fix: Declarative Contracts

Every admin shortcut must declare what it `resets`, `sets`, `preserves`, and `requires_clean` — see [[AdminOverrideContract]]. Runtime enforcement via `_ensure_modal_exclusivity()` catches any remaining violations.

## Discovered In

- PR #6844 — God Mode combat trap
- PR #6842 — Character Creation modal trap from template injection
- PR #6845 — Harness guardrails added to AGENTS.md/CLAUDE.md

## Related

- [[AdminOverrideContract]] — the fix pattern (declarative cleanup manifests)
- [[ModalIntersection]] — concurrent modal corruption (the broader category)
- [[StaleFlag]] — the symptom
- [[DuplicatedConstantLists]] — a co-discovered anti-pattern from the same analysis
