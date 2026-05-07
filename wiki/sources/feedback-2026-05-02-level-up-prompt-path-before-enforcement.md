# Level-up prompt path before enforcement — 2026-05-02

PR 6748 organic level-up debugging showed the failing turn routed to `RewardsAgent`, not `LevelUpAgent`, and the prompt omitted `level_up_instruction.md`. Future level-up fixes must inspect raw selected-agent prompts before adding backend protection. The canonical actionable model signal is `target_level > current_level`; backend must not derive primary availability from XP thresholds. Enforcement is forbidden without explicit `ENFORCEMENT APPROVED`.

Source memory: `/Users/jleechan/.claude/projects/-Users-jleechan-worktree_level_super/memory/feedback_2026-05-02_level_up_prompt_path_before_enforcement.md`
Bead: `rev-sd96f`
PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6748
