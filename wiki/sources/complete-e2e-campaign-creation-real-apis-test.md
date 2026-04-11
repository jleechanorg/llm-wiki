---
title: "Complete E2E Campaign Creation Test with Real APIs"
type: source
tags: [javascript, testing, e2e, playwright, firebase, gemini, real-apis]
source_file: "raw/test_complete_e2e_campaign_creation_real_apis.js"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end test validating the complete user journey for campaign creation using REAL Firebase and Gemini APIs (no mocks). Tests the full workflow from homepage navigation through campaign wizard steps to real AI-powered chat responses.

## Key Claims
- **Real API integration**: Tests use actual Firebase Firestore and Gemini API calls rather than mocks
- **Complete user journey**: Validates homepage → dashboard → campaign wizard (steps 1-3) → chat interface → real AI responses
- **Playwright automation**: Browser-based testing with headless Chromium for consistent screenshots
- **Test mode with real APIs**: Uses test auth bypass while keeping real backend services
- **Screenshot validation**: Captures each step for visual verification of the complete flow

## Key Test Steps
1. Navigate to homepage with real authentication
2. Initialize test mode with real APIs (test_mode=true, test_user_id)
3. Wait for dashboard to load with campaign list
4. Click "Start New Campaign" to open wizard
5. Fill Step 1: campaign title, description, genre, tone
6. Fill Step 2: character name and details
7. Complete wizard and reach chat interface
8. Send message and receive real AI response
9. Screenshot final chat functionality

## Connections
- [[Playwright]] — browser automation framework used for E2E testing
- [[Firebase]] — real backend service for data persistence
- [[Gemini]] — real AI API for generating responses
- [[CampaignCreationWizard]] — multi-step wizard UI for campaign setup

## Contradictions
- []
