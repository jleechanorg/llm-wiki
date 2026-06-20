---
name: wiki-assess
description: Assess wiki against Karpathy pattern standards
---

# /wiki-assess — Wiki Quality Assessment

## When invoked

Assess any wiki directory against Karpathy gist pattern:
- Structure: sources/entities/concepts in wiki/ subdir
- Ratios: Entity and Concept should be >5% of sources
- Index: Curated summaries, not raw content
- Frontmatter: YAML frontmatter with type field

## Execution

### Phase 1: Check wiki exists
Accept path argument or default to /Users/jleechan/llm_wiki/wiki

### Phase 2: Count pages
```bash
SOURCES=$(ls $WIKI/sources/*.md 2>/dev/null | wc -l)
ENTITIES=$(ls $WIKI/entities/*.md 2>/dev/null | wc -l)
CONCEPTS=$(ls $WIKI/concepts/*.md 2>/dev/null | wc -l)
```

### Phase 3: Calculate ratios
- Entity ratio = ENTITIES / SOURCES * 100
- Concept ratio = CONCEPTS / SOURCES * 100

### Phase 4: Check structure
- Verify wiki/ subdirectory exists
- Verify sources/, entities/, concepts/ subdirs exist
- Check for root duplicates

### Phase 5: Check oracle backlink density
```bash
ORACLE="$WIKI/syntheses/jeffrey-oracle.md"
# Count outbound links — both MD links [text](path.md) and legacy [[wikilinks]]
OUTBOUND_MD=$(grep -oE '\[[^\]]+\]\([^)]+\.md\)' "$ORACLE" 2>/dev/null | sort -u | wc -l)
OUTBOUND_WIKI=$(grep -oE '\[\[[^]]+\]\]' "$ORACLE" 2>/dev/null | grep -v '|' | sort -u | wc -l)
OUTBOUND=$((OUTBOUND_MD + OUTBOUND_WIKI))
INBOUND=$(grep -rl 'jeffrey-oracle' "$WIKI"/**/*.md 2>/dev/null | wc -l)
```
Target: outbound ≥15, inbound ≥10.

### Phase 5b: Check for unconverted wikilinks (GitHub link health)
```bash
# Count raw [[wikilinks]] in concepts/ and entities/ (outside code fences)
WIKILINKS=$(grep -rh '\[\[' "$WIKI/concepts" "$WIKI/entities" 2>/dev/null | \
  grep -v '^\s*```' | grep -c '\[\[' || true)
```
Target: 0. Any `[[wikilinks]]` outside code blocks are invisible on github.com.

### Phase 6: Output assessment

```
## Wiki Assessment: <wiki_path>

### Structure: ✅/❌
### Ratios:
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Sources | N | - | - |
| Entities | N | - | - |
| Concepts | N | - | - |
| Entity ratio | X% | >5% | ✅/❌ |
| Concept ratio | X% | >5% | ✅/❌ |

### Index Quality: ✅/❌
### Frontmatter: ✅/❌

### Oracle Backlink Density:
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Outbound links from oracle (MD + wikilinks) | N | ≥15 | ✅/❌ |
| Inbound links to oracle | N | ≥10 | ✅/❌ |

### GitHub Link Health:
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Raw [[wikilinks]] in concepts+entities | N | 0 | ✅/❌ |

### Verdict: COMPLIANT / NON-COMPLIANT
```

## Example usage
- `/wiki-assess` — assess default llm_wiki
- `/wiki-assess ~/memory/wiki` — assess memory wiki