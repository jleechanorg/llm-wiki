# Auto-Research v3: Research-Grade Experiment Design

## Hypothesis

**H1**: Combined technique (Meta-Harness + ExtendedThinking + SWE-bench) outperforms any single technique.
**H2**: ExtendedThinking outperforms SelfRefine on complex/architectural PRs.
**H3**: Test-first discipline improves Type Safety more than other dimensions.
**H4**: Meta-Harness context optimization is the highest-leverage technique.
**H5**: Technique effectiveness is PR-size dependent (small vs medium vs complex).

## Methodology

### Population
- worldarchitect.ai PRs from 2025-2026 (n=50+)
- Stratified sampling: 15 small, 15 medium, 15 complex
- Dimensions: bug-fix, feature, refactor, test

### Techniques (5 agents, 3 runs each)
| Technique | Description | Expected Delta |
|-----------|-------------|---------------|
| ExtendedThinking | Reasoning prefix before code | +20-25 |
| SelfRefine | 3-iteration critique-revise | +15-18 |
| SWE-bench | Test-first → fix → verify | +22-25 |
| Meta-Harness | Context + prompt optimization | +25-30 |
| **COMBINED** | All three together | ??? |

### Scoring
6-dim rubric against canonical patterns (FastAPI, Requests, TanStack):
- Naming (15%)
- Error Handling (20%)
- Type Safety (20%)
- Architecture (20%)
- Test Coverage (15%)
- Documentation (10%)

### Statistical Analysis
- ANOVA across techniques
- Pairwise t-tests (Bonferroni corrected)
- 95% confidence intervals
- Effect size (Cohen's d)

## PR Selection (Stratified)

### Small PRs (1-2 files, <50 lines)
1. f3d94b4de - plain XP increase RuntimeError
2. d79663356 - CI-aware schema prompt perf
3. 250fa73fd - test updater precedence
4. 584eb9f77 - skip character creation modal
5. 5e721bc2f - remove dead rewards_corrections
6. 7e3fa3509 - h264-safe video scaling
7. 0a95693cb - 3-Generation Power Lineage
8. 2b7d1779c - video evidence enforcement
9. 3eb9d07ea - propagate WORLDTOOLS_PROXY_MODE
10. 3254264b4 - detect Think Mode actions
11. 5abd09b62 - move debug_info emission
12. 672e22b62 - mock LLM Think Mode
13. 95afb68a8 - video enforcement opt-out
14. c3d7802ae - add video deps allowed imports
15. fe57a5471 - remove duplicate import block

### Medium PRs (3-5 files, 50-200 lines)
1. 65de91a6b - ProxyFix rate-limit regression
2. 20c08dbf2 - level-up 3 production bugs
3. 53cf675e1 - generic rewards synthesis
4. bccd07d56 - remove rewards followup LLM call
5. e86d25be0 - structured GCP logging
6. 30c21c200 - asyncio ContextVar propagation
7. 5b2b98bc7 - coalesce world_events
8. 931c2e348 - reduce e2e timeout
9. 54f84c2e0 - wire tmux video into MCPTestBase
10. 51ac668c4 - 3-Generation Power Lineage modules
11. 521a0a097 - address CodeRabbit review comments
12. 0a1eaf8d6 - match actual metadata updater string
13. 6e5ba3f35 - centralize level/XP architecture
14. bf42d2e59 - video evidence frame extraction
15. 75e49304c - check postcondition after discrepancy

### Complex PRs (5+ files, 200+ lines)
1. #6233 - LayerUp architecture refactor
2. #6235 - evidence rule CR prohibition
3. #6214 - remove rewards followup LLM call
4. #6127 - directory tests unblocked
5. #6126 - ProxyFix rate-limit regression
6. #6218 - GCP logging rewards_box
7. #6222 - video recording + level-up injection
8. #6212 - debug_info emission
9. #6223 - MockLLM Think Mode
10. #6226 - world_events coalesce
11. #6228 - 3-Generation Power Lineage
12. #6230 - e2e timeout reduction
13. #6231 - mock-services mode propagation
14. #6224 - WORLDTOOLS_PROXY_MODE propagation
15. #6156 - repro copy command

## Output

1. Raw data: `wiki/syntheses/auto-research-v3-raw-data.md`
2. Statistical analysis: `wiki/syntheses/auto-research-v3-stats.md`
3. Findings: `wiki/syntheses/auto-research-v3-findings.md`
4. Paper draft: `wiki/syntheses/auto-research-v3-paper.md`

## Agents

5 parallel agents, each testing one technique on 15 PRs:
- agent-extended-thinking: ExtendedThinking
- agent-selfrefine: SelfRefine
- agent-swebench: SWE-bench Harness
- agent-metaharness: Meta-Harness
- agent-combined: All three combined

Each agent writes to: `wiki/syntheses/technique_<name>_v3_full.md`
