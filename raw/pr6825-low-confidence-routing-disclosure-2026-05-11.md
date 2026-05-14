# PR 6825 Low-Confidence Routing Disclosure — 2026-05-11

Context: PR #6825 evidence review found a Kira/Alexiel prompt routed to `FactionManagementAgent` at weak classifier confidence (`0.663`) even though the user was asking an NPC for advice.

Decision:
- Do not fix faction routing inside PR #6825 unless the 20-turn memory proof cannot pass without it.
- Treat the routing issue as a separate follow-up PR by default.
- Prefer disclosure-first routing hardening: expose top-N classifier scores, margin, and context influence to the selected agent prompt/debug metadata.
- Do not suppress classifier context by heuristic unless evidence shows disclosure is insufficient.
- Keep the fix ZFC-clean: no keyword routing, no regex intent detection, no second router model.

PR #6825 closeout remains focused on:
- same-head real smoke cleanup,
- exactly 20 natural Alexiel evidence turns,
- real server/LLM traces,
- missing-middle fact-card matrix,
- artifact-true PR description.
