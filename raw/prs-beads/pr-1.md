# PR #1: perf: optimize bd init performance by 36% (417ms → 268ms)

**Repo:** jleechanorg/beads
**Merged:** 2025-11-14
**Author:** jleechan2015
**Stats:** +299/-1 in 3 files

## Summary
Optimizes bd init performance by 36% (417ms → 268ms) via git operation optimization.

## Raw Body
## Summary

Optimizes bd init performance by 36% (417ms → 268ms) via git operation optimization.

## Performance Impact

**Benchmark Results** (5 iterations, M2 Mac):
- **Before**: 417ms average
- **After**: 268ms average  
- **Improvement**: 149ms faster (35.7% reduction)

## Optimization: Skip Git Checks on Fresh Repositories

**Problem**: bd init always ran expensive `git show HEAD:.beads/` operations even on fresh repos without any issues.

**Solution**: Added `gitHasBeadsDir()` helper that uses fast `git ls-tree -d HEAD .beads` check before running expensive operations.

**Impact**: Eliminates 1-2 git commands on fresh repositories.

## Critical Bug Fix (Copilot Review)

**Issue**: Initial PR included migration optimization that queried wrong table (`config.schema_version` instead of `metadata.bd_version`)

**Resolution**: Removed optimization entirely (commit fa0357d) because:
1. Schema version not reliably tracked in single location
2. Each migration has own existence checks (idempotent design)  
3. Cost of checking preconditions > cost of running idempotent migrations

## Documentation Fixes (Copilot Review)

Fixed 3 inaccuracies in CLAUDE.md:
- Schema version location (metadata table, not config)
- Migration file location (internal/storage/sqlite/migrations/)
- Table name (dependencies, not issue_dependencies)

## Testing

✅ Red-Green tested with timing measurements
✅ All Copilot feedback addressed

## Files Changed

- `cmd/bd/init.go` - Added gitHasBeadsDir() optimization
- `internal/storage/sqlite/migrations.go` - Removed broken optimization
- `CLAUDE.md` - Fixed documentation inaccuracies

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
