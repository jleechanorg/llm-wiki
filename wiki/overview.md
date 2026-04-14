# Overview

This wiki is a consolidated knowledge base maintained entirely by Claude Code. It spans two major sections:

1. **Original Wiki** — 27K+ sources covering campaigns, research papers, PR histories, and code analysis
2. **Auto-Research Experiment v2.1** — A self-improving coding agent that runs hypothesis-driven experiments against real PRs

---

## Original Wiki Content

The bulk of the wiki covers TTRPG campaign logs, AI research papers, and software engineering analysis.

**Campaigns (jleechan/):** Deep psychological profiles and choice patterns from 500+ turn campaigns. Key themes include serpent-mastermind INTJ archetypes, moral corruption arcs, and third-option cognition. See [[Player Psychology]] and [[character-archetypes]].

**Research Papers:** Canonical papers on transformers, RLHF, coding agents, and agent architecture. Ingested from `raw/` and organized into [[sources/]] with entity and concept extraction.

**PR Histories:** WorldArchitect.AI PR analysis from worldarchitect.ai, worldai_claw, agent-orchestrator, and jleechanclaw repos. Covers level-up systems, streaming architecture, normalization pipelines, and evidence standards. See [[Level-Up Bug Chain]] and [[Normalization Bypass]].

**Canonical Code Analysis:** Ingested patterns from FastAPI, tRPC, Requests, Axum — used as the Auto-Research Experiment's pattern library.

---

## Auto-Research Experiment v2.1

A master AI research system combining LLM wiki + self-discovering meta-research + self-critique verification + canonical scoring.

### What It Does

The system runs autonomous coding improvement cycles against real historical PRs:

1. **Hypothesis Generation** — Analyze PR patterns in `test-prs/`, generate novel falsifiable hypotheses
2. **Implementation** — Run [[SelfCritiqueVerificationLoop]] (prompt chain + generation + sandboxed tests + self-critique, max 3 iterations)
3. **Evaluation** — Score baseline vs technique output using [[CanonicalCodeScorer]] (6-dimension rubric 70% + diff similarity 30%)
4. **Update** — Record results in wiki + create bead for every run

### Key Components

| Component | Role |
|---|---|
| [[AutoResearchLoop]] | Master 4-phase orchestration |
| [[SelfCritiqueVerificationLoop]] | Inner loop: generation + test + critique |
| [[CanonicalCodeScorer]] | Hybrid scoring: rubric + diff similarity |
| [[AutoResearchExperiment]] | Top-level concept page |

### Directory Structure

```
llm_wiki/
├── sources/              # Ingested source pages (papers, PRs, campaigns)
├── wiki/concepts/        # Concept pages for techniques and methods
├── wiki/entities/        # Entity pages for people, projects, repos
├── canonical-repos/      # Reference repos: fastapi/, trpc/, requests/, axum/
├── test-prs/             # 19 historical PR files (pr-6212 through pr-6269)
├── skills/               # 5 skill files (auto-research-loop, self-critique, etc.)
├── scripts/              # verify_setup.sh bootstrap script
├── research-wiki-program.md   # Master instruction set
└── research-wiki-results.md   # Experiment log (18 cycles)
```

### 18-Cycle Experiment Results

- **Score range:** 53–86/100
- **Type Safety** — systematically FAIL across all cycles (pervasive `Any` types, `ignore-errors` pragmas)
- **Highest:** Shell CI scripts at 86/100
- **Pattern:** Iterations that pass tests but still score mid-range due to type safety and documentation gaps
- See [[AutoResearchExperiment]] for full 18-cycle breakdown

---

## Cross-Cutting Themes

- **[[ZeroFrameworkCognition]]** — Delegate all reasoning to AI; forbidden patterns (keyword routing, heuristic scoring, regex intent detection)
- **[[Harness5LayerModel]]** — L1 Constraint, L2 Context, L3 Execution, L4 Verification, L5 Lifecycle
- **[[Level-Up Systemic Fix]]** — game_state.py canonicalizer self-undo bug, computed @property level
- **[[Normalization Atomicity]]** — All Firestore-persisted rewards_box must canonicalize; passthrough path name does not mean skip normalization
