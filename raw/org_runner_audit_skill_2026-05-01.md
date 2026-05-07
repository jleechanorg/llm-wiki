---
name: org-runner-audit-skill-created
description: Added org-runner-audit skill to prevent repo-vs-org runner query mistakes
type: feedback
bead: none
---

## Learning: org-runner-audit skill created

**Type**: feedback | **Classification**: Best Practice | **Bead**: none

**Summary**: When checking self-hosted runner status, ALWAYS use `gh api orgs/jleechanorg/actions/runners` (org-level), NOT `gh api repos/jleechanorg/worldarchitect.ai/actions/runners` (repo-level). Repo-level only shows 2 runners; org-level shows all 8.

**Context**:
- User ran `/integrate` and then asked to check runner status
- `gh api repos/.../actions/runners` returned only 2 runners (offline X64)
- User showed GitHub UI which had 8 org-level runners (6 online ARM64, 2 offline X64)
- This was the 4th time this confusion occurred (memory IDs 0.73, 0.77, 0.78)

**Technical Detail**:
- `gh api repos/.../actions/runners` → repo-registered runners only (2 total: org-runner-3, org-runner-4 both offline)
- `gh api orgs/jleechanorg/actions/runners` → all org-registered runners (8 total: 6 ARM64 online, 2 X64 offline)
- The skill `.claude/skills/org-runner-audit.md` now captures this distinction with trigger patterns

**Solution**:
- Created `.claude/skills/org-runner-audit.md` skill with triggers: runner, self-hosted, list runners, check runners, audit runners
- Skill contains the correct org-level query command and explains the repo-vs-org distinction

**Verification**:
- Org runner query confirmed 6 online ARM64 runners + 2 offline X64 runners
- PR #6770 created with the skill file

**Files**:
- `.claude/skills/org-runner-audit.md` (new skill)

**References**:
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6770
- Memory incidents: 0.73, 0.77, 0.78 (prior org-runner visibility failures)