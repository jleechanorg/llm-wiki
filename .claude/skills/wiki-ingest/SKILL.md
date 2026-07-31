---
name: wiki-ingest
description: Use when ingesting a source document into the local LLM Wiki and updating related indexes, entities, concepts, and logs
---

# /wiki-ingest — Ingest a file into the LLM Wiki

## Usage
```
/wiki-ingest <file_or_path>
```

Ingest a source document into the wiki. Creates a source page, extracts entities and concepts, updates the index.

## Execution

### Phase 1: Resolve source file
```bash
WIKI="$HOME/llm_wiki/wiki"
SOURCE="$HOME/llm_wiki/raw/$(basename "<arg>")"

# Copy source to raw/ if not already there
mkdir -p "$(dirname "$SOURCE")"
cp "<arg>" "$SOURCE" 2>/dev/null || cp "$(pwd)/<arg>" "$SOURCE"

# Determine slug from filename
SLUG=$(basename "<arg>" | sed 's/\.md$//' | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]')
```

### Phase 2: Read source document
Read the file fully.

### Phase 3: Read wiki context
Read `wiki/index.md` and `wiki/overview.md` for current wiki state.

### Phase 4: Create source page
Write `wiki/sources/<slug>.md` using Source Page Format:

```markdown
---
title: "<title>"
type: source
tags: []
date: YYYY-MM-DD
source_file: <relative path>
---

## Summary
2–4 sentence summary.

## Key Claims
- Claim 1
- Claim 2

## Key Quotes
> "Quote here" — context

## Connections
- [EntityName](../entities/EntityName.md) — how they relate
- [ConceptName](../concepts/ConceptName.md) — how it connects
```

**GitHub link rule**: Always use `[Name](../dir/Name.md)` markdown links — NEVER `[[wikilinks]]`.
`[[wikilinks]]` render as plain text on github.com; only standard markdown links are clickable.
- From `sources/`: use `../entities/Name.md` or `../concepts/Name.md`
- From `entities/` or `concepts/`: use `../concepts/Name.md`, `../entities/Name.md`, or `Name.md` (same dir)
- From `wiki/index.md`: use `entities/Name.md` or `concepts/Name.md`

### Phase 5: Update index
Add entry to `wiki/index.md` under Sources section. Use `[Title](sources/slug.md)` markdown link.

### Phase 6: Oracle impact check
Check if new content affects [jeffrey-oracle](../syntheses/jeffrey-oracle.md). If so, append to `wiki/log.md`.

### Phase 7: Entity & concept extraction
Create entity pages for key people, companies, projects.
Create concept pages for key ideas, frameworks, methods.
Use `[Name](../dir/Name.md)` links in all new pages — never `[[wikilinks]]`.

### Phase 8: Log
Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Title>`
