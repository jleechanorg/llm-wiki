---
name: gh-pr-create-two-remote-resolution-bug
description: "gh pr create / gh repo set-default fail with 'Could not resolve to a Repository' when a repo has two remotes (origin + a fork remote); create the PR via the REST pulls endpoint instead"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c594d4f0-a942-4271-85f6-5407a3c1d6e6
---

In `~/.hermes` (and any clone with **two remotes** — `origin`=`jleechanorg/jleechanclaw` plus `hermes-agent`=`jleechanorg/hermes-agent`), `gh pr create` fails persistently with:

```
GraphQL: Could not resolve to a Repository with the name 'jleechanorg/jleechanclaw'. (repository)
```

and `gh repo set-default jleechanorg/jleechanclaw` rejects the slug with *"does not correspond to any git remotes"* — even though the URL is literally `https://github.com/jleechanorg/jleechanclaw.git`. This is a **gh-CLI client-side bug** in its batched base/head repo resolution across the fork chain, NOT a permissions or auth problem: `gh api repos/<owner>/<repo>` (REST GET), `gh api graphql -f query='{repository(owner,name){id viewerCanAdminister}}'`, and `git push` all work fine with the same keyring token (`jleechan2015`, `admin:true`/`push:true`).

**Workaround — create the PR via the REST pulls endpoint (bypasses gh's remote resolution entirely):**

```bash
gh api --method POST repos/jleechanorg/jleechanclaw/pulls \
  -f title="..." -f head="<branch>" -f base="main" -F body=@/tmp/body.md \
  --jq '"PR #" + (.number|tostring) + "  " + .html_url'
```

`-F body=@file` reads the body from a file. To PATCH title/body later: `gh api --method PATCH repos/<o>/<r>/pulls/<N> -f title=... -F body=@file`.

**Two adjacent gotchas hit the same session (2026-06-12, PR [#612](https://github.com/jleechanorg/jleechanclaw/pull/612) landing the Agnt-F SOUL mapping):**
1. **rtk shell wrapper mangles `cat > file <<'EOF'` heredocs and `wc -c < file`** — the heredoc content actually wrote, but `wc -c < file` reported `0`. Don't trust shell heredoc/redirect for body files under rtk; **write body files with the Write tool**, and verify with `Read`, not `wc`.
2. **Transient GitHub write-API 404 incident** — `POST/PATCH .../pulls` intermittently returned `{"message":"Not Found","status":"404"}` while GETs succeeded; a `404` response can still mutate server-side (a probe POST that "failed" had actually created the PR). Always **list open PRs by head branch to get true state** before retrying, then retry the write with backoff (it cleared within ~minutes).

Related: [[hermes-soul-symlink-and-autocommit-branch-hygiene]], [[coderabbit-dismissed-stuck-admin-override]].
