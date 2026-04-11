# WorldArchitect Insights
*3 non-obvious findings for Jeffrey Lee-Chan*

---

## Insight 1: The PR numbering gap reveals a hidden second development workstream — and a looming merge conflict crisis

The deployment log for 2026-04-07 shows five PRs in a 57-minute window. Four of them (#6022, #6026, #6108, #6109) occupy a tight sequential range. But the fifth — PR #6122 — is **14 numbers ahead** of the last infrastructure PR (#6109), and was deployed *second-to-last*, immediately before the runner fix.

This is not just a quirk of ordering. The jump from #6109 to #6122 means **at least 12 PRs were merged between those two deployments** that are not represented in the deployment email data (or were opened in parallel and merged out of order). Given that #6026 and #6108 are also tagged as AI-generated (Claude Code and Codex Cloud respectively), the most likely explanation is that multiple AI agents — or multiple human/AI task streams — are opening PRs simultaneously against `main`, and they are largely invisible to each other.

The practical consequence: PR #6122 (`feat(prototype): simplify onboarding to 2-step flow`) touches `CampaignWizard` frontend logic, while PRs #6022 and #6108 touch `mvp_site/main.py` backend auth and input validation. These appear to be cleanly separated, which is fine. But with ~6,100+ PRs and a codebase of 1.6M+ lines generating PRs at a pace where 14+ merges can happen in under an hour, the risk of two AI-generated PRs touching the same file (e.g., `main.py`) in the same window is high and probably already happening. The deployment email system (which only reports per-merge) would not surface this — a deploy could succeed even if two PRs made contradictory changes to the same function, as long as neither broke the syntax check.

**The gap between #6109 and #6122 is a footprint of the parallelism Jeffrey can't currently see.** There is no evidence in the wiki of any cross-PR conflict detection or serialization mechanism beyond CI/CD itself.

Sources: [deployment-emails-2026-04-07.md](llm-wiki/worldarchitect/wiki/sources/deployment-emails-2026-04-07.md), [log.md](llm-wiki/worldarchitect/wiki/log.md)

---

## Insight 2: The security hardening cluster (PRs #6022, #6026, #6108) was deployed to `mvp-site-app-dev` — the same environment that already had the auth bypass enabled

All five deployments on 2026-04-07 go to the *same Cloud Run service*: `mvp-site-app-dev`. Every email subject reads `✅ SUCCESS: dev Deployment - mvp-site-app-dev`. The wiki explicitly notes: "A production environment likely exists or is planned (PR #6022 explicitly references 'production launch' hardening)" but "Additional services (e.g., a `mvp-site-app-prod`) may exist but were not present in ingested deployment emails."

This creates a structural contradiction. PR #6022 fixed a SMOKE_TOKEN logic bug that "could never be true" — meaning the smoke test bypass was potentially *always active* (always open, not always closed) in the environment that has been running all along. That environment is dev. But every "production launch hardening" fix — auth bypass block, startup validation, rate limit abuse logging, payload size increase — was deployed *into that same dev service*, not a separate production service.

Two possible readings, both uncomfortable:
- **If dev is effectively production** (i.e., real users are hitting `mvp-site-app-dev`), then `TESTING_AUTH_BYPASS` was a live vulnerability against actual users until PR #6022 landed.
- **If dev and prod are separate services and prod was never in the email data**, then the "production hardening" PRs were validated in dev but production may not have received them yet, or may be running a different, untracked revision.

Either way, the SMOKE_TOKEN bug is the most alarming detail: per PR #6022, it "was checking a condition which could never be true." That's not a configuration issue — it's a code logic error that means the intended smoke-test gating was silently non-functional from whenever it was written until April 7, 2026. There is no PR in the ingested data indicating when that bypass code was introduced, meaning the window of exposure is unknown.

Sources: [pr-6022-auth-bypass-disable.md](llm-wiki/worldarchitect/wiki/sources/pr-6022-auth-bypass-disable.md), [cloud-run-infrastructure.md](llm-wiki/worldarchitect/wiki/entities/cloud-run-infrastructure.md), [deployment-emails-2026-04-07.md](llm-wiki/worldarchitect/wiki/sources/deployment-emails-2026-04-07.md)

---

## Insight 3: The Dragon Knight preset is being built as a showcase, but the product's stated identity as an "RPG engine" requires Custom — and Custom is getting no investment

The product is described as "an AI-powered RPG engine for D&D world simulation" (index.md). An engine is general-purpose infrastructure — it implies the core value is the ability to build *any* world, run *any* campaign. But the actual development investment, as revealed by PR #6122, is almost entirely in the Dragon Knight preset path.

The 2-step onboarding redesign (PR #6122, tagged `feat(prototype)`) makes Dragon Knight zero-configuration: Ser Arion is pre-filled, Assiah world is pre-filled, all AI personalities are ON, and the only user decision is which avatar to pick. The Custom path still requires the user to enter a title, character name, world/setting, and configure AI personalities — the old cognitive load is entirely preserved for Custom users, just without the redundant confirm screen.

The `feat(prototype)` tag is the tell. The prototype being validated here is: "can we get new users into a game in 2 clicks?" — which is a *consumer game* hypothesis, not an *RPG engine* hypothesis. An engine-first strategy would be investing in Custom path ergonomics: saved world templates, character import, personality presets. Instead, Custom is effectively static while Dragon Knight gets a first-class express lane.

There are no PRs in the dataset that improve the Custom path's core UX. PR #6122's Custom path changes amount to: removes the confirm screen (same as Dragon Knight), but everything else is unchanged. Meanwhile the memory system (daily backups to `worldarchitect-memory-backups`) is described as supporting "campaign state" generically, but the only named world being persisted is Assiah — Custom campaign persistence architecture is not mentioned anywhere in the wiki.

The hidden strategic consequence: if Jeffrey is positioning WorldArchitect as a platform or engine (implying third-party worlds, external GMs, or API access), the product is being built as a single-player game with one story. The `jleechanorg/beads` repo mentioned in the memory system page ("Memory upgrade for coding agents") suggests awareness of general-purpose memory architecture — but it's being applied to coding agents, not to generalizing the Custom path's world persistence.

**The product vision says "engine." The codebase evolution says "Dragon Knight showcase."**

Sources: [onboarding-flow-evolution.md](llm-wiki/worldarchitect/wiki/comparisons/onboarding-flow-evolution.md), [pr-6122-2step-onboarding.md](llm-wiki/worldarchitect/wiki/sources/pr-6122-2step-onboarding.md), [worldarchitect-ai.md](llm-wiki/worldarchitect/wiki/entities/worldarchitect-ai.md), [memory-system.md](llm-wiki/worldarchitect/wiki/concepts/memory-system.md)
