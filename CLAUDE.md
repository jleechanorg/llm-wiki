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

For each technique/paper:
1. **Pick a technique** from the wiki (SelfRefine, PRM, ExtendedThinking, etc.)
2. **Form a hypothesis**: "If I apply this to PR type X, I expect Y improvement"
3. **Implement**: Generate fix using the technique
4. **Test on real PRs**: Compare against actual merged commits
5. **Score**: Diff similarity + canonical pattern compliance
6. **Record**: Log to research-wiki/syntheses/cycle_*.md
7. **Iterate or abandon**: Keep if >10% improvement

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
