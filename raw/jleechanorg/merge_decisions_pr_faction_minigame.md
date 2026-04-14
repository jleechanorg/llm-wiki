# Merge Decisions: Faction Minigame Branch

**Branch:** `claude/add-force-creation-system-Mxqh0`
**Merged From:** `origin/main`
**Date:** 2025-12-30

## Conflict Resolution

### File: `.claude/commands/generatetest.md`

**Conflict Location:** Evidence Standards Checklist (lines 277-290)

**HEAD (this branch) added:**
```markdown
- [ ] Checksums: SHA256 for all evidence files (via `write_with_checksum()`)
- [ ] Test execution evidence: command + stdout/stderr + exit code saved to `artifacts/`
- [ ] Full git provenance output saved as `git_provenance_full.txt` with checksum
```

**origin/main added:**
```markdown
- [ ] Checksums: SHA256 for ALL evidence files including JSONL and server logs
```

**Resolution:** Combined both additions into a unified checklist item:
```markdown
- [ ] Checksums: SHA256 for ALL evidence files including JSONL and server logs (via `write_with_checksum()`)
- [ ] Test execution evidence: command + stdout/stderr + exit code saved to `artifacts/`
- [ ] Full git provenance output saved as `git_provenance_full.txt` with checksum
```

**Rationale:**
- Both branches extended the checklist with complementary requirements
- Main emphasized JSONL and server logs specificity
- This branch emphasized test execution artifacts and git provenance file
- Combined version maintains all requirements without duplication

## Changes in This Branch

### New Features
1. **Unit Test Evidence Standards** - Added to `evidence-standards.md`
   - Clarifies that unit tests (no server) still need proper evidence
   - Documents required vs optional fields for unit tests

2. **Test Execution Evidence** - New requirement
   - Command line used
   - Raw stdout/stderr captured
   - Exit code recorded

3. **Unit Test Support in /generatetest**
   - Added keyword detection for unit tests
   - Added template for unit test generation

### Refactoring
- `testing_mcp/faction/test_unit.py` now uses centralized `lib/evidence_utils.py`
- Removed ~100 lines of duplicated evidence capture code

## Files Changed
- `.claude/skills/evidence-standards.md` - Added Unit Test Evidence section
- `.claude/commands/generatetest.md` - Added unit test support + merged checklist
- `testing_mcp/faction/test_unit.py` - Refactored to use lib utilities
- `.claude/commands/savetmp.py` - Enhanced for test execution artifacts
