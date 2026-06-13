# Don't second-guess working bashrc wrappers on a TUI error (2026-06-13)

I broke `claudem` by changing `MiniMax-M3` → `MiniMax-M2.5` (then M2.7) on the strength of a TUI "model may not exist" error. The error was the **Claude Max session-limit** (resets ~3:40pm; I was testing 3:36–3:38pm), NOT model validation. M3 is real (verified at `https://api.minimax.io/v1/models`). Same error fired for `claudew` with `GLM-5.1` (different backend) — proving the rejection is not name-specific.

**Fixes applied (2026-06-13, after /harness):**
- `claudem` restored byte-identical from `/tmp/bashrc.bak.1781389720` (uses M3)
- `claudew` function deleted from `~/.bashrc` (per user request)
- `~/.claude/CLAUDE.md`: added "Bashrc wrappers are user-owned config" rule under Method fidelity + Config fidelity
- `~/.claude/skills/_archive/minimax-cli-fix.md`: ⚠️ STALE banner added at top
- Memory entry `feedback_2026-06-13_dont_second_guess_working_setup.md` created and indexed
- Bead `jleechan-bashrc-claudem-2026-06-13` (closed) in `~/.beads/issues.jsonl`

**Proper forward path:** use the AO `agent-minimax` plugin (`packages/plugins/agent-minimax/src/index.ts`) via `ao spawn --agent minimax "<task>"`. The bashrc `claudem` is a quick interactive alias; the plugin is the durable, tested path.

See `~/llm_wiki/raw/feedback_2026-06-13_dont_second_guess_working_setup.md` for the full memory file.
