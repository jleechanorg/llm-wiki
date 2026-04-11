# Source File Inventory

This file tracks which source files exist vs which are referenced in wiki sources.

## Summary
- **Total source references**: 128
- **Files found**: ~10 (most paths are stale/moved)

## Sources in wiki/sources/ that reference missing files

### Files that EXIST (can be ingested):
- ~/AGENTS.md
- ~/.claude/scripts/secondo_campaign_analysis_iteration_005.md
- ~/repos/smartclaw/docs/STAGING_PIPELINE.md
- ~/repos/jleechanorg/worldarchitect.ai/docs/*.md (many files)

### Files that are MISSING (stale paths):
- .beads/BD_GUIDE.md (not in ~/.beads/)
- .beads/readme.md (EXISTS as README.md)
- repos/jleechanclaw/github_stats.md
- repos/worldarchitect-ai/.github/workflows/cost-analysis.md
- repos/worldarchitect.ai/docs/benchmark-genesis-vs-ralph.md
- repos/worldarchitect.ai/docs/ios_mcp_implementation_analysis.md
- projects/worktree_schema/schema_prompt_regression_test.md
- Downloads/campaigns/Iteration 007 Campaign.txt

## Action Items

1. **Create raw/ directory** with available source files
2. **Re-ingest from worldarchitect.ai/docs/** - this has the most files
3. **Track source origins** in future ingests
