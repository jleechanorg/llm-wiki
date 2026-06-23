# Gemini Implicit Cache Verification & Multi-Agent Context

A prior claim stated RAG broke the implicit cache on every turn. BigQuery forensics corrected this: 67% of pre-fix turns actually had cache hits, but a logging bug (fixed in PR #7821) kept the typed `cached_tokens` column NULL (storing it in `extra_json` instead). Furthermore, system instructions differ by agent class (`REQUIRED_PROMPT_ORDER`).

## RAG Caching Guidelines
1. **Agent Context:** System instructions vary across agents (e.g., StoryModeAgent, CharacterCreationAgent, PlanningAgent). Switching agents naturally causes cache misses.
2. **Consecutive Turns:** Ensure consecutive turns of the same agent preserve the static prefix.
3. **Dynamic Elements:** Keep dynamic variables and RAG retrieved chunks at the end of the prompt tail.
