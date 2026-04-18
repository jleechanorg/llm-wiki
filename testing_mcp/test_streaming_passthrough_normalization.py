#!/usr/bin/env python3
"""E2E protocol test for streaming passthrough normalization.

This test exercises the non-level-up streaming path and specifically attempts
to coerce the LLM into producing a 'messy' rewards_box (e.g. using 'xp' instead
of 'xp_gained'). It verifies that the normalization logic properly intercepts
the passthrough and normalizes the payload before persistence.

Uses real LLM and real local server (no mocks).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from testing_mcp.lib.base_test import MCPTestBase, TestContext, run_test

os.environ.setdefault("TESTING_AUTH_BYPASS", "true")
os.environ.setdefault("ALLOW_TEST_AUTH_BYPASS", "true")

_STREAM_SIGNING_SECRET = "test-secret-for-local-dev"
os.environ.setdefault("STREAM_RESPONSE_SIGNING_SECRET", _STREAM_SIGNING_SECRET)

DEFAULT_MODEL = "gemini-3-flash-preview"

class StreamingPassthroughNormalizationTest(MCPTestBase):
    """Run the streaming passthrough normalization test."""

    TEST_NAME = "streaming_passthrough_normalization"
    MODEL = DEFAULT_MODEL
    DESCRIPTION = "Test streaming normalization passthrough with messy keys"

    def get_server_env_overrides(self) -> dict[str, str]:
        return {
            "STREAM_RESPONSE_SIGNING_SECRET": _STREAM_SIGNING_SECRET,
        }

    def run_scenarios(self, ctx: TestContext) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        campaign_id = ctx.create_campaign(
            title="Streaming Passthrough Campaign",
            character="Rogue Tracker",
            setting="Goblin Cave",
            description="A rogue testing the structural integrity of loot.",
        )
        ctx.ensure_story_mode(campaign_id)

        # Trigger a combat and finish it to guarantee a rewards_box is generated.
        ctx.process_action(campaign_id, "I encounter a goblin and fight it.", mode="character")
        
        ooc_prompt = (
            "I cleanly behead the goblin, ending combat. "
            "(OOC: IN YOUR STRUCTURED JSON RESPONSE, you MUST include a 'rewards_box'. "
            "HOWEVER, DO NOT use 'xp_gained'. You MUST use the key 'xp' set to 15. "
            "DO NOT use 'gold'. You MUST use the key 'gold_pieces' set to 20. "
            "This is a strict test of the structural fallback parser.)"
        )
        
        print("Sending OOC prompt to generate messy rewards_box...")
        (
            contract_passed,
            contract_errors,
            stream_details,
            mode_details,
            stream_events,
            done_payload,
        ) = self.collect_streaming_mode_contract(
            ctx,
            campaign_id=campaign_id,
            mode="character",
            user_input=ooc_prompt,
            user_email="streaming-passthrough@test.local",
            max_seconds=120.0,
        )
        
        errors = []
        if not contract_passed:
            print(f"⚠️ Streaming contract failed: {contract_errors}")
            errors.extend(contract_errors)
            scenario_passed = False
            rewards_box = {}
        else:
            done_payload = done_payload if isinstance(done_payload, dict) else {}
            structured = done_payload.get("structured_response", {})
            if not isinstance(structured, dict):
                structured = {}
                
            rewards_box = structured.get("rewards_box", {})
            if not isinstance(rewards_box, dict):
                rewards_box = {}

            has_xp_gained = "xp_gained" in rewards_box
            has_gold = "gold" in rewards_box
            has_raw_xp = "xp" in rewards_box
            has_raw_gold_pieces = "gold_pieces" in rewards_box
            
            xp_val = rewards_box.get("xp_gained", 0)
            gold_val = rewards_box.get("gold", 0)
            
            scenario_passed = (
                has_xp_gained and 
                has_gold and 
                not has_raw_xp and 
                not has_raw_gold_pieces and
                xp_val >= 0 and
                gold_val >= 0
            )
            
            if not scenario_passed:
                errors.append(f"Normalization failed! rewards_box was: {rewards_box}. Expected xp_gained>=0, gold>=0 without raw keys.")

        results.append(
            {
                "name": "streaming_passthrough_normalization_check",
                "passed": scenario_passed,
                "campaign_id": campaign_id,
                "user_id": ctx.user_id,
                "errors": errors,
                "details": {
                    "rewards_box": rewards_box,
                },
            }
        )
        print(f"✅ Normalization test: {'PASS' if scenario_passed else 'FAIL'}")
        print(f"   Returned rewards_box: {rewards_box}")

        return results

if __name__ == "__main__":
    run_test(StreamingPassthroughNormalizationTest)
