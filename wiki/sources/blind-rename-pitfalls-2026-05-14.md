# Blind Rename Pitfalls (openclaw→hermes)

**Date**: 2026-05-14
**Source**: PR #568 (jleechanorg/jleechanclaw)
**Bead**: orch-8zvm

## Summary

Mechanical find-replace renames produce 5 classes of breakage:

1. **Self-referential rename** — "Hermes replaced Hermes" in docs where both old and new name appeared
2. **Config filename format changes** — `.py` configs renamed to `.yaml` or vice versa, changing file format
3. **Historical name inversion** — "formerly OpenClaw" → "formerly Hermes" (reversed migration direction)
4. **Repository references to non-existent repos** — AO config pointed at `hermes-agent` repo that doesn't exist in the org
5. **Hardcoded paths and binary names** — `/Users/jleechan` paths in plists, `openclaw` binary references in scripts

## Rule

For any project rename: (1) never use blind find-replace — review each match category, (2) preserve "formerly <old-name>" historical references, (3) verify binary/path references point to real targets after rename, (4) check that config file extensions weren't changed, (5) verify repository references in CI/deploy configs exist.

## Related

- [[ProjectRename]]
- [[DockerVolumeMigration]]
- [[GreenGateCI]]
