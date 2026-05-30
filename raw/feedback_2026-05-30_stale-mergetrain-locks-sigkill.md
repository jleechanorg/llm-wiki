---
name: stale-mergetrain-locks-sigkill
description: "SIGKILL'd Claude Code sessions leave stale merge_train domain locks that block all Edit/Write tool calls in the next session"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-h37al
  originSessionId: 275ec345-f729-4719-a137-4169f79d03ba
---

## Stale merge_train locks after SIGKILL

When Claude Code is killed with SIGKILL (macOS OOM or forced kill), any
`merge_train` domain locks it held are never released. In the next session,
all `Edit` and `Write` tool calls to locked files are denied by the
`domain-lock-pre-tool.sh` PreToolUse hook with:

```
merge_train: REFUSED — HELD: mvp-frontend by PR#958856 agent=claude-code branch=main
```

The `PR#958856` is a fake/session-level PR number used when the session had no
real open PR at the time of lock acquisition (e.g. working on `main` directly).

**Why:** The `domain-lock-pre-tool.sh` stale-GC runs on each blocked call but
the GC only releases locks whose GitHub PR is closed/merged. PR#958856 doesn't
exist on GitHub so `gh pr view 958856` fails → GC skips it → lock persists forever.

**Fix — manual release:**
```bash
for domain in mvp-core mvp-frontend mvp-testing; do
  python3 -c "import sys; sys.argv=['domain_lock','--registry','file_domains.yaml','release','--domain','$domain','--pr','958856']; from merge_train.domain_lock import main; main()" 2>&1 | tail -2
done
```

Replace `958856` with the actual fake PR number shown in the error. To list
all held locks first:
```bash
python3 -c "import sys; sys.argv=['domain_lock','--registry','file_domains.yaml','list','--json']; from merge_train.domain_lock import main; main()" | python3 -m json.tool
```

**How to apply:** Any time Edit/Write calls are denied with `merge_train: REFUSED`
after a session crash or restart, run the release loop above. The stale PR number
will show in the error message.

**References:**
- Session: 2026-05-30, branch `fix/custom-campaign-default-world-guard`
- Stale locks: PR#958856, domains: mvp-core (×3), mvp-frontend (×1), mvp-testing (×1)
- Resolved by manually releasing all 5 locks
