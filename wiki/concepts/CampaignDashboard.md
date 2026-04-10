---
title: "Campaign Dashboard"
type: concept
tags: [ui, v2, user-experience]
sources: []
last_updated: 2026-04-08
---

## Definition
The campaign dashboard is the main view shown to users who already have campaigns in the system. It displays a list of existing campaigns rather than the onboarding "Create Your First Campaign" landing page.

## Display Logic
- If user has campaigns → show dashboard with campaign list
- If user has no campaigns → show landing page with creation CTA

## Bug Fixed
V2 was incorrectly showing landing page despite user having 503 campaigns.

## Related Concepts
- [[V2CampaignDisplayLogic]]
- [[LandingPage]]
