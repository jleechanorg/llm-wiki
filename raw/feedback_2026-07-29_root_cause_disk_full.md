---
name: 2026-07-29-disk-full-five-root-causes-ranked
description: "50 hours after the 2026-07-26 emergency reclaim, free disk dropped ~30 GiB; the bead disk_magician-7v3 holds the du sheet — these 5 causes are not yet fixed because each is structural"
metadata: 
  node_type: memory
  type: feedback
  bead: disk_magician-7v3
  originSessionId: d1c16e37-c03b-4f8d-bf7d-57d09005a2a4
  modified: 2026-07-29T08:15:12.344Z
---

Context: on 2026-07-29 03:09 PDT free disk is 29 GiB (was 60 GiB during the 2026-07-26 16:49-17:36
emergency reclaim). The 529-path massive reclaim from 2026-07-26 only restored free space
*within that single window*; the underlying producers were not addressed. Top consumers
on this machine, measured with `du -k -d 2 <root>` (output saved at `/tmp/du_hot.txt`
and `/tmp/du_deep.txt` during the 2026-07-29 investigation):

| Path | GiB | Comment |
| --- | --- | --- |
| `~/projects` | 119.08 | dominated by `worldarchitect.ai/.claude` (42.6) |
| `~/.worktrees` | 34.87 | jleechanorg-fix 2.4 + wa-pr8536 1.7 + wa-claw 1.4 + agent-orchestrator 1.97 — abandoned siblings |
| `/private/tmp` | 36.70 | worldarchitect.ai/ 7.6 + ~8.4 from unowned ambientfix*/crashfix/ios-app-prev scratch |
| `~/.hermes` | 13.64 | sessions 4.89, logs 1.14, git 1.13 |
| `~/.gemini` | 12.69 | antigravity-cli/brain 10.25, conversations 2.16 |
| `~/Library/Caches` | 10.14 | pnpm dlx 2.28, ms-playwright 1.71, Chrome 1.56, swiftpm 1.03, Aside 0.75 |
| `~/projects/worldarchitect.ai/.git` | 5.94 | |
| `~/projects/user_scope/backup` | 5.35 | |
| `~/projects/user_scope/.worktrees` | 3.20 | |

## Five root causes (ranked by reclaim potential)

### 1. Agent venv bloat (~25 GiB reclaimable)
`worldarchitect.ai/.claude/worktrees/agent-*/venv` and `venv.bak.20260703-102724` dirs.
`cleanup_worktree_venvs.sh` renames to `.bak.<ts>` (correct safety net) but **nothing
purges `.bak` dirs that age > 30 days**. The disk_magician cleanup script's `find` walk
covers `~/projects/worktree_*` and `~/worktrees_*` but **not** `<repo>/.claude/worktrees`.
**Fix shape:** extend `cleanup_worktree_venvs.sh` to walk `.claude/worktrees/` and prune
`.bak.<ts>` older than 30 days. ~50 lines of shell.

### 2. Abandoned AO+Claude parents under `~/.worktrees` (~30 GiB)
jleechanorg-fix 2.4, wa-pr8536-finish 1.7, wa-claw 1.4, agent-orchestrator 1.97, agent-orchestrator-ts 2.15.
cleanup_worktrees.sh only handles `<repo>/.claude/worktrees` (i.e. nested), not the
**standalone `~/.worktrees/*` siblings**. **Fix shape:** enumerate `~/.worktrees/*` at
depth 1 in cleanup_worktrees.sh, apply SAFE/NEEDS-REVIEW triage. Many are safe-by-now
branches whose PRs already merged.

### 3. Unowned `/private/tmp` scratch (~8.4 GiB)
6 dirs at ~1.4 GiB each: `ambientfix`, `ambientfix-before`, `ambientfix-derived`,
`crashfix`, `ios-app-prev`. cleanup_tmp.sh's allowlist is `worldarchitect.ai`/`wa-missions`
only; hermes-mission-output-cleanup covers a different set. Neither matches these prefixes.
**Fix shape:** add a 48h-or-larger sweep over `/private/tmp/<non-listed>` with WORKTREE_APPROVED,
or accept the cruft and rotate it manually each quarter.

### 4. Antigravity `brain` + `conversations` (~12.7 GiB)
`~/.gemini/antigravity-cli/{brain,conversations}`. Owned by the Antigravity CLI. Not in scope
of disk_magician — bead `disk_magician-1f9` covers the whole-root .gemini symlink retirement
which is unrelated. Conservative: needs an out-of-band sweep (5+ GiB reclaimable).

### 5. `.git` history bloat (~6 GiB across the .worktrees dirs + ~/.hermes/.git)
Standard object-packing. `git gc --prune=now` on each is ~free; not scheduled anywhere.
`scripts/set_gc_worktree_prune.sh` exists and acts once per invocation (not periodic).

## Why not fixed in-place

The fix-on-discovery rule in `~/.claude/CLAUDE.md` says: user-config + <10 lines +
currently blocking → fix now. None of these 5 qualifies on all three. At 29 GiB free
(~3% of disk), there's no immediate pager — the next pressure_sweep window will handle
the next push. Any single fix is a multi-line change with policy surface (e.g. deciding
retention for `.bak` dirs and whether to extend scope to `.claude/worktrees/` needs user
review). Each should be a discrete PR with its own bead rather than a fast-fix.

## Operational pattern: when "disk full" lands again

Same root-cause taxonomy will recur, but the ordering will shift. Fast triage recipe:

1. **Quick state**: `df -h ~` and read free %. If > 10%, monitor; if < 10%, emergency.
2. **Quick cause attribution** (do NOT do a full `du` first):
   ```bash
   # 4.5 GiB minimum set — answers ~80% of "where did it go" within seconds
   python3 -c "
   import subprocess
   for p in ['/Users/jleechan/projects', '/Users/jleechan/.worktrees',
            '/private/tmp', '/Users/jleechan/.hermes', '/Users/jleechan/.gemini',
            '/Users/jleechan/Library/Caches', '/Users/jleechan/Downloads']:
       r = subprocess.run(['du','-k','-d','2',p], capture_output=True, text=True, timeout=120)
       print(p); [print('  ', l.split(chr(9))[0] // 1024 // 1024, 'GiB', l.split(chr(9),1)[1]) for l in sorted(r.stdout.splitlines(), reverse=True)[:5]]
   "
   ```
3. **Cross-reference with bead disk_magician-7v3** for the established taxonomy. Don't
   re-derive; the producers are slow-changing per quarter.
4. **If emergency (free < 20 GiB):** launch `disk_magician/scripts/pressure_sweep.sh`
   manually — it's `LARGE_TMP_APPROVED=1 TMP_WORKTREES_APPROVED=1 cleanup_tmp.sh --clean --large`.
   Per the read-state-check report on the 2026-07-26 session, that freed 60 GiB in ~6 min.
   This is the SLOW-but-CORRECT recovery; the taxonomy above is what to fix at the
   producer level.

## Why the previous /learn session didn't catch this earlier

The 2026-07-26 /learn closed with `disk_magician-y7t: IDENTIFIED a mass sweep (529 paths,
52 GiB, 16:49-17:36 window)` and root cause UNKNOWN. We assumed emergency-pressure-sweeps
were the natural release valve — `pressure_sweep.sh` ran 17:52 freed 60 GiB and was
considered adequate. **It was a one-shot. The structural producers (#1–#5) were not
addressed and continued.** A weekly or daily recurrence on a 50-hour cadence implies
~8 GiB/day of net growth; this matches the measured 30 GiB/50h if it's even partially
active. Embedding the recurrence-class into the memory entry matters more than
the specific numbers (which will be stale within weeks).

## See also

- Bead `disk_magician-7v3` — full root-cause attribution with `du -k -d` outputs and
  reclaimable estimates per cause
- Bead `disk_magician-y7t` (still OPEN) — the 2026-07-26 mass-sweep forensics
- Bead `disk_magician-1f9` — the Antigravity `Retire whole-root AO session .gemini symlinks`
  work (related but distinct from this entry's #4)
- Bead `disk_magician-si1` — machine-wide 14-day floor for worktree deletion (would
  address #1 and #2 if extended to the right worktree roots)
- Bead `disk_magician-yua` — `~/.local/libexec/ezgha` deploy drift (separate issue but
  same pattern: hand-copied deploys with no installer = future-breakage waiting)
- Memory `feedback_2026-07-20_grep_shim_truncates_pipelines_use_python_parsing.md` — why
  every disk sweep needs `du | python3` instead of `du | grep | sort`
