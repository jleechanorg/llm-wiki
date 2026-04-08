# LLM Wiki (Fork)

This is a **fork** of [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (1,274 stars), modified to use a coding agent instead of direct API calls.

**Original**: A personal knowledge base that builds and maintains itself using LLMs  
**This Fork**: Uses Claude Code CLI via your preferred agent (default: **claudem** with MiniMax M2.5)

## Quick Start

```bash
cd ~/llm_wiki

# Ingest a document (uses claudem by default - MiniMax M2.5)
python3 ingest.py ~/some-file.md

# Query the wiki
python3 query.py "What does the wiki say about X?"

# Lint for health issues
python3 lint.py
```

## Agent Options

```bash
# Default: uses WIKI_AGENT env var (defaults to 'claudem')
python3 ingest.py file.md

# Explicit agents
python3 ingest.py file.md --agent=claude   # Claude Sonnet
python3 ingest.py file.md --agent=claudem  # MiniMax M2.5 (default)
python3 ingest.py file.md --agent=codex    # OpenAI Codex
python3 ingest.py --agent=cursor cursor   # Cursor

# AO (Agent Orchestrator) integration - uses AO workers
python3 ingest.py file.md --agent=ao
export WIKI_AGENT=ao
export AO_RUNTIME=antigravity  # antigravity, tmux, etc.
```

Set your default in `~/.bashrc`:
```bash
export WIKI_AGENT=claudem  # Use MiniMax (default)
export WIKI_AGENT=ao     # Use AO with workers
export AO_RUNTIME=antigravity  # AO runtime (antigravity, tmux)
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

- Claude Code CLI (`claude`) or other supported agent
- **For claudem**: MiniMax API key (`$MINIMAX_API_KEY`)
- No Anthropic API key needed when using coding agents

## Credits

- **Original**: [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (MIT License)
- **Pattern**: [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
