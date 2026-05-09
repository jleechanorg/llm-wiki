# Canonicalize LW cooldown stripping to authoritative field set

- **Date**: 2026-05-08
- **Severity**: maintainability risk (low runtime risk)
- **Bead**: rev-247t8
- **Summary**: Avoid duplicate hardcoded lists of living-world cooldown fields in `mvp_site/world_logic.py`.
- **Fix**: both cooldown strip loops now iterate `firestore_service._AUTHORITATIVE_LIVING_WORLD_FIELDS`.
- **Context**: only one code path had the hardcoded tuple; another call site (`mvp_site/llm_parser.py`) already consumed the canonical set from `firestore_service`.
- **Outcome**: reduces schema drift risk and keeps strip/restore behavior aligned when canonical LW fields evolve.

## References

- `/Users/jleechan/projects/worktree_worker4/mvp_site/world_logic.py`
- `/Users/jleechan/projects/worktree_worker4/mvp_site/firestore_service.py`
- `/Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree-worker4/memory/project_2026-05-08_world_logic_lw_authoritative_canonical_fields.md`
