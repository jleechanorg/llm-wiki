# Auto-Research Wiki — karpathy/autoresearch for worldarchitect.ai

**Based on:** karpathy/autoresearch (https://github.com/karpathy/autoresearch)
**Purpose:** Autonomous AI research system — wiki knowledge base + auto-research experiment loop
**Target:** worldarchitect.ai codebase

This repo adapts karpathy's auto-research pattern: an AI agent iteratively experiments on a codebase, evaluates against canonical patterns, and builds knowledge. The wiki is the knowledge layer; the experiment framework is the action layer.

## Slash Commands

| Command | What to say |
|---|---|
| `/wiki-ingest` | `ingest raw/my-article.md` |
| `/wiki-query` | `query: what are the main themes?` |
| `/wiki-lint` | `lint the wiki` |
| `/wiki-graph` | `build the knowledge graph` |

## Directory Layout

```
karpathy/autoresearch origin (read-only experiment harness):
  train.py           # THE FILE YOU MODIFY during experiments
  prepare.py         # Fixed data/eval harness (DO NOT MODIFY)
  program.md         # Experiment instructions

auto-research extension (this repo):
  raw/               # Immutable source documents — arxiv papers, PRs, notes
  wiki/              # LLM knowledge base — sources, entities, concepts, syntheses
    sources/         # One summary page per source document
    entities/         # People, companies, projects
    concepts/         # Ideas, methods, techniques
    syntheses/        # Saved query answers
    index.md          # Catalog of ALL pages
    log.md            # Append-only chronological record
    overview.md        # Living synthesis across all sources
  test-prs/          # [autoresearch] labeled test PRs + results
  canonical-repos/   # Reference code repos for pattern comparison (FastAPI, Requests, etc.)
  research-wiki/      # Full experiment system (cycles A-E, hypotheses, syntheses)
  skills/            # Agent instruction files (self-critique, scoring, taste)

The experiment framework (train.py, prepare.py, program.md) is adapted for worldarchitect.ai research.
```

---

## Core Concept: The Auto-Research Loop

```
wiki/ (knowledge) → test-prs/ (experiments) → research-wiki/ (results) → wiki/ (updated knowledge)
```

**THE GOAL IS REAL PRS.** Every cycle must produce real code that can be pushed and merged. Predictions without real code are failures — not useful evaluations.

For each technique/paper:
1. **Pick a technique** from the wiki (SelfRefine, PRM, ExtendedThinking, etc.)
2. **Form a hypothesis**: "If I apply this to PR type X, I expect Y improvement"
3. **Implement**: Generate fix using the technique
4. **Test on real PRs**: Compare against actual merged commits
5. **Score**: Diff similarity + canonical pattern compliance
6. **Record**: Log to research-wiki/syntheses/cycle_*.md
7. **Iterate or abandon**: Keep if >10% improvement

**What succeeded in Cycles 1-26**: benchmark mode (predicting merged PRs). **What failed**: producing zero real code. Cycles 27+ must produce real PRs on jleechanorg/worldarchitect.ai.

---

## Auto-Research Experiment Cycles (A-E)

| Cycle | Technique | PRs Tested | Status |
|-------|-----------|-----------|--------|
| A | Self-Refine (3-iteration) | 3 | Done |
| B | Extended Thinking | 3 | Done |
| C | Process Reward Models (PRM) | 2 | Done |
| D | Canonical Code Scorer | 3 | Done |
| E | SWE-bench Harness (test-first) | 2 | Done |

---

## Page Format

Every wiki page uses this frontmatter:

```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis
tags: []
sources: []       # list of source slugs that inform this page
last_updated: YYYY-MM-DD
---
```

Use `[[PageName]]` wikilinks to link to other wiki pages.

---

## Ingest Workflow

Triggered by: *"ingest <file>"* or `/wiki-ingest`

Steps (in order):
1. Read the source document fully
2. Read `wiki/index.md` and `wiki/overview.md` for context
3. Write `wiki/sources/<slug>.md` — source page format
4. Update `wiki/index.md` — add entry under Sources section
5. Update `wiki/overview.md` — revise synthesis
6. Create/update entity pages for key people/companies/projects
7. Create/update concept pages for key ideas
8. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Title>`

---

## Research Plan

**Phase 1 (done):** Bootstrap wiki with frontier papers (2022-2026) + canonical repos
**Phase 2 (done):** Run 5-cycle auto-research experiment (A-E) on worldarchitect.ai PRs
**Phase 3 (todo):** Self-discovering meta-research — generate novel hypotheses from results
**Phase 4 (todo):** Final synthesis — what worked, what didn't, recommendations

---

## Scoring: Canonical Pattern Compliance

Rather than comparing against potentially buggy existing code, score generated fixes against **ideal patterns** from canonical repos:

| Dimension | Weight | Source |
|----------|--------|--------|
| Naming | 15% | FastAPI, Requests conventions |
| Error Handling | 20% | FastAPI typed exceptions |
| Type Safety | 20% | TypedDict for data shapes |
| Architecture | 20% | Canonical repo patterns |
| Test Coverage | 15% | Test quality vs complexity |
| Documentation | 10% | Docstrings, comments |

---

## Log Format

```
## [YYYY-MM-DD] operation | title
```

Operations: `ingest`, `query`, `lint`, `graph`, `cycle_a`, `cycle_b`, etc.

---

## Auto-Research Evidence Rule (MANDATORY)

When running experiments (auto-research, benchmark, technique tests):

1. **Run artifacts MUST exist**: stdout logs, commit timestamps, score JSON files
2. **Do NOT declare complete based solely on reading prior-session artifacts**
3. **Wiki-ingest only after run artifacts are committed alongside results**
4. **Session ID required**: Every cycle file must have `run_session: <session_id>` in frontmatter
5. **Verifier agent required**: After all techniques complete, run verification to check each cycle has matching log + score evidence

**Proof of execution required for any technique claim:**
- Log file: `wiki/syntheses/et_logs/<technique>_<pr>_<timestamp>.log`
- Score file: `research-wiki/scores/<technique>_<pr>_<timestamp>.json`
- Cycle file frontmatter must include `run_session`

**If results appear pre-existing and unverifiable**: Say "Cannot confirm live execution — re-run required" and run the experiment fresh.

---

## Router Prerequisite Gate (MANDATORY before any router work)

Any work that implements a PR-type → technique router (bead `br-5bj` and successors) MUST first clear:

```bash
python3 scripts/validate_router_prereqs.py
# exit 0 → unblocked; exit 1 → blocked; exit 2 → input error
```

**Why this gate exists:** All three techniques (SelfRefine, Extended Thinking, PRM) converge within rubric noise (~81-85, CIs overlap). A router can only add value if matched-PR evidence shows ranking reversals — i.e. technique A beats B on PR X while B beats A on PR Y. Bandit means on *different* PR sets cannot prove this, because the variance could be PR-specific, not technique-specific.

**What the gate enforces (do NOT soften these thresholds without user approval):**
- ≥ 5 PRs scored by ALL tracked techniques (rubric_scores entries must carry an explicit `technique` field so matches are unambiguous).
- ≥ 2 ranking reversals across technique pairs.

**If the gate fails:**
1. Do NOT write router code. Do NOT open a router PR.
2. Open or continue the matched-corpus task first: pick 5 PRs, run SR + ET + PRM on each, append to `technique_bandit/bandit_state.json` with proper `technique` fields.
3. Re-run the gate. Proceed only when exit 0.

This rule exists because an earlier session recommended "build the router" based on convergent means on disjoint PR sets — a structural fallacy. The gate is deliberately dumb so smaller/weaker models cannot rationalize around it.

---

## CLI Argument Verification (MANDATORY)

Before calling any CLI tool with required arguments (especially `--run_id`, `--output`, `--report`, or similar output-specifying flags), **read the tool's `--help` and verify all required arguments are present.**

This is a mandatory check, not optional. The SWE-bench harness failed silently because `--run_id` was missing — a required argument that the script never verified.

```bash
# Always verify required arguments before running
python -m swebench.harness.run_evaluation --help
# or
<swebench binary> --help
```

**Why this matters**: Tools with required output-specifying arguments (run_id, report_path, output_file) will silently fail or produce no usable output if those arguments are missing. The failure mode (empty output) looks identical to the failure mode (genuine failure), making the error invisible.

---

## Autor PR Lifecycle (MANDATORY)

**Autor PRs are evaluation artifacts, never merge candidates.** The purpose of opening a PR is to get a scorable diff, not to ship code.

Required lifecycle for every autor-generated PR:
1. **Open as draft** (`gh pr create --draft`) with `[autor]` label and technique tag (`[SR]`, `[ET]`, `[PRM]`).
2. **Score against the 6-dim rubric**; write `research-wiki/scores/<tech>_<pr>_<ts>.json` + `wiki/syntheses/et_logs/<tech>_<pr>_<ts>.log`.
3. **Update bandit state** with explicit `technique` field in `rubric_scores`.
4. **Close the PR** (`gh pr close`) with a comment noting the technique + score. Do not leave it open.

**Do NOT:**
- Open autor PRs as ready-for-review.
- Attempt to merge an autor PR (even if CR approves).
- Interpret "all autor PRs CLOSED" as a failure signal — closed-after-score is the **correct** end state.

**Why:** A CLOSED autor PR with a committed score JSON + log is a successful evaluation. An OPEN autor PR is an incomplete evaluation. A MERGED autor PR is a policy violation. This rule exists because a prior review confused "closed without merge" with "work not done" — autor's goal is the evaluation record, not production code.
