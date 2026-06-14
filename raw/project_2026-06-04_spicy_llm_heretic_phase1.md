---
name: spicy_llm — Heretic abliteration Phase 1 (M4 Pro)
description: Repo state after Phase 1 (prebuilt smoke test) — 1 commit unpushed, 2 new execution beads, MPS dual-load OOM still unroot-caused, kernels patches known-working but not ported to repo
metadata:
  type: project
  bead: jleechan-sj4, jleechan-12z, jleechan-k1f, jleechan-rz0, jleechan-u7i
---

## What this repo is

`jleechanorg/spicy_llm` (public, owner `jleechanorg`) — research repo for local abliteration ("decensoring") of open-weights LLMs using [p-e-w/heretic](https://github.com/p-e-w/heretic) on Apple Silicon. Not a packaged product — a reproducibility + evidence harness.

**Hardware target:** Apple M4 Pro, 14 cores, 51 GB unified memory, Metal 3.

**Local path:** `/Users/jleechan/projects_other/spicy_llm`

## State as of 2026-06-04

- **Local `main` is 1 commit ahead of `origin/main`** — commit `6992f02` (Hermes, "Phase 1: smoke-test heretic 20B vs stock (drugs + erotica + coding)"). Push is mine when I'm ready.
- **Phase 1 (prebuilt smoke test) done** — 3 probes (drug synthesis, erotica, Fibonacci) on `svjack/gpt-oss-20b-heretic` vs stock `gpt-oss:20b`. Both comply on harmful prompts, both handle benign. Transcripts at `results/phase1-smoke/`. `REPORT.md` committed.
- **Phase 2 (DIY ablation) unproven on M4 Pro** — Session 2 attempt on Qwen3-4B stalled at batch-128 for 30+ min.

## Open work (beads)

| Bead | Owner | What |
|------|-------|------|
| `jleechan-12z` | jleechan2015 → Hermes | Long-context erotica A/B; also doubles as MPS OOM reproducer |
| `jleechan-k1f` | jleechan2015 → Hermes | Re-run DIY Heretic on `gemma3:4b` with `--batch-size 32` from t=0 |
| `jleechan-sj4` | jleechan2015 | Doc MPS OOM / Ollama 500 root cause (transient, retry-resolved) |
| `jleechan-rz0` | (unowned) | Make repo reproducible from committed files (port kernel patches, scripts, BENCHMARK_PROTOCOL) |
| `jleechan-u7i` | (unowned) | Fix `.gitignore` allowlist — Hermes's `results/*` is wrong, needs `results/**` |
| `jleechan-a0z` | (unowned) | Review spicy_llm code |
| `jleechan-ob1` | (unowned) | Add sanitized or gate-friendly transcript artifact path (P3) |

## Slack coordination split (per msg 1780623008)

- **Hermes (M4 Pro execution):** writes to `results/**`, `patches/`. Owns the long-context erotica run, DIY rerun, kernel patch port.
- **Me (repo/docs/beads):** writes to `docs/**`, `.gitignore`, README, `~/.beads/`. Owns .gitignore fix, kernel patch port (in `patches/`), BENCHMARK_PROTOCOL draft, README status updates.
- **Push serialization:** "I pushed X first" before each `git push` to avoid collisions.

## Known M4 Pro footguns (write to `docs/RESEARCH_PLAN.md` if not yet)

1. **`kernels` package import crash on macOS / Python 3.12** — `hub_kernels.py` registers `LayerRepository` calls without `revision=` or `version=`. The `kernels/layer/layer.py` + `func.py` `__init__` then raise `ValueError: Either a revision or a version must be specified`. Fix: default `revision="main"` in BOTH `kernels/layer/layer.py` and `kernels/layer/func.py`. Patches live in `/private/tmp/heretic/.venv/lib/python3.12/site-packages/kernels/layer/` and need porting to `patches/` in the repo.

2. **Batch-128 stall in Heretic auto-detection on M4 Pro** — process alive, CPU 17-87%, RSS drops 89→23 MB (model offloaded), `tee` log stops flushing for 30+ min. Workaround: `--batch-size 32 --max-batch-size 32` from t=0. Also use `unbuffer python -u heretic ... 2>&1 | tee -a` to fix the line-buffered `tee` issue.

3. **Dual-model Ollama OOM on M4 Pro (transient)** — running with stock 13 GB + heretic 15 GB loaded, first request to heretic on benign prompt returns Ollama 500. Retry with shorter response succeeds. Theory: MPS kills the lower-RSS runner when context exceeds 8 GB allocation. Workaround candidates: unload stock first, `OLLAMA_NUM_PARALLEL=1`, `num_ctx=2048`. Repro: see `jleechan-12z`.

## What's already on disk (not yet committed at session start)

- `heretic/` (gitignored — local upstream clone, see heretic/SOURCE.md in 6992f02)
- `results/phase1-smoke/` (committed in 6992f02)
- `AGENTS.md` and `CLAUDE.md` (untracked as of 2026-06-04 18:21 — user/linter added them, per the system reminder)

## How to resume in a fresh session

1. `cd /Users/jleechan/projects_other/spicy_llm`
2. `git log --oneline -3` to see local state vs origin
3. `br list --status open --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('\n'.join(f\"{b['id']:18s} P{b.get('priority',0)} {b.get('title','')}\" for b in d if 'spicy_llm' in (b.get('labels') or [])))"`
4. Check the Slack thread `C09GRLXF9GR` for the latest msg — Hermes may have started or finished `jleechan-12z` / `jleechan-k1f`

**Why:** A fresh agent joining this repo (Claude Code, Codex, Hermes, etc.) needs to know: (a) where the local-vs-remote state diverges, (b) which beads are open and who owns them, (c) the M4 Pro footguns so they don't re-discover them. This memory captures all three.

**How to apply:** When a future session touches `spicy_llm`, read this memory FIRST. It cuts the "what is this repo / what's done / what's blocked" discovery loop from ~15 min to ~30 sec.
