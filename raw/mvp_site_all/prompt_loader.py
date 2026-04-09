"""
Prompt variant loading system for dice strategy-specific prompts.

Replaces hidden string injection with explicit, version-controlled prompt files.
"""

from pathlib import Path
from typing import Literal

from mvp_site import logging_util

DiceStrategy = Literal["code_execution", "tool_requests", "native", "native_two_phase"]


def load_prompt_variant(base_name: str, dice_strategy: DiceStrategy) -> str:
    """Load prompt file variant based on dice strategy.

    This replaces the previous approach of injecting code_exec_override strings
    at runtime. Now all prompt variants are explicit markdown files that can be
    reviewed, version-controlled, and tested independently.

    Args:
        base_name: Base prompt filename without .md extension
                   (e.g., "mechanics_system_instruction")
        dice_strategy: Dice generation strategy determining which variant to load
                      - "code_execution": Load _code_execution.md variant
                      - "tool_requests"/"native"/"native_two_phase": Load default

    Returns:
        Prompt file contents as string

    Raises:
        FileNotFoundError: If neither variant nor default file exists

    Example:
        >>> # For code_execution, loads mechanics_system_instruction_code_execution.md
        >>> prompt = load_prompt_variant("mechanics_system_instruction", "code_execution")
        >>> assert "DICE VALUES ARE UNKNOWABLE" in prompt

        >>> # For tool_requests, loads mechanics_system_instruction.md
        >>> prompt = load_prompt_variant("mechanics_system_instruction", "tool_requests")
        >>> assert "BEGIN_TOOL_REQUESTS_DICE" in prompt
    """
    # Determine prompts directory relative to this file
    current_file = Path(__file__)
    prompts_dir = current_file.parent / "prompts"

    # Initialize variant_path to avoid NameError in error messages
    variant_path = None

    # Try code_execution variant first if strategy matches
    if dice_strategy == "code_execution":
        variant_path = prompts_dir / f"{base_name}_code_execution.md"
        if variant_path.exists():
            logging_util.info(f"Loading code_execution variant: {variant_path.name}")
            with open(variant_path, encoding="utf-8") as f:
                return f.read()
        else:
            logging_util.warning(
                f"Code execution variant not found: {variant_path.name}, "
                f"falling back to default"
            )

    # Fall back to default variant
    default_path = prompts_dir / f"{base_name}.md"
    if not default_path.exists():
        variant_msg = f"checked {variant_path.name} and " if variant_path else ""
        raise FileNotFoundError(f"Prompt file not found: {variant_msg}{default_path}")

    logging_util.info(f"Loading default prompt: {default_path.name}")
    with open(default_path, encoding="utf-8") as f:
        return f.read()
