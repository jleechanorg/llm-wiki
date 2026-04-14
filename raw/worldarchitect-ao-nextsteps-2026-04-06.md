# WorldArchitect.AI + Agent Orchestrator — next steps (2026-04-06)

Handoff report: evidence enforcement, beads, and cross-repo follow-ups.

## WorldArchitect.AI (`jleechanorg/worldarchitect.ai`)

### Landed

- [PR #6110](https://github.com/jleechanorg/worldarchitect.ai/pull/6110) merged (evidence path, `evidence-gate.yml`, orchestration completion `exit_code`, beads).
- [PR #6115](https://github.com/jleechanorg/worldarchitect.ai/pull/6115) merged (roadmap `/nextsteps` + related beads/docs on branch `chore/nextsteps-2026-04-06`).

### Why evidence is not “fully enforced” yet

- `Evidence Bundle Validation` job name is misleading: it checks **repo structure** (grep, stubs, `py_compile`), not real `/tmp` bundles or video.
- Workflow runs only on PRs touching `testing_mcp/**`, `testing_ui/**`, or the workflow file — many PRs **never** run it.
- **Branch protection:** “Validate Evidence Bundles” must be added as a **required** check on `main` (admin).

### Priority beads (WA, prefix `rev-`)

| ID | Focus |
|----|--------|
| **rev-b8a0** | GitHub: require **Validate Evidence Bundles** on `main` (branch protection / rulesets). |
| **rev-3oon** | CI: validate **real bundle artifacts** (checksums under `EVIDENCE_TMP_ROOT`), not only static checks. |
| **rev-owc1** | Broaden **`evidence-gate.yml`** path triggers or document policy so gates cannot be skipped silently. |
| **rev-g41u** | Land / verify **AO PR #335** installer (`install-skeptic-ci-for-repo.sh`). |
| **rev-zz65** | [PR #6034](https://github.com/jleechanorg/worldarchitect.ai/pull/6034) wizard — conflicts + review. |
| **rev-revgejn** | Harness: **`git worktree prune`** after removing worktrees (`pair_execute_v2` / pairv2). |

### Dependency note

- **rev-3oon** `discovered-from` **rev-b8a0** (policy/required-check context before deeper CI).

---

## Agent Orchestrator (`jleechanorg/agent-orchestrator`)

### Repo / branch

- Local clone used: `/Users/jleechan/projects/agent-orchestrator-skeptic-wt`.
- Beads pushed on branch **`ao-beads-20260406`** — **open a PR** to `main` when ready:  
  [Compare / PR](https://github.com/jleechanorg/agent-orchestrator/compare/main...ao-beads-20260406?expand=1).

### Priority beads (AO, prefix `bd-`)

| ID | Focus |
|----|--------|
| **bd-f6uh** | Cross-repo: align consumer evidence gates with WA rollout (**depends on** **bd-wx84**). |
| **bd-wx84** | Verify **PR #335** installer on `main`; update consumer one-liners (links **WA rev-g41u**). |
| **bd-5g09** | Policy: workers attach **real media evidence** when job class requires (ties **bd-7x6y**, **bd-806w**). |
| **bd-7x6y** | Skeptic: evidence defaults **N/A** — evaluate authenticity when required. |

---

## Files (this handoff)

| Path | Purpose |
|------|---------|
| `/Users/jleechan/Downloads/worldarchitect-ao-nextsteps-2026-04-06.md` | This report. |
| `/Users/jleechan/Downloads/memory-snippet-worldarchitect-ao-2026-04-06.txt` | Short bullets for paste into mem0 / Cursor / other memory tools. |
| `/Users/jleechan/Downloads/beads.db.bak-20260406` | Optional **SQLite backup** of WA `.beads/beads.db` taken before DB rebuild (recovery only). |
| `/Users/jleechan/roadmap/followups-worldarchitect-ao-2026-04-06.md` | **Roadmap** copy of follow-ups. |
| `/Users/jleechan/roadmap/MEMORY-followups-2026-04-06.txt` | **Ultra-compact** lines for memory paste. |

## New handoff beads (created with `br`)

- **WA:** **rev-s4ja** — “Handoff 2026-04-06: next steps report (Downloads + evidence priorities)” (`external_ref`: `wa-handoff-report-20260406`).
- **AO:** **bd-ear4** — “Handoff 2026-04-06: next steps report (Downloads + AO PR + cross-repo)” (`external_ref`: `ao-handoff-report-20260406`).

### WA `issues.jsonl` maintenance (2026-04-06)

- `br` import failed on **multi-hyphen** issue ids (e.g. `rev-stream-sign-env`). Those **13** ids were renamed to **`rev-{6-hex}`** (stable hash of the old id); **duplicate id lines** were collapsed to **726** unique issues.
- **rev-6e42c1** (ex–stream retry latency): fixed **`updated_at` &lt; `created_at`** and set **`closed_at`** for validation.

---

## Suggested order of work

1. **Admin:** Add required check **Validate Evidence Bundles** on WA `main` (**rev-b8a0**).
2. **Engineering:** Extend evidence CI to real bundle validation (**rev-3oon**).
3. **Engineering:** Widen evidence-gate triggers or document exceptions (**rev-owc1**).
4. **AO:** Open/merge PR **`ao-beads-20260406`**; complete **bd-wx84** → **bd-f6uh**.
5. **Cross-repo:** Keep **rev-g41u** / **bd-wx84** / PR #335 in sync.

---

*Generated for session handoff. Update beads with `br` as work completes.*
