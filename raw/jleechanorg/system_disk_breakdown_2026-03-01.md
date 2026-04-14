# Disk Breakdown Report (System-level, 2026-03-01)

Source run:

- Command: `./scripts/system_disk_async_map.sh /tmp/system_disk_async_map_full`
- Raw output: `/tmp/system_disk_async_map_full`
- Timestamp: `2026-03-01` (latest run completed in this session)

---

## 1) Overall capacity

- **APFS total:** 994.7 GB
- **Used:** 986.4 GB (99.2%)
- **/System/Volumes/Data used:** 932.5 GB

---

## 2) Top-level on /System/Volumes/Data (what is dominating)

Computed against the Data volume (932.5 GB):

| Path         | Size    | % of Data |
|--------------|---------|-----------|
| /Users       | ~882.2 GB | ~94.6%  |
| /Applications| 17 GB   | ~1.8%   |
| /private     | 15 GB   | ~1.6%   |
| /Library     | 9.1 GB  | ~1.0%   |
| /opt         | 8.5 GB  | ~0.9%   |
| /usr         | 731 MB  | ~0.08%  |
| /tmp         | 0 B     | (at top-level) |
| /var         | 0 B     | (at top-level) |
| /Volumes     | 0 B     | (at top-level) |

**Dominant driver:** `/Users` (~94.6% of Data).

---

## 2b) /Users breakdown — Full Second Pass (≈882 GB total)

*Second pass completed 2026-03-01 via targeted `du -sh` on all top-level home entries.*

### Tier 1: Massive (10+ GB each) — ~640 GB

| Path | Size | Notes |
|------|------|-------|
| `~/projects/` | 135 GB | 73 GB = `orch_worldarchitect.ai` (274 harness worktrees) |
| `~/Library/` | 99 GB | see §2c for sub-breakdown |
| `~/projects_other/` | 51 GB | 31 GB = `codex_fork` |
| `~/project_ai_universe/` | 50 GB | |
| `~/actions-runner/` | 47 GB | GitHub Actions self-hosted runner |
| `~/actions-runner-2/` | 42 GB | second runner |
| `~/.codex/` | 39 GB | 35 GB sessions, 4 GB sqlite |
| `~/.cache/` | 24 GB | 18 GB = `uv` package cache |
| `~/.cursor/` | 15 GB | 15 GB worktrees |
| `~/.gemini/` | 10 GB | 6.4 GB tmp, 2.6 GB antigravity |
| `~/project_ai_universe_frontend/` | 10 GB | |
| `~/Desktop/` | 10 GB | |
| `~/.claude/` | 9.5 GB | 4.7 GB projects, 3.5 GB debug |

### Tier 2: Medium (1–10 GB) — ~65 GB

| Path | Size |
|------|------|
| `~/Downloads/` | 8.7 GB |
| `~/.nvm/` | 5.0 GB |
| `~/.local/` | 5.1 GB |
| `~/project_jleechanclaw/` | 4.4 GB |
| `~/.npm/` | 4.1 GB |
| `~/.pyenv/` | 3.9 GB |
| `~/.rustup/` | 3.6 GB |
| `~/project_worldaiclaw/` | 2.9 GB |
| `~/project_ai_universe_convo/` | 1.7 GB |
| `~/conductor/` | 1.5 GB |
| `~/worldarchitect.ai/` | 1.4 GB |
| `~/claude-codex-usage/` | 1.4 GB |

### Tier 3: Small (<1 GB)

`~/.bun` (670 MB), `~/.cargo` (627 MB), `~/mcp_mail` (568 MB), `~/openclaw-repo` (497 MB), worktree stubs in home root (~1.2 GB combined), misc dotfiles and temp files.

---

## 2c) ~/Library sub-breakdown (99 GB)

| Path | Size | Notes |
|------|------|-------|
| `Library/Containers` | 32 GB | **31 GB = Docker** (`com.docker.docker`) |
| `Library/Application Support` | 27 GB | 12 GB Claude, 4.5 GB Cursor, 3 GB Comet, 2.7 GB Google |
| `Library/Messages` | 24 GB | **23 GB = iMessage Attachments** |
| `Library/Mail` | 5.5 GB | |
| `Library/Caches` | 2.8 GB | |
| `Library/Metadata` | 2.1 GB | |
| `Library/Python` | 1.9 GB | |
| `Library/pnpm` | 1.6 GB | |
| `Library/Group Containers` | 1.4 GB | |
| rest | ~1.5 GB | Logs, Biome, Photos, etc. |

---

## 2d) ~/projects/ sub-breakdown (135 GB)

| Path | Size | Notes |
|------|------|-------|
| `orch_worldarchitect.ai/` | 73 GB | 274 `harness*` worktree dirs (~1 GB each) |
| `orch_jleechanclaw/` | 9.5 GB | |
| `worktree_genesis/` | 4.5 GB | |
| `worldarchitect.ai/` | 3.3 GB | |
| `worktree_logs/` | 2.8 GB | |
| 10+ other worktrees | ~1–1.6 GB each | `worktree_worker*`, `worktree_pr_*`, etc. |
| `openclaw-docs/` | 1.2 GB | |

---

## 3) Big confirmed detail buckets

| Path                       | Size    |
|----------------------------|---------|
| /Applications/Xcode.app   | 4.9 GB  |
| /Library/Developer        | 5.8 GB  |
| /private/var              | 11 GB   |
| ~/.cursor                 | 15 GB   |
| ~/.gemini                 | 10 GB   |
| ~/Desktop                 | 10 GB   |
| ~/Downloads               | 8.7 GB  |

### Drill-down (selected)

**/Applications** (17 GB total)

- Xcode.app — 4.9 GB (single largest app bundle)
- Docker.app — 1.9 GB
- Google Chrome.app — ~1.3 GB
- Cursor.app — 1.1 GB
- TikTok LIVE Studio.app — 1.3 GB

**/Library/Developer** (5.8 GB)

- CoreSimulator/Caches/dyld/... — 3.5 GB (includes simulator dyld shared cache)
- Large file >2 GB noted (dyld cache)

**/private/var** (11 GB)

- /private/var/db — 4.8 GB
- /private/var/folders — 4.6 GB
- Diagnostics and app code-sign clone caches — multiple ~1.3 GB blocks

---

## 4) /tmp current large trees

Top `/tmp` entries (note: /tmp may show 0 B at top-level; large trees live under it):

| Path                          | Size   |
|-------------------------------|--------|
| /tmp/worldarchitect.ai        | 2.9 GB |
| /tmp/pr-orch-bases            | 1.1 GB |
| /tmp/pr-orch-bases/jleechanorg/jleechanclaw | 817 MB |

---

## 5) System volumes outside Data

| Volume                     | Size   |
|----------------------------|--------|
| /System/Volumes/Preboot    | 14.5 GB |
| /System/Volumes/VM         | 20 GB   |
| /System/Volumes/Update     | 750 MB  |
| / (system)                 | 17.8 GB |

---

## 6) Reproducible breakdown pipeline

```bash
./scripts/system_disk_async_map.sh /tmp/system_disk_async_map_latest
du -h -d 1 /tmp/system_disk_async_map_latest/*.size 2>/dev/null
```

For a full drilldown, inspect:

```bash
cat /tmp/system_disk_async_map_latest/Users.children
cat /tmp/system_disk_async_map_latest/private.children
cat /tmp/system_disk_async_map_latest/Library.children
cat /tmp/system_disk_async_map_latest/opt.children
cat /tmp/system_disk_async_map_latest/tmp.children
```

---

## 7) Cleanup Performed (2026-03-01)

| Target | Before | After | Freed | Method |
|--------|--------|-------|-------|--------|
| `orch_worldarchitect.ai/harness*` (274 dirs) | 73 GB | 2 GB | **71 GB** | `rm -rf harness*` |
| `actions-runner*/.old-ws-*` (73 dirs) + `ci-stale-*` (131 dirs) | 84 GB | 4.2 GB | **~80 GB** | `chmod + rm` |
| `~/.cache/uv/` | 18 GB | 0 | **15 GiB** | `uv cache clean --force` |
| `~/projects_other/codex_fork/` | 31 GB | 0 | **31 GB** | `rm -rf` (re-clonable) |
| `~/.gemini/tmp/` | 6.4 GB | 0 | **6.4 GB** | `rm -rf` |

**Pass 1 total: ~194 GB freed.**

### Pass 2: Project worktrees (2026-03-01, continued)

| Target | Before | After | Freed | Method |
|--------|--------|-------|-------|--------|
| `project_ai_universe/worktree_*` (64 dirs) | 50 GB | 5 GB | **~45 GB** | `find -mtime +14 -exec rm -rf` |
| `project_ai_universe_frontend/worktree_*` (20 dirs) | 10 GB | 889 MB | **~9 GB** | same |
| `project_ai_universe_convo/worktree_*` (11 dirs) | 1.7 GB | 306 MB | **~1.4 GB** | same |
| `~/projects` stale dirs (env, orch, snap, etc.) | 135 GB | 62 GB | **~8 GB** | same |
| Home root stale worktrees | 530 MB | 0 | **530 MB** | same |

**Pass 2 total: ~64 GB freed.**

### Pass 3: Caches and old backups (2026-03-01, continued)

| Target | Size | Freed | Method |
|--------|------|-------|--------|
| `~/.npm` cache | 4.2 GB | **4.2 GB** | `npm cache clean --force` |
| `~/.claude/debug/` | 3.6 GB | **3.6 GB** | `rm -rf` contents |
| `~/.cache/puppeteer/` | 2.5 GB | **2.5 GB** | `rm -rf` |
| `~/.claude.backup.*` (80+ dirs) | 2.6 GB | **2.6 GB** | `rm -rf` |
| `~/.claude/projects.backup.*.20250905` | 594 MB | **594 MB** | `rm -rf` |

**Pass 3 total: ~13 GB freed.**

### Grand Total: ~280 GB freed. Disk: 99.2% (8 GB free) -> 69% (285 GB free).

### PRESERVED (do not delete)

| Path | Size | Reason |
|------|------|--------|
| `~/.codex/sessions/` | 35 GB | Codex conversation history — valuable records |
| `~/.claude/` | 9.5 GB | Claude conversation/project data — valuable records |

### Not cleaned (Docker not running)

| Target | Size | Action needed |
|--------|------|---------------|
| Docker (`Library/Containers/com.docker.docker`) | 31 GB | `docker system prune -a` when Docker is running |

### Not cleaned (< 2 weeks old)

| Target | Size | Notes |
|--------|------|-------|
| `~/.cursor/worktrees/` | 15 GB | Only 1 dir, created today |
| `/tmp/worldarchitect.ai` + `/tmp/pr-orch-bases` | 4 GB | Actively used |

### Remaining targets for future cleanup

| Target | Size | Notes |
|--------|------|-------|
| Docker (`Library/Containers/com.docker.docker`) | 31 GB | `docker system prune -a` when daemon is running |
| `~/Library/Messages/Attachments/` | 23 GB | iMessage media — manual in Messages app |
| `~/Library/Application Support/Claude` | 12 GB | Investigate before cleaning |
| `~/.nvm` old versions | 5 GB | `nvm uninstall` unused versions |
| `actions-runner .ci-container-secrets` | ~few MB | Need sudo to remove |

---

## 8) Root Cause: Actions-Runner Bloat

The `actions-runner/_work/worldarchitect.ai/` directory accumulates:
- `.old-ws-*` hidden dirs: stale workspace snapshots from CI jobs not cleaned after completion
- `ci-stale-*` dirs: stale CI worktrees from docs/test jobs

These are created by GitHub Actions workflows and never cleaned up. Consider adding a periodic cleanup cron or post-job step.

---

## 9) Fix: Harness worktrees redirected to /tmp

**PR change** in `orchestration/task_dispatcher.py`:
- `_get_worktree_base_path()` now defaults to `/tmp/orch_worktrees/orch_{repo_name}/` instead of `~/projects/orch_{repo_name}/`
- New env var `ORCHESTRATION_WORKTREE_BASE` allows override if persistence is needed
- Prevents future accumulation of ephemeral pair-programming worktrees in home dir

---

## 10) Summary

- Recovered **~280 GB** across 3 passes (99.2% -> 69% disk usage, 285 GB free).
- Root causes: stale orchestration harness worktrees (71 GB), stale CI workspace snapshots in actions-runner (80 GB), project worktrees (64 GB), dev tool caches (65 GB).
- Codex sessions and Claude project data preserved per policy.
- Harness worktrees redirected to `/tmp` via PR #5810 to prevent recurrence.
- Reusable cleanup: `scripts/disk_cleanup.sh` (dry-run default).
- Methodology documented: `docs/disk_cleanup_methodology.md`.
