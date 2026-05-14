---
name: gemini-ttfc-token-floor-and-ablation-findings
description: Irreducible prompt token floor ~65K; system instructions are the dominant TTFC lever; story size barely matters; API variance dominates below 78K
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: c619c27c-76e4-426a-a962-a7f6a97f22d9
---

Gemini TTFC ablation (AB6-AB9) isolated each payload component:

| Test | Story | Instructions | prompt_tokens | Median TTFC |
|------|-------|-------------|--------------|------------|
| AB7 | 0 | ZERO | 64,922 | 17,399ms |
| AB6 | 0 | slim | 73,187 | 45,173ms* |
| AB8 | 6K | slim | 70,051 | 38,627ms* |
| AB9 | 24K | ZERO | ~65K | 34,273ms* |

*AB6/8/9 ran during high Gemini API latency; TTFC not comparable to AB4/7.

**Findings:**
1. **Irreducible floor = ~65K tokens** — game state/character/world data = 252KB even with ZERO story + ZERO instructions
2. **Story adds ~5K tokens** (0→24K chars = 65K→70K tokens) — negligible
3. **Slim instructions add ~1K system_tokens** vs ~200K for full — the dominant lever
4. **Within 65-78K tokens, Gemini API variance dominates**, not payload size differences
5. **The real win**: 255K→65K tokens (cached sys instructions) = 4x speedup; 78K→65K = within noise

**Full A/B ladder:**

| Arm | Median TTFC | vs Control |
|-----|------------|-----------|
| Control (full + code exec) | 64,070ms | 1.0x |
| Slim + 24K story + code exec ON | 21,924ms | 2.92x faster |
| Slim + 24K story + code exec OFF | 15,825ms | 4.05x faster |
| Slim + 24K story + conditional gate | 19,316ms | ~3.3x faster |
| ZERO story + ZERO instructions (floor) | 17,399ms | ~3.7x faster |

**Why:** The ~200K cached system instruction tokens are the dominant cost. Cutting those (813KB→5KB) = 4x speedup. Story is negligible. Below 78K tokens, Gemini API variance dominates — further token reduction won't improve TTFC.

**How to apply:** Production fix = summarize prompt files (quality-preserving, ~2-5KB each) + conditional code execution gate. Story cap not material. Further optimization below 65K requires reducing game state fields, which is not worth it.

**Evidence:**
- AB1-AB3: `/tmp/story_budget_ab{,2,3}/`
- AB4: `/tmp/story_budget_ab4/`
- AB5: `/tmp/story_budget_ab5/`
- Ablation: `/tmp/story_budget_ablation/ABLATION_REPORT.md`
- Branch: `feature-slim-system-instructions` in worktree_runner4
- Commits: `ab9117c97` (gate), `8b6b6aa51` (docs), `fb54e7552` (slim stubs)
