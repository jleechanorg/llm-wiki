# LLM Wiki Agents

This file provides agent-specific instructions for Claude Code and other AI agents working on this wiki.

## Insight Presentation

When presenting insights from wiki content:

1. **Verify novelty** — Check if concept already exists in:
   - User's known repos (ai_universe, worldarchitect.ai, jleechanclaw)
   - Existing slash commands (/4layer, /harness, etc.)
   - Recent merged PRs
2. **Flag uncertainty** — Say "you may already have this" if uncertain
3. **Don't present as novel** — Ideas user already built are not insights

## Wiki Quality Standards

- **Karpathy pattern compliance**: wiki/ subdir only, sources/entities/concepts
- **Entity ratio target**: >5%
- **Concept ratio target**: >5%
- **Index quality**: Curated summaries, not raw content
- **Frontmatter**: All pages require YAML frontmatter with type field
