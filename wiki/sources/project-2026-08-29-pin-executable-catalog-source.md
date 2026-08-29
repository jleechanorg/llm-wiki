---
title: "Pin executable catalog source, not only its documentation link"
type: source
tags: [skills, catalog, reproducibility, git, worldarchitect]
last_updated: 2026-08-29
source_file: /Users/jleechan/llm_wiki/raw/project_2026-08-29_pin_executable_catalog_source.md
---

# Pin executable catalog source, not only its documentation link

## Finding

A revision-qualified documentation URL does not pin a `git clone` command
inside that document. Reproducible catalog installation requires an explicit
detached checkout of the compatible source SHA before running the installer.

Installation and discovery are separate contracts: `CLAUDE_HOME` selects the
destination, while `CLAUDE_CONFIG_DIR="$CLAUDE_HOME"` makes the verification
host discover that isolated catalog.

## Evidence

- WorldArchitect PR #9485 final head: `0b3e186877ddc5936e0ffb3ba1d5f168bf738703`
- Compatible catalog: `41ce34ba240f4d5e8ff5c479907db4887598ce00`
- Squash merge: `9a2b26e71a474e3ab86b5486201d6d91fa6f6401`
- Independent review: two reviewers covered 25/25 changed paths; one executed the detached checkout and installer.
- Related concept: [[skill-consolidation-pattern]]

This operational workflow learning does not affect [[jeffrey-oracle]].
