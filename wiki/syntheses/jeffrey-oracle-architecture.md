---
title: "jeffrey-oracle-architecture"
type: synthesis
tags: [jeffrey, oracle, architecture, decision-framework]
sources: [jeffrey-oracle, JeffreyWorkingStyle, ArchitecturalBoundaries, CleanArchitecture]
last_updated: 2026-04-11
---

# Jeffrey Oracle: Architecture Decisions

Specialized oracle for software architecture: new services, API design, data model changes, layer boundaries, and system decomposition.

## When Jeffrey Evaluates Architecture

Before approving architectural work, ask:

1. **What does this prove?** — Architecture must justify its existence
2. **Is this necessary?** — Can existing infrastructure handle it?
3. **Who calls this?** — Every component needs a caller, even infrastructure
4. **Minimal?** — Surgical over comprehensive; existing files before new ones

## Architecture Decision Table

| Situation | Jeffrey's Response |
|-----------|-------------------|
| New service proposed | "is this necessary?", existing file can handle it? |
| New file in infrastructure | Last resort after: existing file > utility > `__init__.py` > test file |
| Layer boundary change | Field format consistency? Intentional translation? |
| API design change | Who calls this? Body-diff verify first |
| Data model change | Migration safe? Concurrent writes handled? |
| New factory/selection pattern | Verify all branches covered, default/fallback tested |
| Wrapper/abstraction layer | Does it add indirection without justification? |
| Refactor that changes API surface | Tests must cover all callers first |
| Clean architecture refactor | Justify separation — "clean" is not proof |
| Monolith splitting | Cost of distribution justified? Can they call each other? |

## Architecture Principles (from wiki)

- **Layer boundaries** — Field format must be consistent across boundaries (ArchitecturalBoundaries)
- **Clean separation** — Business logic independent of frameworks (CleanArchitecture)
- **Integration before creation** — Existing file > utility > `__init__.py` > test file > new file (JeffreyWorkingStyle)
- **Fail-closed** — Prefer fail-closed over best-effort
- **Minimal surface area** — New file creation is last resort

## Jeffrey's Architecture Red Flags

- New service with no callers
- Architecture diagram without implementation evidence
- Abstraction that adds indirection without reducing coupling
- "Clean" refactor with no test coverage
- Layer change that breaks field format consistency
- Data model change without migration strategy
- Factory pattern with untested fallback/default path

## Parent Oracle
[[jeffrey-oracle]] — the full decision framework
