---
title: "Launch CTA Atomicity"
type: concept
tags: [launch, cta, atomicity, user-experience, worldai]
last_updated: 2026-04-14
---

## Summary

Launch CTA (Call-to-Action) atomicity refers to the principle that the launch action should be a single, indivisible operation — either fully completes or fully rolls back, with no partial states visible to the user.

## Why Atomicity Matters

If a launch action (e.g., starting a campaign, deploying a world) is interrupted:
- User could be charged without campaign starting
- Campaign state could be inconsistent
- UX confusion about what actually happened

## Pattern

**Optimistic UI with server confirmation**:
```python
async def launch_campaign(campaign_id: str) -> LaunchResult:
    # 1. Optimistically update UI
    ui_state.transition_to("launching")

    try:
        # 2. Server action
        result = await api.start_campaign(campaign_id)

        # 3. Confirm UI or rollback
        if result.success:
            ui_state.transition_to("running")
            return LaunchResult(success=True)
        else:
            ui_state.rollback()
            return LaunchResult(success=False, error=result.error)
    except Exception as e:
        ui_state.rollback()
        raise
```

**Idempotent launch**:
```python
# Safe to retry — does not create duplicate campaigns
PUT /api/campaign/{id}/launch  # Idempotent PUT
```

## UX Requirements

- Button disabled immediately on click (prevent double-submit)
- Loading indicator visible within 100ms
- Error message if action fails
- Success confirmation within 30s (with timeout error if exceeded)

## Connections
- [[StateTransitions]] — State machine for UI states
- [[RewardsBoxAtomicity]] — Rewards box update atomicity
