"""Provider-specific LLM client implementations."""

import importlib

# Cold-start optimization: provider submodules are NOT eagerly imported here.
# Previously, importing this package triggered gemini_provider (google.genai, ~840ms)
# at package init time. Providers now load on first attribute access via __getattr__.
# ContextTooLargeError and check_context_too_large are re-exported for backward compat.
from .provider_utils import ContextTooLargeError, check_context_too_large


def __getattr__(name: str):
    """Lazy submodule access for provider names (cold-start optimization)."""
    if name in (
        "cerebras_provider",
        "gemini_provider",
        "openclaw_provider",
        "openrouter_provider",
        "provider_utils",
    ):
        module = importlib.import_module(f"mvp_site.llm_providers.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "cerebras_provider",
    "gemini_provider",
    "openclaw_provider",
    "openrouter_provider",
    "provider_utils",
    "ContextTooLargeError",
    "check_context_too_large",
]
