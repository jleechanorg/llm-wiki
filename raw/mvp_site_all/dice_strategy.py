"""Dice strategy selection.

This module centralizes how we decide between:
- Gemini 3.x code_execution (single call, structured JSON)
- universal two-phase tool calling (server executes dice)

Kept separate from mvp_site/constants.py to avoid turning constants into a
grab-bag of logic and to make unit testing clearer.
"""

from __future__ import annotations

from mvp_site import constants

DICE_STRATEGY_CODE_EXECUTION = "code_execution"
DICE_STRATEGY_NATIVE_TWO_PHASE = "native_two_phase"


def get_dice_roll_strategy(model_name: str, provider: str = "") -> str:
    """Determine the dice rolling strategy for a given model/provider.

    Provider-based strategy:
    - Gemini: code_execution (Python code for dice)
    - Cerebras/OpenRouter: native_two_phase (tool_requests)
    """
    # Gemini uses code_execution - Python code generates dice rolls
    if (
        provider.lower() == "gemini"
        and model_name in constants.MODELS_WITH_CODE_EXECUTION
    ):
        return DICE_STRATEGY_CODE_EXECUTION

    # Cerebras/OpenRouter use native_two_phase - server executes tool_requests
    return DICE_STRATEGY_NATIVE_TWO_PHASE
