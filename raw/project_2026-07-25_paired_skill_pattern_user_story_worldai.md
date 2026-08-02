---
name: paired-skill-pattern-user-story-worldai
description: "general practice lives in the user-scope skill, product specifics live in a repo-scope companion skill that requires the general one — neither is sufficient alone; routing rule is \"general goes up, product-specific stays down\""
metadata: 
  node_type: memory
  type: project
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:45:52.432Z
---

Created `.claude/skills/user-story-worldai/SKILL.md` in the worldarchitect.ai repo (commit `68ce7dc85bcfacad1cb43ab2db4b3b9b3ff5ba9a`, verified present) holding product specifics: docset paths, which evidence source settles which claim, the four long campaigns and how to mine them, the local-server capture recipe (and why capturing against a deployment previously locked the repo owner out — see [[project_2026-07-25_waitlist_fabricated_deny_and_ip_ratelimit_lockout]]), the traps that produced false claims, and a table of already-refuted claims so nobody re-asserts them.

Meanwhile `~/.claude/skills/user-story/SKILL.md` keeps only the general law: rewritability bar, story form, zero-code ban, evidence-class matching.

**Bidirectional requirement, not just a link:** the user-scope skill tells readers to look for a repo companion first; the repo-scope skill opens by requiring the user-scope skill. Each is incomplete without the other — general law without product traps re-derives mistakes already made; product traps without general law lose the rewritability/evidence-class discipline.

**Routing rule:** general practice goes up (user scope), product specifics stay down (repo scope). Putting repo paths and one product's traps into the user-global file is exactly how that file rots into unusable noise for other repos — this pattern is the fix. Reusable whenever a skill accumulates both a general principle and a single project's operational detail: split along this line rather than letting one grow to cover both.
