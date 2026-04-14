# Taste Learning Loop

Whenever I manually reject, heavily edit, or comment on a PR:

1. **Extract my feedback** — Pull your comment + the original PR description/diff
2. **Add to product-taste/good-bad-examples.md** — Label as Good or Bad Example with your reasoning
3. **Update product-taste/taste-rubric.md** — If new principles emerge from the feedback, add them
4. **Create a bead** — Record the learning event with the feedback and outcome
5. **Auto-incorporation** — [[ProductJudge]] will now reference the updated wiki on future PRs

This loop turns every correction you make into permanent institutional knowledge.

## Trigger Conditions

- You manually reject a PR verdict
- You heavily edit generated code before accepting
- You leave substantive comments explaining *why* something was wrong beyond technical accuracy
- You override [[ProductJudge]]'s verdict with your own reasoning

## What to Record

For each learning event, record:
- The original PR / generated code
- Your feedback (exact words if possible)
- Why the generated code didn't match your taste
- What principle from [[ProductPrinciples]] was violated (or what new principle emerged)

## Integration

- Reads from [[ProductJudge]] verdicts (to detect when you overrule the agent)
- Updates [[ProductTasteLayer]] wiki pages (good-bad-examples.md, taste-rubric.md)
- Creates beads for each learning event
- [[ProductJudge]] consumes the updated wiki for future verdicts

## Tags

#agent-harness #product-judgement #llm-wiki #self-improvement
