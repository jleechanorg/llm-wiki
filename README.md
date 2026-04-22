# LLM Wiki — Personal Knowledge Base

Forked from [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) — a personal knowledge base that builds and maintains itself using LLMs.

## What This Wiki Covers

A multi-topic knowledge base built and maintained by LLM agents. Key areas:

### AI & Coding Agents
Coding agents (Voyager, SWE-Agent, OpenHands, Devin, Claude Code, Codex), benchmarks (SWE-bench, AgentBench, EvoEval, SWE-Shepherd), agent architectures (multi-agent orchestration, SOP encoding, Constitutional AI), self-improvement (self-reflection, PRMs, RL from feedback), and evaluation frameworks.

**25+ papers ingested (2022–2026):** Meta-Harness, Kimi k1.5, SWE-Shepherd, Agentic Verification, Shadows in Code, RefineRL, Mem²Evolve, FM-Agent, and more.

**Special content:**
- **Karpathy LLM Wiki gist** (full text + 30 comments) — `raw/gists/karpathy-llm-wiki-442a6bf.md`
- **Jeffrey Oracle** — Synthesis from 56K+ Claude Code messages + 1900+ GitHub commits
- **Auto-Research v3** — 18-cycle experiment testing SWE-bench, PRM, and Meta-Harness techniques
- **Agent Orchestrator** — 100+ PR entries documenting OpenClaw/Agent Orchestrator development

### TTRPG & Game Mechanics
Campaign world-building, character classes, spells, rules systems (D&D 5e), stat blocks, encounter design, loot systems, faction mechanics, player character logs, and narrative-driven game sessions. Multiple campaign worlds including BG3, Visenya, Nocturne, Astarion, and more.

### Engineering & Architecture
Python, TypeScript/React, APIs, databases (Firestore), GitOps (ArgoCD, Flux), stream governance (Kafka, Schema Registry), MCP servers, testing patterns (TDD, unit, e2e), authentication, observability, and CI/CD workflows.

### Philosophy & Governance
Constitutional AI, scalable oversight, data contracts, fail-closed validation, AI safety preparedness, and privacy.

### Product & Design
Architecture decision records, authentication patterns, UI systems (CSS), product taste frameworks, and user research.

### Personal Projects & Experiments
Beads-based memory tracking, Codex sessions, auto-research experiments, level-up game systems, and agent orchestration workflows.

---

## Wiki Structure

```
llm_wiki/
├── wiki/
│   ├── index.md              # Master catalog — all sections and pages
│   ├── log.md               # Activity log
│   ├── overview.md          # Living synthesis across all sources
│   ├── sources/             # ~7,585 sources (papers, PRs, campaigns, sessions, notes)
│   ├── entities/            # ~2,242 entities (people, companies, tools, TTRPG locations)
│   ├── concepts/            # ~1,637 concepts (AI patterns, TTRPG mechanics, engineering)
│   └── syntheses/           # Research findings and saved query answers
├── raw/
│   ├── arxiv-*              # 25 full-text arxiv papers (AI/coding agents)
│   └── gists/               # Gist archives (Karpathy LLM Wiki + comments)
├── ingest.py / query.py / lint.py  # LLM agent interface scripts
└── CLAUDE.md                 # Schema for coding agent
```

**Content overview:**
- **Sources:** ~4,319 PRs · ~2,000 campaigns · ~1,000 other (beads, design docs, research) · 178 level-up/game files · 37 papers · 35 research/design docs · 15 Codex sessions
- **Entities:** ~2,100 TTRPG locations/characters · 51 people · 25 tech stack · 22 AI agents · 16 AI companies
- **Concepts:** ~204 testing · ~77 python · ~68 game-mechanics · ~68 validation · ~58 API · ~53 architecture · ~50 llm · ~40 security · + more

---

## Quick Start

```bash
cd ~/llm_wiki

# Ingest a document (uses WIKI_AGENT env var, defaults to claudem/MiniMax M2.5)
python3 ingest.py ~/some-file.md

# Query the wiki
python3 query.py "What does the wiki say about X?"

# Lint for health issues
python3 lint.py
```

### Agent Options

```bash
python3 ingest.py file.md --agent=claude    # Claude Sonnet
python3 ingest.py file.md --agent=claudem   # MiniMax M2.5 (default)
python3 ingest.py file.md --agent=codex    # OpenAI Codex
python3 ingest.py file.md --agent=ao       # Agent Orchestrator workers
```

Set your default in `~/.bashrc`:
```bash
export WIKI_AGENT=claudem  # Default (MiniMax M2.5)
export WIKI_AGENT=ao       # Use AO with workers
export AO_RUNTIME=antigravity  # AO runtime (antigravity, tmux)
```

---

## Ingested AI/Coding Agent Papers (2022–2026)

| Paper | arxiv ID | Key Contribution |
|-------|----------|-----------------|
| Meta-Harness | 2603.28052 | Outer-loop harness optimization; +27 SWE-bench |
| Coding Agents Over-Mocked Tests | 2602.00409 | Agents prefer mocked tests over real ones |
| Agentic Much | 2601.18341 | 22-28% coding agent adoption on GitHub |
| Kimi k1.5 | 2501.12599 | RL scaling for reasoning; 77.5 AIME, matches o1 |
| Agentic Verification | 2511.17330 | AutoRocq: LLM + Coq theorem proving |
| Shadows in Code | 2511.18467 | Multi-agent security attacks; 93% attack rate |
| BOAD | 2512.23631 | Hierarchical agent discovery via bandit opt |
| Vibe Coding Safe | 2512.03262 | Only 10.5% of vibe-coded apps are secure |
| From Correctness to Collaboration | 2512.23844 | CA benchmark for coding agents |
| GitHub Issue Ready for Copilot | 2512.21426 | 32 criteria for copilot-ready issues |
| Reformulate Retrieve Localize | 2512.07022 | Bug localization via query reformulation |
| One Tool Is Enough | 2512.20957 | RepoNavigator RL agent; 7B > 14B |
| SWE-Shepherd | — | PRMs for step-level code agent supervision |
| RefineRL | — | Self-refinement RL for competitive programming |
| ThinkTwice | — | Joint GRPO reasoning + self-refinement |
| Agent Mentor | — | Execution monitoring for agent corrective instructions |
| Mem²Evolve | — | Self-evolving agents via co-evolution |
| CodeComp | — | KV cache compression via code property graphs |
| E3-TIR | — | Tool-integrated reasoning experience exploitation |
| FM-Agent | — | LLM-based Hoare-style formal methods |
| AdverMCTS | — | Adversarial MCTS for pseudo-correctness detection |
| Self-Debias | — | Self-correcting debiasing via trajectory optimization |
| Voyager | 2305.16291 | Lifelong learning agent in Minecraft |
| SWE-Agent | 2308.03688 | Agent Computer Interface for autonomous software engineering |
| OpenHands | 2412.21130 | Open platform for reproducible coding agent evaluation |

---

## Potentially Missing Papers (not yet ingested)

Notable papers that may not yet be in the wiki:

**Frontier Models (2025–2026):**
- o3 / o4-mini (OpenAI reasoning models)
- Claude 4 (Sonnet/Opus) — Anthropic's 2025 coding improvements
- Gemini 2.5 — Google's coding agent advances

**Coding Agents:**
- Devin 2.0 — Cognition's updated software engineer
- Aider v0.5+ — New coding agent benchmarks
- BOLT — DeepMind's coding agent (if published)

**Benchmarks & Evaluation:**
- RE-Bench — Realistic engineering benchmark
- CRUXEval-II / HumanEval-2 — Next-gen coding evals
- SWE-bench Lite / Full updates

**Agent Safety & Tool Use:**
- TrustKit — Tool use safety for agents
- TAROT — Test-aware agent routing

If you have paper URLs or PDFs, drop them in `~/llm_wiki/raw/` and run `python3 ingest.py`.

---

## Credits

- **Original:** [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) (MIT License)
- **Pattern:** [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
