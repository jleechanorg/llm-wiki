---
title: "Visual Content Validation - End-to-End Data Flow"
type: source
tags: [worldarchitect-ai, e2e-testing, visual-validation, react-v2, content-bug]
sources: [worldarchitect-ai-docs-react_v2_current_status.md-9ee474df.md]
date: 2026-04-07
source_file: raw/test-llm-visual-content-validation.md
last_updated: 2026-04-07
---

## Summary
End-to-end test protocol for validating that React V2 displays actual user-created content instead of hardcoded template content. Tests the complete data flow from user input through API calls, database storage, retrieval, and UI display. Critical bug discovered: game view displayed "Shadowheart" content instead of user-created character "Elara the Brave".

## Key Claims

- **Critical Bug Pattern**: API integration succeeds but wrong content displays — game view renders hardcoded characters/settings
- **Missing Data Flow**: GET request to `/api/campaigns/{id}` missing, causing game view to use hardcoded content
- **Pre-condition**: Must run in REAL PRODUCTION MODE with no test mode parameters
- **Visual Verification Required**: Screenshots must confirm content matches user input, not template defaults

## Key Test Data

```json
{
  "campaign_title": "Visual Test Campaign",
  "character_name": "Zara the Mystic",
  "setting": "Crystal caves of Luminara where gemstones sing ancient melodies"
}
```

## Test Steps

### Step 1: Create Campaign with Specific Content
- Navigate to http://localhost:3002
- Complete real Google authentication
- Create custom campaign with unique character name and setting
- Complete all 3 steps: Basics → AI Style → Launch

### Step 2: Visual Content Verification
- Wait for campaign creation
- Navigate to game view at `/campaigns/{id}`
- Take screenshot and verify:
  - ✅ Character name "Zara the Mystic" appears in story
  - ✅ Setting references "Crystal caves" or "Luminara"
  - ❌ NO hardcoded characters (Shadowheart, Ser Arion)
  - ❌ NO hardcoded settings (Bastion of Eternal Radiance)

### Step 3: API Verification
- Check Flask logs for both POST and GET requests
- POST /api/campaigns (201) — creation
- GET /api/campaigns/{id} (200) — retrieval (CRITICAL)

## Pass/Fail Criteria

### PASS (GREEN)
- Campaign creation API returns 201
- Game view loads with campaign ID in URL
- Story contains user's custom character name
- Story references user's custom setting
- NO hardcoded content present

### FAIL (RED)
- Game view shows hardcoded characters (Shadowheart, Ser Arion)
- Game view shows hardcoded settings (Bastion, World of Assiah)
- Story content doesn't match user input
- No GET request in Flask logs (root cause indicator)
- Generic/template content displayed

## Root Cause

**Symptom**: API integration works but wrong content displays
**Root Cause**: Game view component not fetching or not rendering real campaign data
**Fix Required**: Verify GamePlayView.tsx fetches and displays actual campaign content

## Connections
- [[ReactV2NextPriorityFixes]] — related to React V2 fixes addressing settings/sign-out issues
- [[ReactV2CurrentStatus]] — visual testing confirms fixed/broken status
- [[CacheBustingE2ETesting]] — related E2E testing methodology

## Contradictions
- None identified yet — this test is part of ongoing validation work
