# LLM Wiki (Fork)

This is a **fork** of [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (1,274 stars), modified to use a coding agent instead of direct API calls.

**Original**: A personal knowledge base that builds and maintains itself using LLMs  
**This Fork**: Uses Claude Code CLI (`claude -p`) instead of Anthropic API for ingestion, querying, and linting.

## Quick Start

```bash
cd ~/llm_wiki

# Ingest a document
python3 ingest.py ~/some-file.md

# Query the wiki
python3 query.py "What does the wiki say about X?"

# Lint for health issues
python3 lint.py
```

## Wiki Structure

```
llm_wiki/
├── wiki/
│   ├── index.md      # Catalog of all pages
│   ├── log.md       # Activity log
│   ├── overview.md  # Living synthesis
│   ├── sources/     # Ingested source pages
│   ├── entities/    # People, companies, projects
│   ├── concepts/    # Ideas, frameworks, methods
│   └── syntheses/   # Saved query answers
├── ingest.py        # Ingest sources via coding agent
├── query.py        # Query wiki via coding agent
├── lint.py         # Health check via coding agent
└── CLAUDE.md       # Schema for coding agent
```

## Requirements

- Claude Code CLI installed (`claude`)
- No Anthropic API key needed — uses your coding agent

## Credits

- **Original**: [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (MIT License)
- **Pattern**: [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
