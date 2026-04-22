---
title: "Budget Overflow Test Stabilization"
type: concept
tags: [testing, budget, stability, flakiness, worldai]
last_updated: 2026-04-14
---

## Summary

Budget overflow tests fail non-deterministically when token/compute budgets are exhausted mid-test. Stabilization involves capping test runtime, mocking external calls, and setting deterministic budget thresholds.

## Key Patterns

**Timeout-wrapped test execution**:
```python
@pytest.mark.asyncio
async def test_budget_overflow():
    with asyncio.timeout(30):  # Hard cap
        result = await run_with_budget(mock_budget(1000))
        assert result.status == "ok"
```

**Deterministic budget simulation**:
```python
def mock_budget(cap_tokens: int):
    async def _mock(*args, **kwargs):
        return {"usage": {"total_tokens": cap_tokens - 1}}
    return _mock
```

**Retry with exponential backoff for transient overflow**:
```python
for attempt in range(3):
    try:
        result = await bounded_call()
        break
    except BudgetOverflow:
        await asyncio.sleep(2 ** attempt)
```

## Root Causes
- LLM response variability causing token count spikes
- Missing budget guardrails in production code paths
- Test environment having lower budget limits than prod

## Connections
- [[BudgetAllocation]] — Budget management patterns
- [[TokenBudgetCalculation]] — Token budget formulas
