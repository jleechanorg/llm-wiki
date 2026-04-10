---
title: "CampaignCreationV2"
type: entity
tags: [react-component, campaign-creation, memory-management]
sources: []
last_updated: 2026-04-08
---

React component responsible for the campaign creation flow in the application. The memory leak tests verify that all JavaScript timers are properly cleaned up when the component unmounts.

## Related Tests
- [[CampaignCreationV2 Memory Leak Tests]] — validates timer cleanup on unmount
