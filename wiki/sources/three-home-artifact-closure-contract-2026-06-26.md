---
type: source
title: Three-Home Artifact Closure Contract
slug: three-home-artifact-closure-contract
date: 2026-06-26
classification: best-practice
tags: [harness, deploy-pipeline, skillify, closure-summary, jleechanclaw]
---

# Three-Home Artifact Closure Contract

## Source

- Slack thread: `C09GRLXF9GR / 1782517257.897709` — `/roadmap` skillify, 2026-06-26
- Memory file: `~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-26_three-home-artifact-closure-contract.md`
- Roadmap entry: `~/roadmap/learnings-2026-06.md` § 2026-06-26
- Bead: `jleechan-hzs8` (P4, OPEN)
- Fix commit: `df209445c0` on `jleechanorg/jleechanclaw` — `feat(roadmap): sync skill + thin-pointer slash command + RESOLVER entry to origin/main`

## The rule

For any artifact that lives outside `deploy.sh` `POLICY_FILES=(CLAUDE.md SOUL.md TOOLS.md HEARTBEAT.md)` — `skills/`, `scripts/`, `launchd/`, `.claude/commands/`, `cron/jobs.json` — the closure summary MUST verify THREE homes, not two:

1. **Staging tree** (`~/.hermes/<path>`) — git-tracked source of truth
2. **Prod tree** (`~/.hermes_prod/<path>`) — runtime mirror, what the live gateway serves
3. **origin/main** on `jleechanorg/jleechanclaw` — what a fresh `git clone` would see

The trap is treating `diff -q staging ↔ prod` (byte-equality) as the deployment contract. The actual contract is: `origin/main` is canonical + `deploy.sh` Stage 4.5/4.6 + manual `cp` (for non-POLICY_FILES).

## The recipe (30-second diagnostic)

```bash
ARTIFACT="skills/roadmap/SKILL.md"

echo "1. staging: $(test -f ~/.hermes/$ARTIFACT && echo PRESENT || echo MISSING)"
echo "2. prod:    $(test -f ~/.hermes_prod/$ARTIFACT && echo PRESENT || echo MISSING)"
echo "3. tracked: $(cd ~/.hermes && git ls-files $ARTIFACT)"
echo "4. on main: $(cd ~/.hermes && git show origin/main:$ARTIFACT 2>/dev/null | wc -l)"
echo "5. last commit: $(cd ~/.hermes && git log --oneline -1 -- $ARTIFACT)"
```

| Item 1-2 | Item 3-5 | State | Fix |
|----------|----------|-------|-----|
| both PRESENT | both PRESENT | durably landed | none |
| staging PRESENT, prod PRESENT | missing | prod-only orphan (THIS BUG) | worktree + cp + commit + push |
| both PRESENT | both PRESENT but stale | drift | re-sync |

## The failure class

- Skill works in prod but `git clone` of jleechanclaw has no skill
- Slash command `/foo` works in current session but 404s for anyone who clones fresh
- `/roadmap` returns "skill not found" despite the skill being "delivered"

Same shape as `skillify` → "Anti-Pattern: Skill Evolution Lives in Prod, Not in Git-Origin" (the prod-vs-origin drift class) and `hermes-deploy-pipeline` → "Known Issue: `.claude/commands/` is also NOT in `POLICY_FILES`". The three documents together cover:
- **prod-vs-origin drift** (skillify): how the gap appears
- **deploy-pipeline gap** (POLICY_FILES): why the deploy script doesn't close the gap automatically
- **three-home contract** (this): the explicit closure-summary requirement that catches the gap at the natural point of failure

## See also

- Concept page: `concepts/ThreeHomeArtifactContract.md`
- Companion: `skillify/SKILL.md` → "Anti-Pattern: Skill Evolution Lives in Prod, Not in Git-Origin"
- Companion: `hermes-deploy-pipeline/SKILL.md` → "Known Issue: `.claude/commands/` is also NOT in `POLICY_FILES`"