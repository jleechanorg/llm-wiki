# Stale merge_train Locks After SIGKILL

**Date**: 2026-05-30
**Type**: feedback / operational procedure
**Bead**: rev-h37al
**PR context**: worldarchitect.ai PR [#7170](https://github.com/jleechanorg/worldarchitect.ai/pull/7170)

## Problem

When Claude Code is killed with SIGKILL (OOM or forced kill), `merge_train` domain
locks it held are never released. The next session's Edit/Write calls are blocked:

```
merge_train: REFUSED — HELD: mvp-frontend by PR#958856 agent=claude-code branch=main
```

`PR#958856` is a fake/session-level number used when no real PR was open. The stale-GC
in `domain-lock-pre-tool.sh` tries `gh pr view 958856` → fails → skips GC → lock persists.

## Fix

```bash
# List all locks to find fake PR numbers
python3 -c "import sys; sys.argv=['domain_lock','--registry','file_domains.yaml','list','--json']; \
  from merge_train.domain_lock import main; main()" | python3 -m json.tool

# Release all locks for the fake PR (replace 958856 with actual number)
for domain in mvp-core mvp-frontend mvp-testing; do
  python3 -c "import sys; sys.argv=['domain_lock','--registry','file_domains.yaml','release',\
    '--domain','$domain','--pr','958856']; from merge_train.domain_lock import main; main()" 2>&1 | tail -2
done
```

## Related concepts

- [[MergeTrainDomainLock]]
- [[StaleStateRecovery]]
