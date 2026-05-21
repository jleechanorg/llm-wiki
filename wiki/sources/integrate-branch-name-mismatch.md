# Integrate Branch Name Mismatch

`integrate.sh` may report a different branch name than what git actually creates. Script reported `dev1778804652` but actual was `dev1778804655`.

## Lesson
Always verify with `git branch --show-current` after integrate.sh completes before running any branch-specific commands. Never trust the script's reported name.

## Related
- [[skeptic-cron-hermes-agent-deploy]]
