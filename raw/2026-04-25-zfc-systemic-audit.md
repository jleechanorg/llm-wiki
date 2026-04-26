# ZFC Leveling Initiative — Systemic Audit

**Date**: 2026-04-25
**Method**: PR metrics, commit analysis, skill landscape audit, postmortem review, conversation history

---

## The Numbers Tell The Story

### PR Sprawl (Apr 22–25, 4 days)

| PR | State | Commits | Created | Title |
|----|-------|---------|---------|-------|
| [#6557](https://github.com/jleechanorg/worldarchitect.ai/pull/6557) | closed | ? | Apr 22 | test: salvage narrow item-1 ZFC enforcement gate |
| [#6558](https://github.com/jleechanorg/worldarchitect.ai/pull/6558) | closed | ? | Apr 22 | ZFC Level Up: bypass rewards_engine resolver |
| [#6559](https://github.com/jleechanorg/worldarchitect.ai/pull/6559) | closed | **30** | Apr 22 | ZFC Level-Up: remove world_logic resolver path |
| [#6561](https://github.com/jleechanorg/worldarchitect.ai/pull/6561) | closed | ? | Apr 22 | ZFC M2: delete project_level_up_ui wrapper |
| [#6563](https://github.com/jleechanorg/worldarchitect.ai/pull/6563) | closed | **30** | Apr 22 | ZFC M1: compliance evidence harness |
| [#6564](https://github.com/jleechanorg/worldarchitect.ai/pull/6564) | closed | ? | Apr 22 | prompts(zfc): tighten canonical prompts |
| [#6565](https://github.com/jleechanorg/worldarchitect.ai/pull/6565) | closed | **25** | Apr 22 | fix(level-up): M0 stabilization bridge |
| [#6566](https://github.com/jleechanorg/worldarchitect.ai/pull/6566) | closed | ? | Apr 22 | ZFC: remove game_state resolver duplicate |
| [#6567](https://github.com/jleechanorg/worldarchitect.ai/pull/6567) | closed | ? | Apr 22 | ZFC Level-Up: remove world_logic resolver path |
| [#6568](https://github.com/jleechanorg/worldarchitect.ai/pull/6568) | closed | ? | Apr 22 | docs(zfc): tighten canonical prompt docs |
| [#6570](https://github.com/jleechanorg/worldarchitect.ai/pull/6570) | closed | ? | Apr 22 | fix(rewards_engine): reject float values |
| [#6577](https://github.com/jleechanorg/worldarchitect.ai/pull/6577) | closed | ? | Apr 22 | Docs: split ZFC proof-order notes |
| [#6578](https://github.com/jleechanorg/worldarchitect.ai/pull/6578) | closed | ? | Apr 22 | tests: prove formatter survivability alias |
| [#6580](https://github.com/jleechanorg/worldarchitect.ai/pull/6580) | closed | **30** | Apr 22 | Verify ZFC Architecture (Evidence Bundle) |
| [#6585](https://github.com/jleechanorg/worldarchitect.ai/pull/6585) | closed | ? | Apr 22 | chore: remove redundant rewards wiring imports |
| [#6587](https://github.com/jleechanorg/worldarchitect.ai/pull/6587) | closed | ? | Apr 23 | clarify level_up_signal prompt semantics |
| [#6591](https://github.com/jleechanorg/worldarchitect.ai/pull/6591) | closed | ? | Apr 23 | Clarify level-up mismatch warning contract |
| [#6595](https://github.com/jleechanorg/worldarchitect.ai/pull/6595) | closed | ? | Apr 24 | remove level_up_signal schema field |
| [#6600](https://github.com/jleechanorg/worldarchitect.ai/pull/6600) | closed | ? | Apr 24 | recognize canonical prompt field names |
| [#6618](https://github.com/jleechanorg/worldarchitect.ai/pull/6618) | **open** | **21** | Apr 25 | ZFC M3: Final Enforcement Gates |
| [#6622](https://github.com/jleechanorg/worldarchitect.ai/pull/6622) | **open** | **26** | Apr 25 | fix(level-up): propagate signal |
| [#6625](https://github.com/jleechanorg/worldarchitect.ai/pull/6625) | merged ✅ | 9 | Apr 25 | contradiction guard for level_up_signal |
| [#6630](https://github.com/jleechanorg/worldarchitect.ai/pull/6630) | open | 1 | Apr 25 | "Stop reopening it if you see this LLM" |
| [#6632](https://github.com/jleechanorg/worldarchitect.ai/pull/6632) | merged ✅ | 2 | Apr 25 | M1b: compliance rate harness |
| [#6633](https://github.com/jleechanorg/worldarchitect.ai/pull/6633) | merged ✅ | 2 | Apr 25 | docs: sync ZFC model doc |
| [#6635](https://github.com/jleechanorg/worldarchitect.ai/pull/6635) | **open** | **30** | Apr 25 | false positive heuristic contradiction guard |
| [#6638](https://github.com/jleechanorg/worldarchitect.ai/pull/6638) | **open** | **23** | Apr 25 | M3 final enforcement |
| [#6640](https://github.com/jleechanorg/worldarchitect.ai/pull/6640) | closed | **30** | Apr 25 | Consolidate M2 (rev-yxcnw) |
| [#6641](https://github.com/jleechanorg/worldarchitect.ai/pull/6641) | open | 7 | Apr 25 | Consolidated M2 Completion (rev-yxcnw) |
| [#6643](https://github.com/jleechanorg/worldarchitect.ai/pull/6643) | **open** | **16** | Apr 25 | fix-tests / prompts: ZFC |
| [#6645](https://github.com/jleechanorg/worldarchitect.ai/pull/6645) | **open** | **30** | Apr 25 | zfc item5: llm_parser projected rewards |
| [#6647](https://github.com/jleechanorg/worldarchitect.ai/pull/6647) | **open** | **13** | Apr 25 | Level-Up: Fix Time Freeze |

### Summary Metrics

| Metric | Value |
|--------|-------|
| Total ZFC PRs (Apr 22–25) | **~30** |
| Actually merged | **3** (10%) |
| Still open | **11** |
| Closed without merge | **~16** |
| Average commits per open PR | **22** |
| PRs hitting GitHub's 30-commit cap | **6** |
| PRs with "Stop reopening" in title | **1** (human frustration signal) |

> [!CAUTION]
> **3 merged out of ~30 PRs is a 10% success rate.** The average open PR has 22 commits — each commit is a "fix the fix" cycle. This is not efficient progress; it's agents spinning.

---

## Pattern Analysis: Why Agents Spin

### Pattern 1: "Fix Where You See It" Prior

The dominant failure mode across #6622, #6640, #6645:

1. Agent sees bug: "level_up_signal not in unified_response"
2. Agent traces data flow to `world_logic.py` (where `unified_response` is built)
3. Agent adds canonicalization logic to `world_logic.py`
4. **Violation**: `world_logic.py` MUST NOT own canonicalization — `rewards_engine.py` does
5. Reviewer catches it → agent adds another commit to "fix" → 30 commits later, still wrong

**Root cause**: LLM training data says "fix where the bug manifests." The ZFC architecture requires indirection (fix upstream, pass through). This indirection is a *minority pattern* in training data.

### Pattern 2: API Contract Ignorance

The `canonicalize_rewards()` 3-tuple saga across #6622:

1. Agent needs to return `canonical_signal` alongside `rewards_box` and `planning_block`
2. Agent adds a 3rd element to the return tuple
3. **Violation**: API contract freeze says 2-tuple only; use `out_meta` dict
4. This breaks 20+ call sites → 10+ commits just fixing test unpacking
5. Eventually reverted to 2-tuple + `out_meta` (the right answer from day 1)

**Root cause**: The contract freeze didn't exist in any agent-readable location until this session created `zfc-boundaries.md`. There was nowhere for the agent to learn "don't change the return type."

### Pattern 3: Scope Creep Via "While I'm Here"

#6622 grew from "propagate signal" to also include:
- `include_raw_llm_payloads` observability feature (decommissioned later)
- Evidence synthesis harness changes (`base_test.py` +115 lines)
- `http_client.py` changes + test file
- `GEMINI.md` config changes

Each addition felt justified in isolation. Together they turned a 5-file PR into a 27-file PR that couldn't pass CI because the test surface was too broad.

### Pattern 4: Supersede Without Close

Multiple PRs do overlapping work:
- #6559, #6566, #6567 all "remove world_logic resolver path"
- #6640 and #6641 are both "Consolidated M2 Completion"
- #6618 and #6638 are both "M3 final enforcement"

Agents create new PRs rather than fixing existing ones, but don't close the old ones. This creates a branching tree of competing work where none reaches completion.

### Pattern 5: Evidence Theater

From the postmortem: agents "post truthful PR comments" and "build audit notes" as progress substitutes. Real progress = merged code. Classification, notes, and review comments are *not* progress toward merge.

---

## Skill Fragmentation Problem

| Skill | Lines | Where | Overlap |
|-------|-------|-------|---------|
| `zfc-boundaries.md` | 53 | `~/.claude/skills/` | Core table + contract — **the useful 20%** |
| `zfc-preflight.md` | 50 | `~/.claude/skills/` | ~80% duplicates boundaries |
| `level-up-zfc/SKILL.md` | 140 | `.claude/skills/` (project) | M0-M3 checklists — partially stale |
| `loop-level-zfc/SKILL.md` | 525 | `.claude/skills/` (project) | AO orchestration — **entirely stale** (references #6420, #6404, #6418) |
| `field-ownership-contracts.md` | 92 | `.claude/skills/` (project) | Field writer/reader contracts — complementary |

**Total ZFC skill lines: 860** across 5 files, plus a **100KB roadmap doc** and a **28KB task spec**.

Agents are told "read the roadmap" (1,725 lines) + "check 5 skills" (860 lines) = **2,585 lines of context** before writing code. In practice, they skip all of it because the signal-to-noise ratio is terrible.

**The actually useful enforcement content fits in ~80 lines**:
1. The 6-row file-responsibility table (15 lines)
2. The API contract freeze (5 lines)
3. The common violations table (10 lines)
4. The pre-flight checklist (20 lines)
5. The design principle (2 lines)
6. The milestone status (10 lines)
7. The decision flowchart (8 lines)

---

## Root Cause Hierarchy

```
1. NO MACHINE ENFORCEMENT (biggest factor)
   → File-responsibility boundaries exist only as prose
   → No CI gate rejects boundary violations
   → Agents get zero automated feedback

2. TOO MUCH CONTEXT, NOT ENOUGH SIGNAL (second factor)  
   → 2,585 lines across 5 skills + 2 docs
   → Agents read selectively and miss the constraints
   → The "Owns / Must Not Do" table drowns in detail

3. LLM TRAINING DATA PRIORS (contributing factor)
   → "Fix where the bug manifests" is the dominant pattern
   → Architectural indirection is rare in training data
   → Without explicit override instructions, agents default to priors

4. PR PROLIFERATION WITHOUT CLOSURE (amplifying factor)
   → Agents open new PRs instead of fixing existing ones
   → ~16 closed-without-merge PRs = wasted compute
   → Competing branches create merge conflicts that generate more commits
```

---

## Recommendations

### Immediate (this session)

1. **Consolidate 5 skills → 1**: Single `.claude/skills/zfc-leveling-roadmap/SKILL.md` (~120 lines). Delete the rest.
2. **Update AGENTS.md + CLAUDE.md**: Point to the single consolidated skill, not `~/.claude/skills/zfc-boundaries.md`.
3. **Delete `loop-level-zfc/SKILL.md`**: 525 lines of entirely stale AO orchestration with dead PR references.

### This week

4. **Ship lightweight CI grep gate**: Check for `canonicalize_level_up_signal` called outside `rewards_engine.py`. This is the most common violation and can be caught with a simple `grep`.
5. **PR hygiene rule**: Add to AGENTS.md: "Before opening a new ZFC PR, check if an open PR already covers this scope. Fix the existing PR instead of creating a new one."

### Longer term

6. **PR commit budget**: Consider adding a soft guideline: "If a PR exceeds 15 commits without approaching merge, STOP and split it."
7. **Scope-lock enforcement**: Task specs should be machine-readable, not just prose.
