---
title: "LLMProviderWindowScheduling"
type: concept
tags: [dk2d-chrono]
date: 2026-07-14
last_updated: 2026-07-14
---

LLM provider health is a scheduling axis for real-LLM test runs. Observed on MiniMax (2026-07-13/14): long generations (2-6k chars) hang mid-stream >120s overnight PT while short turns stay at ~2.05s first-token — run trend 15/15 → 13 → 13 → 14 → 10 across the night, then 14 → 14 → 15 in the morning window (15:30Z+). Schedule real-LLM evidence runs morning/midday PT; treat a ~exact-timeout total_s as "whose timeout?" (harness poll cap vs provider) before attributing.

Source: [[feedback-2026-07-14-dk2d-chrono-operational-lessons]] · Related: [[EvidenceHarnessDiscipline]]
