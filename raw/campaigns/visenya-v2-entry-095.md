---
title: "Visenya V2 — Scene 095"
type: source
tags: [campaign, scene, visenya-v2]
last_updated: 2026-04-12
scene_number: 95
scene_total: 277
source_file: /tmp/campaign_downloads_v2/
---

## Scene 095 Summary

============================================================ [Timestamp: 298 AC, Month 4, Day 6, 11:45:00 Location: The Council Solar, Great Pyramid of Astapor Status: Lvl 3 Dragonlord | HP: 20/20 | XP: 1375/2700 | Gold: 1,500gp (Hidden) Active Effects: Belaerys Catalyst (+2 Spell DC/Atk, +2 Dragon/Mind), Lack of Confidence (-2 Social Penalty)]  Game Master: The DC 18 for the Gilded Leash proposal was calculated as follows:  **DC Breakdown:** - **Base DC 15**: Standard Difficulty Class for swayi

## Key Details

- **Location:** The Council Solar, Great Pyramid of Astapor
- **Level hint:** 3
- **Word count:** 620
- **Campaign:** [[Visenya V2]]
- **Entry:** [[visenya-v2-entry-095]]

---

## Full Scene Content

============================================================
[Timestamp: 298 AC, Month 4, Day 6, 11:45:00
Location: The Council Solar, Great Pyramid of Astapor
Status: Lvl 3 Dragonlord | HP: 20/20 | XP: 1375/2700 | Gold: 1,500gp (Hidden)
Active Effects: Belaerys Catalyst (+2 Spell DC/Atk, +2 Dragon/Mind), Lack of Confidence (-2 Social Penalty)]

Game Master:
The DC 18 for the Gilded Leash proposal was calculated as follows:

**DC Breakdown:**
- **Base DC 15**: Standard Difficulty Class for swaying a King/Queen-tier NPC on major policy.
- **Severity +3 (Submission Tier)**: You are proposing a 'Submission' level request. Asking the 'Breaker of Chains' to allow former masters back into the power structure is a radical ideological conflict for her, triggering the highest difficulty modifier.
- **Ally Support -2 (Joint Appeal)**: Ser Jorah's (Lvl 8) endorsement successfully lowered the difficulty from what would have been a DC 20.
- **Lack of Confidence +2 (Trauma Penalty)**: Per your active constraint, your feigned trauma adds +2 to the DC (or -2 to your roll). Narratively, Daenerys sees your strategic logic as a symptom of your fear/shaken state rather than clinical reality, making her more resistant to the idea because she wants to 'protect' you from such harsh compromises.

**Roll Breakdown:**
- **Roll Result (7)**: The 1d20 result was a 7.
- **Modifier (+6)**: Your Intelligence (+4) plus Proficiency (+2) via Royal Insight.
- **Total (13)**: 7 + 6 = 13 vs DC 18.

**History Bonus:** While you have a history of convincing her, social HP challenges with King-tier NPCs require sustained effort. You have dealt 5 'successes' worth of progress, but her core belief regarding Slavery makes this specific 'Gilded Leash' arc the hardest hurdle yet.

Player (freeform):
## Agent Handoff Prompt

```
## Context: Snapchat SEO Investigation - November 2024 Ranking Drop

### What Was Done

Investigated why Snapchat lost SEO ranking in November 2024 (position dropped from ~6-7 to ~18). 

**Root Cause Found:**
- PR #5953 (Nov 20, 2024) exposed 538K profile URLs to Google
- URLs used redirect format `/add/username` instead of canonical `/@username`
- Only 17% indexing rate (94K of 538K URLs indexed)
- Coincided with Google's November 2024 Core Update penalizing thin content

### PRs Created

1. **[PR #8876](https://github.sc-corp.net/Snapchat/web/pull/8876)** - Fix URL format
   - Changes `siteUrl` from `/add` to root domain
   - Sitemap now uses canonical `/@username` URLs
   - File: `apps/profiles/next-sitemap.public-profiles.config.js`

2. **[PR #8877](https://github.sc-corp.net/Snapchat/web/pull/8877)** - Reduce sitemap size  
   - Limits sitemap from 538K to 100K profiles
   - Adds `topProfiles.slice(0, SITEMAP_PROFILE_LIMIT)`
   - File: `apps/profiles/next-sitemap.public-profiles.config.js`

### Historical PRs Referenced

| Date | PR | What Happened |
|------|-----|---------------|
| Oct 1, 2024 | [#5686](https://github.sc-corp.net/Snapchat/web/pull/5686) | Created profile sitemaps with 538K usernames |
| Oct 1, 2024 | [#5692](https://github.sc-corp.net/Snapchat/web/pull/5692) | Changed siteUrl to `/add` (created redirect URL problem) |
| Nov 20, 2024 | [#5953](https://github.sc-corp.net/Snapchat/web/pull/5953) | **Exposed sitemaps to Google** (trigger date) |

### Key Discovery: Two Different Sitemaps

| Sitemap | Source | Size |
|---------|--------|------|
| `/add/sitemap.xml` | `top_public_profiles.json` (static) | 538K → 100K (fixed) |
| `/sitemaps/add/sitemap-index.xml` | `profiles.ts` (BigQuery) | ~220K (different sitemap) |

### Report Saved
`~/Downloads/snapchat-seo-investigation-report.md`

### What's Left To Do

1. **Get PRs reviewed and merged**
2. **Research task was interrupted** - wanted to use `/research` command to find SEO sitemap best practices from web sources to validate our approach
3. **Monitor Search Console** after changes deploy - track if indexing rate improves over 2-4 weeks
4. **Consider future work:**
   - Consolidate the two confusingly-named profile sitemaps
   - Add content enhancement to profile pages (user said "can worry about this later")

### Technical Notes

- Git push requires `dangerouslyDisableSandbox: true` due to SOCKS proxy through SSHFE
- Use `--repo Snapchat/web` flag with all `gh` commands (worktree issue with enterprise GitHub)
- The JSON file `top_public_profiles.json` has 538,430 usernames pre-sorted by engagement
```

============================================================
