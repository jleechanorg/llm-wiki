---
description: Org runner audit skill — use org-level GH API, not repo-level
tags: [github, runners, skills, infrastructure]
---

# org-runner-audit skill

**Source**: `.claude/skills/org-runner-audit.md`

## Purpose

Query and audit all org-level self-hosted runners for `jleechanorg`.

## Key Rule

**Always use org-level API, not repo-level:**

```bash
# CORRECT — org-level, shows all 8 runners
gh api orgs/jleechanorg/actions/runners

# WRONG — repo-level, shows only 2 runners
gh api repos/jleechanorg/worldarchitect.ai/actions/runners
```

## Runner Inventory (2026-05-01)

| Runner | Arch | Status |
|--------|------|--------|
| org-runner-2SXGKNOwR7Qzd | ARM64 | online |
| org-runner-bgswU1chN3k3D | ARM64 | online |
| org-runner-CmpGyqdqekKaF | ARM64 | online |
| org-runner-fLVP8DKZmyH5v | ARM64 | online |
| org-runner-lktqrKP9ik2l7 | ARM64 | online |
| org-runner-m5oBAqJ57GgCX | ARM64 | online |
| org-runner-O5pboDO9PzDia | ARM64 | online |
| org-runner-Rb1ZbGyViUPJY | ARM64 | online |
| org-runner-3 | X64 | offline |
| org-runner-4 | X64 | offline |

## Memory History

- Memory incident 0.73: org-runner confusion first noted
- Memory incident 0.77: org-runner confusion re-occurred
- Memory incident 0.78: org-runner confusion re-occurred
- 2026-05-01: `org-runner-audit.md` skill created to prevent recurrence