---
title: "V2 Campaign Creation Performance Improvements"
type: source
tags: [performance, ux, frontend, react, campaign-creation]
sources: []
last_updated: 2026-04-07
---

## Summary
Comprehensive performance and UX improvements to the V2 Campaign Creation system that reduced perceived wait time from 10-11 seconds of anxiety to a managed, informative experience with progress indicators, error recovery, and power-user options.

## Key Claims

- **Progress Feedback**: Animated progress bar (0% → 100%) with contextual status messages at each stage ("Setting up your world...", "Preparing AI personalities...", "Creating your character...", "Weaving the story threads...", "Almost ready...")
- **Optimistic UI**: Show creation interface immediately on click, start progress simulation before API completes for immediate feedback
- **Error Recovery**: 15-second timeout warning, up to 3 automatic retry attempts with smart error classification (network/timeout vs authentication vs generic API errors)
- **Power User Features**: "Skip Animation" button speeds up progress from 800ms to 200ms intervals, jumps to 90% when clicked
- **Technical Optimization**: Reduced mock service delay from 600ms to 1500ms, reduced delay variance from 200ms to 100ms for predictable timing

## Key Quotes

> "Your campaign will be created in a few moments. You can customize settings later in the game." — Helpful tip displayed during creation

> "This is taking longer than expected..." — Timeout warning message at 15 seconds

## Connections

- [[CampaignCreationV2]] — frontend component implementing these improvements
- [[MockService]] — service with optimized delays
- [[ErrorHandling]] — smart error classification pattern
- [[UserExperience]] — broader UX improvements in the system

## Contradictions

- None identified — this document describes improvements to an existing feature

## Technical Implementation

### State Management
```typescript
const [creationProgress, setCreationProgress] = useState(0)
const [creationStatus, setCreationStatus] = useState('')
const [showOptimisticUI, setShowOptimisticUI] = useState(false)
const [retryCount, setRetryCount] = useState(0)
const [isTimeout, setIsTimeout] = useState(false)
const [skipAnimation, setSkipAnimation] = useState(false)
```

### Progress Simulation Algorithm
The progress simulation runs independent of actual API timing, showing completion animation even if API calls take longer than expected — decoupling perceived performance from actual backend latency.

## Results

1. **Perceived Performance**: 10-11 second wait now feels manageable with clear progress indicators
2. **Anxiety Reduction**: Users know exactly what's happening and how long it will take
3. **Error Recovery**: Failed campaigns can be retried without starting over
4. **Power User Support**: Skip animation option for users who want speed