---
title: "Firebase"
type: concept
tags: [backend, database, google, realtime]
sources: [shared-type-definitions]
last_updated: 2026-04-08
---

## Description
Google's mobile and web application development platform providing backend services including Firestore NoSQL database, Authentication, and Cloud Functions.

## Usage in WorldArchitect.AI
Firebase Firestore stores:
- CampaignData (campaigns collection)
- EntityData (embedded in campaigns)
- StateUpdate (state_updates array)
- MissionData (missions collection)

## Key Collections
- users/{user_id}/campaigns/{campaign_id}
- users/{user_id}/campaigns/{campaign_id}/entities/{entity_id}
- users/{user_id}/campaigns/{campaign_id}/missions/{mission_id}
