# SuperlightCommand

`/superlight <task>` — legacy thin local-GLM-5.2 router via the `claudeg` bash function (`~/.bashrc`). Same model identity the [[SuperpowersCloudBuild]] box uses, BUT **no remote execution, no plan.md, no hermeticity gate**. For one-liners where a full plan + handoff is overkill.

## NOT the box
`/superlight` runs locally via OpenRouter — it does NOT dispatch to [[SuperpowersCloudBuild]]. Affected by OpenRouter 402 credit exhaustion (returns 402 until the account is topped up). For real cloud dispatch use [[SuperCommand]] (`/super`).

## When to use
- Single-LLM-call task (write a function, explain a snippet).
- No spec/plan needed.
- When the Cloud Build box is overkill.

Do NOT use for multi-task features, evidence-gated work, or anything requiring the box's hermetic AGY runtime — use `/super` for those.
