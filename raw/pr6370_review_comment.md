## Review Comment — Behavioral Changes Beyond Stale-Flag Scope

Two changes in `rewards_engine.py` go beyond the PR's stated goal of "fixing stale level-up state flags" and should either be split into separate PRs or explicitly acknowledged.

### 1. ASI Choices Now Apply to Single-Class Characters (Not Just Multiclass)

**Before:**
```python
# Multiclass ASI check — use total character level for ASI decision
if len(class_levels) > 1:
    total_level = sum(class_levels.values())
    ...
```

**After:**
```python
# ASI check — use target_level for ASI decision
asi_list: list[dict[str, Any]] = []
seen_asi_levels: set[int] = set()
for class_type, class_level in class_levels.items():
    if _is_asi_level(target_level, class_type) and target_level not in seen_asi_levels:
```

Single-class characters now receive ASI choices at levels 4, 8, 12, 14, 16, 19 — behavior that previously only fired for multiclass characters. This is a meaningful behavior change, not a bug fix.

### 2. XP Display: `rewards_pending.xp_gained` Now Overrides Computed Progress

**Before:** `xp_gained` = XP above level floor (e.g., 0 for a fresh level-1 character who earns 300 XP).

**After:** `xp_gained` = `rewards_pending.xp_gained` or `rewards_pending.xp` when present — so the same character now sees `xp_gained=300` instead of `xp_gained=0`.

The PR body states "UI evidence is N/A - no UI changes." The XP display change is UI-visible.

### Recommendation

Either (a) split these into their own PRs with dedicated evidence, or (b) update the PR body to explicitly scope these as intentional behavior changes alongside the stale-flag fix.