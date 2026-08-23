# Command Research Methodology & Top 20 Empirical Audit (2026-08-23)

## Summary
Empirical data mining across 128,756 session turns in Hermes SQLite (`~/.hermes/state.db`), Claude Code JSONL logs (`~/.claude/projects/`), and Codex SQLite (`~/.codex/state_5.sqlite`) to determine genuine slash command and skill usage across human and agentic workflows.

## The Anti-Noise Discovery
Raw substring search across session logs fails with 10,000–180,000 false positives because Claude Code injects the entire tool/skill catalog into system reminders on every tool turn. Accurate measurement requires:
1. Exact prompt-start token matching: `(?:^|\s)/cmd` or canonical Claude Code tag `<command-name>/cmd</command-name>`.
2. Filtering out system injections (`<skill_listing>`, `<EXTREMELY_IMPORTANT>`, `"Base directory for this skill:"`).
3. Excluding filesystem path prefixes (`/Users`, `/tmp`, `/dev`, `/api`, `/src`, `/tests`, `/var`, `/home`, etc.) and file suffixes (`.py`, `.md`, `.ts`, `.sh`, `.json`).

## Dual Taxonomy Breakdown
- **Human-Typed**: Directly initiated by the operator (Slack DMs, interactive terminal prompts with `promptSource: "typed"` or root user prompt turns).
- **Agentic / Subagent**: Automated delegation (`source: "subagent"`), swarm fan-out lanes, sidechain sessions (`isSidechain: true`), autonomous loops, or Stop-hook verifications.

### Top 20 Human-Typed Commands
1. `/advice` (8,145 human / 20,226 total)
2. `/green` (4,090 human / 17,715 total)
3. `/repro` (2,954 human / 13,774 total)
4. `/research` (2,690 human / 4,038 total — 66.7% human, highest human concentration)
5. `/ms` (2,586 human / 8,769 total)
6. `/history` (2,320 human / 6,761 total)
7. `/er` (2,215 human / 20,488 total)
8. `/linux` (700 human / 3,068 total)
9. `/f` (676 human / 6,115 total)
10. `/ready` (594 human / 3,623 total)
11. `/es` (555 human / 20,030 total)
12. `/web-advice` (457 human / 3,231 total)
13. `/browser` (366 human / 1,705 total)
14. `/skillify` (258 human / 2,923 total)
15. `/document-standards` (153 human / 309 total)
16. `/browserclaw` (150 human / 737 total)
17. `/auto` (144 human / 2,069 total)
18. `/wiki-search` (142 human / 386 total)
19. `/smoke` (135 human / 8,417 total)
20. `/roadmap` (135 human / 3,339 total)

### Top 20 Agentic Commands
1. `/es` (19,475 agent / 20,030 total — 97.2% agentic)
2. `/er` (18,273 agent / 20,488 total — 89.2% agentic)
3. `/green` (13,625 agent / 17,715 total)
4. `/advice` (12,081 agent / 20,226 total)
5. `/repro` (10,820 agent / 13,774 total)
6. `/smoke` (8,282 agent / 8,417 total — 98.4% agentic)
7. `/execute` (7,136 agent / 7,136 total — 100% agentic)
8. `/copilot` (6,191 agent / 6,231 total)
9. `/ms` (6,183 agent / 8,769 total)
10. `/fixpr` (5,695 agent / 5,716 total)
11. `/f` (5,439 agent / 6,115 total)
12. `/nextsteps` (4,538 agent / 4,588 total)
13. `/history` (4,441 agent / 6,761 total)
14. `/harness` (3,898 agent / 4,015 total)
15. `/learn` (3,367 agent / 3,451 total)
16. `/roadmap` (3,204 agent / 3,339 total)
17. `/ready` (3,029 agent / 3,623 total)
18. `/web-advice` (2,774 agent / 3,231 total)
19. `/skillify` (2,665 agent / 2,923 total)
20. `/end2end-testing` (2,555 agent / 2,577 total)

## Unified Canonical Tooling
Unified scanner implemented at `~/.claude/skills/command-research/scripts/count_command_usage_unified.py` and wrapped with `/command-research`.
