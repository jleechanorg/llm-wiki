# Real-Time Governance Layer Design

## Status

- **Type**: Feature design
- **Author**: Hermes Agent
- **Created**: 2026-04-15

## Context

The AO evolve loop (orchestrator-prompt.ts) is an 8-phase autonomous loop that already reads GOVERNANCE.md and SCOPE.md at startup. These are currently hardcoded in the prompt. This design proposes making governance files filesystem-based and runtime-readable.

## What Exists vs What's Proposed

| Layer | Existing | Proposed |
|-------|----------|----------|
| Constitution file | IMPLICIT_DENY_LIST hardcoded | GOVERNANCE.md filesystem-based |
| Scope definition | agent-orchestrator.yaml | SCOPE.md per-project |
| Evidence artifacts | Skeptic verdict stored in JSON | skeptic-verdict.md markdown |
| Evidence artifacts | Evidence bundle in JSON store | evidence-bundle.md markdown |

## Proposed File Structure

```
~/.ao-evolve-knowledge/<projectId>/
├── GOVERNANCE.md      # Hard constraints loaded every OBSERVE cycle
├── SCOPE.md           # In/out of bounds for issues
└── prs/
    └── <prNumber>/
        ├── skeptic-verdict.md   # Skeptic output, optional read
        └── evidence-bundle.md   # Evidence bundle, optional read

~/.ao-evolve-knowledge/global/
├── GOVERNANCE.md      # Global hard constraints
└── SCOPE.md           # Global scope
```

## GOVERNANCE.md Format

```markdown
# Hard Constraints (enforced, no override)
- Never: gh pr merge, gh pr close, git reset --hard, git clean -fd
- Never: git worktree remove, rm -rf
- Never: modify GOVERNANCE.md itself

# Soft Constraints (warned, can proceed)
- PR max 600 lines
- Always run tests before merge
- Skeptic must PASS (not SKIPPED)

# Escalation Paths (optional human review)
- /escalate — request human review
- Auto-escalate after 3 consecutive failures
```

## SCOPE.md Format

```markdown
# In Scope
- Bug fixes tagged "good-first-issue"
- Documentation updates
- Test additions
- Refactoring within existing modules

# Out of Scope
- Security changes without explicit approval
- Database migrations
- Breaking API changes
- Changes to CI/CD infrastructure
```

## Key Design Properties

1. **No mandatory human review** — artifacts are byproducts, not gates
2. **No blocking gates** — system never waits for human input
3. **No required files** — system proceeds without them
4. **Edit without PR** — write directly to `~/.ao-evolve-knowledge/`
5. **Backwards compatible** — existing behavior unchanged when files absent

## Injection Point

Phase 0: GOVERNANCE_LOAD
- Reads GOVERNANCE.md + SCOPE.md from filesystem
- Injects constraints into Phase 1 OBSERVE prompt
- Falls back to IMPLICIT_DENY_LIST when files absent

## Relationship to PR #453

PR #453 (gate-governance plugin) implements the hard merge gate enforcement.
This design (#452) provides the runtime governance layer that feeds into it.
They are complementary: #452 is the constitution, #453 is the enforcement.

## Open Questions

1. Sync governance files to git? (risk: drift between machines)
2. Version governance history? (git vs filesystem)
3. Global vs per-project precedence?
4. Who can edit GOVERNANCE.md? (ACL? just the operator?)
