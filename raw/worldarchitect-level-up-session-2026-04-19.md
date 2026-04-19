# WorldArchitect.AI — Level-up / Layer 2 session digest (2026-04-19)

**Scope:** Same-day PR truth, merge order, gates, beads, roadmap pointers, parallel-work rules, story-persistence learning. **Repo:** `jleechanorg/worldarchitect.ai`.

## PR inventory (verify with `gh pr view` before acting)

**Merged (2026-04-19):** #6372 (split C repro), #6373 (split D docs/beads/wiki), #6397 (testing_mcp pip_py after venv).

**Closed without merge:** #6376 (god-mode planning strip — review closed), #6395 (skeptic checklist docs).

**Open:** #6370 (split A canonicalization), #6377 (atomic level-up UI repro), #6379 (contract gate, base `test/level-up-centralization-migration`), #6386 (schema cache), #6387 (migration to `main`), #6278 (SelfRefine scoring), #6289 (design-doc skill, often conflicting), #6398 (story persistence reload parity harness docs).

## Merge order (desired)

1. **Split A to `main`:** #6370 — remaining production canonicalization after #6372/#6373 landed.
2. **Migration stack (physical):** #6379 into `test/level-up-centralization-migration`, then #6387 to `main`.
3. **Parallel:** #6386, #6377, #6278, #6289, #6398 — by readiness and file overlap; #6289 needs conflict resolution first.

## Gates and evidence

- **`gh pr checks` is insufficient** for “7-green”; use `/Users/jleechan/.claude/skills/pr-green-definition/SKILL.md`: CI, mergeable, CodeRabbit **APPROVED**, Bugbot clean, threads resolved, evidence gate, Skeptic **VERDICT: PASS** for current head.
- **Gate 6 ≠ Skeptic alone:** Skeptic Gate enforces ~1–5 + polls VERDICT; full evidence standards live under `~/.claude/skills/evidence-standards/` (beads: `rev-jpq4`, `rev-mmq0`).

## Agent-only sessions

- Progress ≠ merges when no human operator: track **branch health**, **Green Gate run URL + SHA + per-gate PASS lines** (see `~/roadmap/nextsteps-2026-04-19.md`, bead `rev-o0pd`).
- **Lane declaration:** one PR# per session before edits.
- **#6386 firewall:** schema lane must not absorb migration-sized `world_logic`/`rewards_engine` diffs.

## Beads / roadmap

- `rev-vief`: Layer 2 queue; `rev-rzkn` / `rev-rzkn.3`: contract + migration; **rev-rzkn.2** closed after #6392 reconciliation.
- Rolling docs: `/Users/jleechan/roadmap/README.md`, `/Users/jleechan/roadmap/learnings-2026-04.md`, `/Users/jleechan/roadmap/2026-04-19-layer2-centralization-nextsteps.md`.

## Story persistence (critical product tenet)

- **Round-trip parity:** reloading the page must show the same planning/rewards-facing UX state; do not strip `planning_block` at persistence without reload-proof waiver (see `~/roadmap/learning-2026-04-19-story-persistence-reload-parity.md`, skill `story-persistence-reload-parity`, PR #6398 thread).

## Parallel work (safe)

Disjoint verification (Green Gate logs), roadmap-only edits, merge-tree analysis on different heads — **not** two writers on the same PR branch or simultaneous `.beads/issues.jsonl` merges.

## Branches note

Many local topic branches exist (`codex/*`, `test/*`, `feat/*`); **authoritative head** for merge planning is **GitHub PR head** + **`main`**, not unmerged local branches.
