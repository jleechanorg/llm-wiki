---
name: blind-rename-pitfalls-openclaw-to-hermes
description: Mechanical find-replace renames produce 5 classes of breakage; each needs targeted remediation
metadata: 
  node_type: memory
  type: project
  originSessionId: 5e846711-556f-4eab-85b3-0883dbc44f75
---

The openclaw→hermes migration rename (PR #568, 69+ CodeRabbit findings) produced 5 classes of breakage:

1. **Self-referential rename** — "Hermes replaced Hermes" in docs where both old and new name appeared
2. **Config filename format changes** — `.py` configs renamed to `.yaml` or vice versa, changing file format
3. **Historical name inversion** — "formerly OpenClaw" → "formerly Hermes" (reversed migration direction)
4. **Repository references to non-existent repos** — AO config pointed at `hermes-agent` repo that doesn't exist in the org
5. **Hardcoded paths and binary names** — `/Users/jleechan` paths in plists, `openclaw` binary references in scripts

**Why:** A mechanical `s/openclaw/hermes/g` across all files cannot distinguish between: (a) current identity, (b) historical references that should preserve the old name, (c) file format identifiers, (d) paths to actual binaries/directories that need separate migration.

**How to apply:** For any project rename: (1) never use blind find-replace — review each match category, (2) preserve "formerly <old-name>" historical references, (3) verify binary/path references point to real targets after rename, (4) check that config file extensions weren't changed, (5) verify repository references in CI/deploy configs exist. Test by grepping for the old name post-rename — any remaining hits should be intentional (historical, upstream, or third-party).
