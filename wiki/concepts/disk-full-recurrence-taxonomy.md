---
title: DiskFullRecurrenceTaxonomy
type: concept
tags: [disk_magician, taxonomy, disk-full, structural-producers, retention-policy]
sources: [sources/feedback-2026-07-29-root-cause-disk-full.md]
last_updated: 2026-07-29
---

The 5 producer classes that cause disk-full recurrence on this machine, ranked by
reclaimable size at the 2026-07-29 snapshot. This is the operative taxonomy — when free
disk drops below ~30 GiB again, walk this list and pick the cheapest fix first.

| # | Producer | Class | Typical size | Cheap-fix shape |
| --- | --- | --- | --- | --- |
| 1 | agent-venv bloat in `<repo>/.claude/worktrees/*/venv` and `venv.bak.<ts>` | scope gap (cleanup_worktree_venvs misses `.claude/worktrees`) | ~25 GiB | Extend `cleanup_worktree_venvs.sh` find walk + add `.bak.<ts>` older-than-30d prune |
| 2 | abandoned AO+Claude siblings under `~/.worktrees/*` | scope gap (cleanup_worktrees misses standalone siblings) | ~30 GiB | Depth-1 enumerate `~/.worktrees`, apply SAFE/NEEDS-REVIEW triage |
| 3 | `/private/tmp/{ambientfix*,crashfix,ios-app-prev}` unowned cruft | coverage gap (allowlists exclude these prefixes) | ~8.4 GiB | Add a separate launchd sweep over `/private/tmp/<non-listed>` with WORKTREE_APPROVED |
| 4 | `~/.gemini/antigravity-cli/{brain,conversations}` | out of scope (agent-cli owned) | ~12.7 GiB | Out-of-band; needs Antigravity config change. Bead `disk_magician-1f9` covers related territory. |
| 5 | `.git` history (worktree dirs + `~/.hermes/.git`) | cosmetic | ~6 GiB | Schedule `set_gc_worktree_prune.sh` weekly |

**Reclaimable headroom if #1+#2+#3+#5 are addressed:** ~69 GiB without touching cache or
`~/.gemini`. Pressure_sweep is **not** in this list — that's a release valve, not a producer.

## When emergency pressure hits and disk crosses 30 GiB free

The fastest path is **manual** pressure_sweep (recovers 60 GiB in < 6 min, observed on
2026-07-26 16:49-17:36). The structural fixes above are what keeps pressure_sweep's
emergency invocation from becoming a daily ritual. They are *cheap maintenance* vs the
emergency *pressure release*.

## Diagnosis recipe (30 seconds)

```bash
df -h ~ | tail -1
python3 - <<'PY'
import subprocess
for p in ['/Users/jleechan/projects', '/Users/jleechan/.worktrees',
         '/private/tmp', '/Users/jleechan/.hermes', '/Users/jleechan/.gemini',
         '/Users/jleechan/Library/Caches']:
    r = subprocess.run(['du','-k','-d','2',p], capture_output=True, text=True, timeout=180)
    rows = []
    for l in r.stdout.splitlines():
        try: s,pp=l.split('\t',1); rows.append((int(s)//1024//1024,pp))
        except: pass
    rows.sort(reverse=True)
    print(p); [print(f'  {g:5d} GiB  {p2}') for g,p2 in rows[:5]]
PY
```

Match the output against the taxonomy table. Don't re-derive.

## Why this taxonomy exists

Each entry fixes a specific gap identified on a specific date. The taxonomy has been
measured twice and updated once (2026-05-29 prior, 2026-07-29 current). New producer
classes get added when they appear in diagnosis, not when someone has the bandwidth.

## See also

- [[DiskMagician]] — tooling
- [[DiskCleanupCoverage]] — high-level coverage map
- [[HostDiskGuardianScript]] — sister script for what pressure_sweep doesn't sweep
- Pressure_sweep invocation recipe in `feedback_2026-07-29_root_cause_disk_full.md`
