# Level-Up Centralization Learning 2026-04-17

Critical learning: centralization must be proven by behavioral equivalence and real integration evidence, not by design intent, grep gates, or similar function names.

The WorldArchitect.AI level-up PR line drifted after the v4 rewards-engine centralization work because agents treated the roadmap as proof that `world_logic.py` behavior could be replaced by `rewards_engine.py`. The replacement functions were not behaviorally equivalent. `rewards_engine.py` handled causal XP-threshold decisions, while `world_logic.py` still handled stateful modal recovery, stale flags, stuck completion, persisted-story projection, and planning-block injection.

Going forward, every level-up/rewards PR touching `world_logic.py`, `rewards_engine.py`, `llm_parser.py`, or `game_state.py` must state module ownership, document any `world_logic.py` exception as modal/state recovery, provide behavioral-equivalence proof before replacement/deletion claims, and run real-server real-LLM `testing_mcp` strict, stale-pending, and streaming tests before claiming all bugs are fixed.

This learning is separate from autor experiments. Autor-tagged/titled PRs are not source-of-truth inputs for the level-up bugfix disposition unless explicitly promoted by the human operator.
