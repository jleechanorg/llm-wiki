"""Regression tests for startup import behavior after lazy-loading refactors."""

from __future__ import annotations

import importlib
import sys

import pytest


def _clear_modules(module_names: list[str]) -> dict[str, object | None]:
    """Temporarily remove modules, returning prior cached values."""
    return {name: sys.modules.pop(name, None) for name in module_names}


def _restore_modules(snapshot: dict[str, object | None]) -> None:
    """Restore a module snapshot captured by `_clear_modules`."""
    for name, module in snapshot.items():
        if module is None:
            sys.modules.pop(name, None)
            continue
        sys.modules[name] = module


def _is_lazy_proxy(module) -> bool:
    """Return True if *module* is a LazyLoader proxy (body not yet executed).

    LazyLoader works by installing a __class__ cell that triggers exec on first
    attr access. A proxy's __spec__.loader is still a LazyLoader instance.
    """
    try:
        return isinstance(
            getattr(module, "__spec__", None) and module.__spec__.loader,
            importlib.util.LazyLoader,
        )
    except Exception:
        return False


def test_streaming_orchestrator_import_keeps_heavy_modules_lazy() -> None:
    """`mvp_site.streaming_orchestrator` import must not execute heavy module bodies.

    All three lazy modules (firestore_service, gemini_provider, llm_service) ARE
    registered in sys.modules immediately — that's how LazyLoader works — but their
    bodies (which pull google.genai / google.cloud.firestore) must not have run yet.
    """
    targets = [
        "mvp_site.streaming_orchestrator",
        "mvp_site.firestore_service",
        "mvp_site.llm_providers.gemini_provider",
        "mvp_site.llm_service",
        "google",
        "google.genai",
        "google.cloud",
        "google.cloud.firestore",
    ]
    snapshot = _clear_modules(targets)
    try:
        importlib.import_module("mvp_site.streaming_orchestrator")

        # Lazy proxies are registered in sys.modules immediately.
        assert "mvp_site.firestore_service" in sys.modules
        assert "mvp_site.llm_providers.gemini_provider" in sys.modules
        assert "mvp_site.llm_service" in sys.modules

        # The heavy transitive deps must NOT be loaded (bodies not executed).
        assert "google.genai" not in sys.modules
        assert "google.cloud.firestore" not in sys.modules
    finally:
        _restore_modules(snapshot)


def test_streaming_orchestrator_llm_service_body_deferred() -> None:
    """`llm_service` body must not execute at streaming_orchestrator import time."""
    targets = [
        "mvp_site.streaming_orchestrator",
        "mvp_site.firestore_service",
        "mvp_site.llm_providers.gemini_provider",
        "mvp_site.llm_service",
        "google",
        "google.genai",
        "google.cloud",
        "google.cloud.firestore",
    ]
    snapshot = _clear_modules(targets)
    try:
        importlib.import_module("mvp_site.streaming_orchestrator")

        # google.genai still absent — proves llm_service body hasn't executed.
        assert "google.genai" not in sys.modules
    finally:
        _restore_modules(snapshot)


def test_main_import_defers_cloud_backed_modules() -> None:
    """`mvp_site.main` should keep google.genai out of the startup path."""
    targets = [
        "mvp_site.main",
        "mvp_site.firestore_service",
        "mvp_site.llm_providers.openclaw_provider",
        "mvp_site.world_logic",
        "mvp_site.llm_service",
        "google",
        "google.genai",
        "google.cloud",
        "google.cloud.firestore",
    ]
    snapshot = _clear_modules(targets)
    try:
        try:
            importlib.import_module("mvp_site.main")
        except ModuleNotFoundError as exc:
            pytest.skip(f"main import unavailable in this environment: {exc}")

        # The critical cold-start check: google.genai must not be loaded.
        assert "google.genai" not in sys.modules
        assert "google.cloud.firestore" not in sys.modules
    finally:
        _restore_modules(snapshot)
