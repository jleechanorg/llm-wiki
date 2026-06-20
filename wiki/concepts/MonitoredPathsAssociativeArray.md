---
title: "MonitoredPathsAssociativeArray"
type: concept
tags: [bash, data-structure, disk-magician, audit]
date: 2026-06-13
last_updated: 2026-06-13
---

# MonitoredPathsAssociativeArray

A bash `declare -A` associative array used in `disk_snapshot.sh` (discover
mode) and any consumer that needs the canonical "is this path tracked?"
answer. Keys are absolute paths (after `~` and `$HOME` expansion); values
are always `1`.

## Populating it correctly
Three sources must be merged to match what the snapshot measurement
actually tracks:

```bash
declare -A MONITORED_PATHS=()

# 1. Direct monitored_dirs
while IFS=$'\t' read -r raw_path; do
  path="${raw_path/#\~/$HOME}"
  path=$(eval echo "$path")
  MONITORED_PATHS["$path"]=1
done < <(python3 - "$CONFIG_FILE" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for item in data.get("monitored_dirs", []):
    print(item["path"])
PY
)

# 2. monitored_globs (shell-glob expanded)
while IFS=$'\t' read -r raw_pattern; do
  pattern="${raw_pattern/#\~/$HOME}"
  # shellcheck disable=SC2206
  expanded=( $(eval echo "$pattern") )
  for p in "${expanded[@]}"; do
    [[ -e "$p" ]] && MONITORED_PATHS["$p"]=1
  done
done < <(python3 - "$CONFIG_FILE" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for item in data.get("monitored_globs", []):
    print(item["pattern"])
PY
)

# 3. monitored_file_globs (same expansion)
while IFS=$'\t' read -r raw_pattern; do
  pattern="${raw_pattern/#\~/$HOME}"
  expanded=( $(eval echo "$pattern") )
  for p in "${expanded[@]}"; do
    [[ -e "$p" ]] && MONITORED_PATHS["$p"]=1
  done
done < <(python3 - "$CONFIG_FILE" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for item in data.get("monitored_file_globs", []):
    print(item["pattern"])
PY
)
```

## Lookup
```bash
if [[ -z "${MONITORED_PATHS[$dir]:-}" ]]; then
  echo "  UNTRACKED  $dir"
else
  echo "  tracked    $dir"
fi
```

## The bug pattern it prevents
If a downstream consumer (discover, audit candidate lister) only reads
`monitored_dirs[].path` and ignores the glob entries, it diverges from
the snapshot measurement. Glob-matched dirs are tracked by the snapshot
loop but reported as UNTRACKED by the consumer, inflating the
regrowth-prevention audit backlog with phantom gaps.

## See also
- [SubshellLocalBug](SubshellLocalBug.md) — the other bug that hid this one's impact
- [DiskMagicianDiscover](DiskMagicianDiscover.md) — the subcommand that uses this array
- [feedback-2026-06-13-disk-snapshot-discover-bugs](../sources/feedback-2026-06-13-disk-snapshot-discover-bugs.md) — original incident
