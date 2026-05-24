# 7-Green Proof Artifact

The binding proof that a PR has reached 7-green is a comment posted by
`github-actions[bot]` (via `skeptic-self-verify.yml`) containing both:
1. The literal text `VERDICT: PASS`
2. An HTML comment marker `<!-- skeptic-head-sha-<HEAD_SHA> -->` matching
   the current `headRefOid`

The comment enumerates 8 gates and shows PASS for each. `gh pr checks`
SUCCESS is necessary but not sufficient.

## Detection query

```bash
head=$(gh pr view <N> --json headRefOid --jq .headRefOid)
gh pr view <N> --json comments --jq \
  ".comments[] | select(.author.login == \"github-actions[bot]\") |
   select(.body | test(\"VERDICT: PASS\")) |
   select(.body | test(\"$head\")) | .html_url"
```

Empty output = 7-green NOT proven for this HEAD.

## Related
- [[pr7048-location-centralization-merged]]
- [[Green-Gate-Timing]]

## Source
- ~/.claude/skills/pr-green-definition.md
- ~/.claude/projects/-Users-jleechan-projects-worktree-location-centralize/memory/feedback_2026-05-24_7green_proof_artifact.md
