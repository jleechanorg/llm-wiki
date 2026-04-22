# Investigation Recap: Skeptic Cron and CodeRabbit Stale Blocks (April 18, 2026)

## Summary
A deep-dive investigation into persistent Pull Request blockages in the `worldarchitect.ai` repository. We discovered that PRs #6356 and #6360 were stuck in a "stale" blockage state because `gh pr checks` incorrectly reports a "Green Gate: pass" simply because the GitHub Actions webhook returned 200, masking deep structural 7-green policy failures actively enforced by the `skeptic-cron.yml` loop.

## Key Technical Discoveries & Diagnostics
1. **The CodeRabbit Stale Trap:** 
   - CodeRabbit's `CHANGES_REQUESTED` GitHub constraint state does not clear automatically if the code is patched quietly. It must be explicitly re-approved using `@coderabbitai resolve` or a manual GitHub API approval review.
   - `skeptic-cron` strictly fails Gate 3 if the reviewDecision remains `CHANGES_REQUESTED`, regardless of whether `gh pr checks` presents green dots.
2. **Comment Resolution Blockade:** 
   - Gate 5 strictly counts unresolved inline GitHub review threads via the GraphQL API. Fixing the underlying code is insufficient; threads must be formally collapsed.
3. **The `gh pr checks` Illusion:** 
   - `CodeRabbit: pass` in `gh pr checks` does NOT mean the code was approved; it merely means the CodeRabbit CI webhook triggered successfully.
4. **Evidence Stringency:** 
   - The `skeptic-cron` Evidence bot (Gate 6) sweeps for explicit `gist.github.com` or terminal recording links in the PR body. Without them, PRs remain suspended indefinitely.

## Next Directions
- All agents should rely strictly on `skeptic-cron.yml` logs or `gh run view <id> --log` for authoritative PR mergeability, rather than `gh pr checks`.
- When mitigating CodeRabbit feedback, ensure the agent executes `gh pr comment <N> -b "@coderabbitai resolve"` to collapse threads and finalize the loop.
