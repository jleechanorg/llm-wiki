---
title: "React V2 - Next Priority Fixes"
type: source
tags: [react, frontend, worldarchitect.ai, react-v2, fixes, settings, sign-out]
date: 2025-08-08
source_file: /Users/jleechan/repos/worldarchitect.ai/docs/react_v2_next_priority_fixes.md
last_updated: 2026-04-07
---

## Summary
A prioritized fix list for React V2 frontend addressing critical security issues (sign-out capability), URL routing, and UI cleanup. Based on visual testing evidence and gap analysis. Three sprints totaling 75-90 minutes to implement all critical fixes.

## Key Claims

### IMMEDIATE PRIORITY: Settings & Sign-Out Access
- **Fix #1**: Add Global Settings Button to header component — critical because users cannot sign out (security issue)
- **Fix #2**: Implement Settings Page with Sign-Out — requires Settings page route, Firebase auth integration, and redirect to login after sign-out

### HIGH PRIORITY: URL Routing
- **Fix #3**: Campaign Click Navigation — clicking campaigns should update URL to `/campaign/:id`, enabling browser back/forward and deep linking

### QUICK WINS
- **Fix #4**: Remove per-campaign settings buttons (gear icons) from campaign cards — simpler than implementing full campaign-specific settings

## Key Quotes

> "The highest priority is adding the settings button and sign-out functionality. This unblocks a critical security issue where users cannot sign out of their accounts."

## Connections
- [[React V2 Settings Button Discovery]] — appears to contradict (this source says add settings button, discovery says button already exists but visibility issue)
- [[Worldarchitect.ai]] — project this frontend belongs to

## Contradictions
- **Contradicts [[React V2 Settings Button Discovery]]**: This source says "add global settings button" as Fix #1, but the earlier discovery source states the settings button already exists and is a visibility issue, not a missing feature. The earlier source appears more accurate as it was based on actual code discovery.

## Implementation Details

### Sprint 1 (30 min) - Critical Security
- Add settings button to header
- Create settings page with sign-out
- Test sign-out flow
- Verify redirect to login

### Sprint 2 (30 min) - Navigation
- Implement React Router v6 properly
- Add campaign click navigation
- Test URL updates
- Verify browser history works

### Sprint 3 (15 min) - Cleanup
- Remove/hide per-campaign settings buttons
- Clean up console errors
- Final testing

### Success Metrics
1. User can sign out - Critical security requirement
2. URLs update on navigation - Core UX requirement
3. No broken UI elements - Professional appearance
4. Zero console errors - Clean implementation