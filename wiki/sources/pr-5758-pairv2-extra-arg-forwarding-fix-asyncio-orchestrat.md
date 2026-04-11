---
title: "PR #5758: pairv2: extra arg forwarding fix + asyncio orchestration migration design"
type: source
tags: []
date: 2026-02-25
source_file: raw/prs-worldarchitect-ai/pr-5758.md
sources: []
last_updated: 2026-02-25
---

## Summary
- Fix `.claude/pair/benchmark_pair_executors.py` so forwarded `--coder-extra-arg/--verifier-extra-arg` values are emitted as `--flag=value`
- Preserves dash-prefixed tokens (e.g. `--search`, `-m`) instead of triggering argparse "expected one argument"
- Add regression coverage in `.claude/pair/tests/test_pair_v2_and_benchmark.py` for dash-prefixed argument forwarding
- Update `testing_llm/pair/sdui_blog_tdd.md` with spec-only XL exit criteria aligned to evidence standards
- Add `no_tmux` paramet

## Metadata
- **PR**: #5758
- **Merged**: 2026-02-25
- **Author**: jleechan2015
- **Stats**: +12595/-8024 in 43 files
- **Labels**: none

## Connections
