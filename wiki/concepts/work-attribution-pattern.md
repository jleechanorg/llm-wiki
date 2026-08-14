---
title: "WorkAttributionPattern"
type: concept
tags: [claude-code, token-burn, attribution, jsonl, worktree]
last_updated: 2026-08-14
---

# Work Attribution Pattern

When asked "what work used up my tokens?", the right answer requires mapping **JSONL files → worktree → PR → git commits**. The wrong answer is a vague list of slash commands.

## Pattern

```python
import os, glob, json, re
from collections import defaultdict

worktree_data = defaultdict(lambda: {
    'files': [], 'first_user_messages': [], 'pr_refs': Counter(),
    'size_bytes': 0,
})

for path in glob.glob('/Users/jleechan/.claude/projects/*/*.jsonl'):
    mtime = os.path.getmtime(path)
    if mtime < cutoff: continue
    proj_dir = os.path.basename(os.path.dirname(path))
    # Extract worktree from path
    m = re.search(r'claude-worktrees-([^/]+)|worktree-([^/]+)|worktree_([^/]+)', proj_dir)
    wt = next(g for g in m.groups() if g) if m else proj_dir
    
    worktree_data[wt]['files'].append(path)
    worktree_data[wt]['size_bytes'] += os.path.getsize(path)
    
    # Extract first user message + PR refs
    with open(path, 'r', errors='ignore') as f:
        for i, line in enumerate(f):
            if i > 30: break
            try:
                obj = json.loads(line)
                if obj.get('type') == 'user' and not worktree_data[wt]['first_user_messages']:
                    # ...extract text
                for pr in re.findall(r'#(\d{3,5})', line):
                    worktree_data[wt]['pr_refs'][pr] += 1
            except: pass

# For each worktree, run git log to get actual commits
for wt, data in sorted(worktree_data.items(), key=lambda x: -x[1]['size_bytes'])[:25]:
    wt_dir = worktree_meta.get(wt)
    if wt_dir and os.path.exists(wt_dir):
        commits = subprocess.check_output(
            ['git', '-C', wt_dir, 'log', '--since=7 days ago', '--oneline'],
            text=True
        )
        # ... present
```

## Output format

Group by worktree, present:

```
### <worktree-name>
  Size: X.X MB across N JSONLs
  PRs: #1234, #5678, ...
  First task: <first user message snippet>
  Commits:
    <sha> <commit subject>
    ...
```

## Why work attribution FIRST, cost SECOND

Cost without work attribution is uninterpretable. The user needs to know what they actually spent tokens on, not just how much they spent.

## Lesson

The user had to push back multiple times when given vague answers. Each pushback was a hint toward this specific pattern. Trust user pushback as data, not noise.

## Related

- [[feedback-2026-08-12-token-burn-investigation-learnings]]
- [[CmuxResumeWatchdogLlmRemoval]] — the dominant token source found via this pattern