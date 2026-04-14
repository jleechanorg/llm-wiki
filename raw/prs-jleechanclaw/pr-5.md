# PR #5: chore: Scaffold development scripts and enhance AGENTS.md

**Repo:** jleechanorg/jleechanclaw
**Merged:** 2026-02-14
**Author:** jleechan2015
**Stats:** +5046/-0 in 19 files

## Summary
Scaffolds essential development scripts and tools from [jleechanorg/claude-commands](https://github.com/jleechanorg/claude-commands), intelligently adapted for OpenClaw's TypeScript/Node.js environment.

## Raw Body
## Summary

Scaffolds essential development scripts and tools from [jleechanorg/claude-commands](https://github.com/jleechanorg/claude-commands), intelligently adapted for OpenClaw's TypeScript/Node.js environment.

## 📦 What's Included

### Root-Level Scripts
- ✅ **create_worktree.sh** - Git worktree management for parallel development
- ✅ **integrate.sh** - Intelligent branch integration with conflict resolution
- ✅ **schedule_branch_work.sh** - Branch work scheduling and management

### Scripts Directory (scripts/)

#### Linting & Quality (⭐ Adapted)
- ✅ **run_lint.sh** - Comprehensive linting adapted for OpenClaw stack
  - oxlint (type-aware TypeScript)
  - oxfmt (formatting)
  - TypeScript compilation check
  - SwiftLint (iOS/macOS)
  - markdownlint (documentation)

#### Testing & Coverage (⭐ Adapted)
- ✅ **run_tests_with_coverage.sh** - Test runner adapted for vitest
  - Multiple modes: unit, e2e, fast, coverage, docker
  - Coverage reporting with vitest
  - Integration with existing test infrastructure

#### Code Metrics
- ✅ **loc.sh**, **loc_simple.sh**, **codebase_loc.sh** - Code analysis
- ✅ **coverage.sh** - Coverage report generation

#### Development Utilities
- ✅ **push.sh** - Smart git push with validation
- ✅ **resolve_conflicts.sh** - Automated conflict resolution
- ✅ **create_snapshot.sh** - Project snapshot creation
- ✅ **setup_email.sh**, **sync_branch.sh** - Git utilities
- ✅ **setup-github-runner.sh** - CI/CD setup
- ✅ **claude_start.sh** - Claude CLI startup script

## 🎯 Technology Stack Adaptations

The scripts have been intelligently adapted for OpenClaw's environment:

**Detected Stack:**
- Runtime: Node.js ≥22
- Language: TypeScript
- Package Manager: pnpm
- Test Framework: vitest
- Linting: oxlint (type-aware), SwiftLint, markdownlint

**Key Changes:**
- Replaced Python tooling (ruff, pytest) with TypeScript equivalents (oxlint, vitest)
- Added SwiftLint support for iOS/macOS code
- Integrated with existing pnpm scripts
- Added comprehens
