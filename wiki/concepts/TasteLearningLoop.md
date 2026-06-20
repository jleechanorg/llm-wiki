---
title: "TasteLearningLoop"
type: concept
tags: [agent-harness, product-judgement, llm-wiki, self-improvement]
sources: [auto-product-master-system]
last_updated: 2026-04-14
---

## Definition

A self-improving feedback loop that converts every manual correction you make on a PR into permanent institutional knowledge. Whenever you reject, heavily edit, or comment on a PR, the loop extracts your feedback, updates the [ProductTasteLayer](ProductTasteLayer.md) wiki, and creates a bead. Future [ProductJudge](ProductJudge.md) verdicts automatically use the updated wiki.

## How It Works

Whenever you manually reject, heavily edit, or comment on a PR:

1. **Extract feedback** — Pull your comment + the original PR description/diff
2. **Add to good-bad-examples.md** — Label as Good or Bad Example with your reasoning
3. **Update taste-rubric.md** — If new principles emerge from the feedback, add them
4. **Create a bead** — Record the learning event with the feedback and outcome
5. **Auto-incorporation** — [ProductJudge](ProductJudge.md) will now reference the updated wiki on future PRs

## Key Design Choices

- **Event-driven**: Triggers on manual human correction, not on automated checks
- **Two-file update**: good-bad-examples.md (concrete instances) + taste-rubric.md (abstract principles)
- **Bead tracking**: Every learning event is a bead for traceability
- **Passive accumulation**: The wiki grows without prompting — every correction automatically feeds it
- **Closed loop**: Corrected verdicts → updated wiki → better future verdicts

## Integration Points

- Reads from [ProductJudge](ProductJudge.md) verdicts (to detect when you overrule the agent)
- Updates [ProductTasteLayer](ProductTasteLayer.md) wiki pages (good-bad-examples.md, taste-rubric.md)
- Creates beads for each learning event
- [ProductJudge](ProductJudge.md) consumes the updated wiki for future verdicts

## Related Concepts

- [ProductJudge](ProductJudge.md) — the oracle that consumes the taste wiki
- [ProductTasteLayer](ProductTasteLayer.md) — the full product taste subsystem
- [AutoResearchLoop](AutoResearchLoop.md) — the research loop that ProductJudge evaluates within
- [[BeadsTracking]] — the bead system used to record learning events
