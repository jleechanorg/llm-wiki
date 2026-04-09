import pytest

from mvp_site import constants, llm_service
from mvp_site.game_state import GameState


def _raise_datastore_unavailable(_user_id):
    raise KeyError("datastore unavailable")


@pytest.fixture(autouse=True)
def clear_testing_env(monkeypatch):
    monkeypatch.delenv("TESTING_AUTH_BYPASS", raising=False)
    monkeypatch.delenv("MOCK_SERVICES_MODE", raising=False)
    monkeypatch.delenv("FORCE_TEST_MODEL", raising=False)
    monkeypatch.delenv("ALLOW_ALTERNATIVE_PROVIDER_IN_TEST", raising=False)
    monkeypatch.delenv("FORCE_PROVIDER", raising=False)


def test_selects_gemini_by_default(monkeypatch):
    monkeypatch.setattr(llm_service, "get_user_settings", lambda user_id: {})

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == constants.DEFAULT_LLM_PROVIDER
    assert selection.model == llm_service.DEFAULT_MODEL


def test_prefers_openrouter_when_configured(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {
            "llm_provider": "openrouter",
            "openrouter_model": "meta-llama/llama-3.1-70b-instruct",
        },
    )

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == "openrouter"
    assert selection.model == "meta-llama/llama-3.1-70b-instruct"


def test_prefers_cerebras_when_configured(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {
            "llm_provider": "cerebras",
            "cerebras_model": "llama-3.3-70b",  # Updated: 3.1-70b retired from Cerebras
        },
    )

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == "cerebras"
    assert selection.model == "llama-3.3-70b"


def test_invalid_provider_raises_fail_closed_error(monkeypatch):
    monkeypatch.setattr(
        llm_service, "get_user_settings", lambda user_id: {"llm_provider": "invalid"}
    )

    with pytest.raises(llm_service.LLMRequestError, match="PROVIDER_SELECTION_INVALID_PROVIDER"):
        llm_service._select_provider_and_model("user-1")


def test_empty_provider_raises_fail_closed_error(monkeypatch):
    monkeypatch.setattr(
        llm_service, "get_user_settings", lambda user_id: {"llm_provider": ""}
    )

    with pytest.raises(
        llm_service.LLMRequestError, match="PROVIDER_SELECTION_INVALID_PROVIDER"
    ):
        llm_service._select_provider_and_model("user-1")


def test_no_user_id_returns_defaults(monkeypatch):
    """When no user_id is provided, return default provider and model."""
    selection = llm_service._select_provider_and_model(None)

    assert selection.provider == constants.DEFAULT_LLM_PROVIDER
    assert selection.model == llm_service.DEFAULT_MODEL


def test_force_provider_env(monkeypatch):
    """FORCE_PROVIDER env var should override user settings."""
    monkeypatch.setenv("FORCE_PROVIDER", "gemini")

    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {
            "llm_provider": "openrouter",
            "openrouter_model": "meta-llama/llama-3.1-70b-instruct",
        },
    )

    selection = llm_service._select_provider_and_model("user-1")

    # Should use FORCE_PROVIDER, not user settings
    assert selection.provider == "gemini"
    assert selection.model == constants.DEFAULT_GEMINI_MODEL


def test_force_provider_with_user_settings(monkeypatch):
    """FORCE_PROVIDER should use openclaw provider with default model."""
    monkeypatch.setenv("FORCE_PROVIDER", "openclaw")

    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {"llm_provider": "openclaw"},
    )

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == "openclaw"
    assert selection.model == constants.DEFAULT_OPENCLAW_MODEL


def test_testing_auth_bypass_uses_user_settings(monkeypatch):
    """TESTING_AUTH_BYPASS should NOT force provider - use user settings."""
    monkeypatch.setenv("TESTING_AUTH_BYPASS", "true")
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {
            "llm_provider": "cerebras",
            "cerebras_model": "llama-3.3-70b",
        },
    )

    selection = llm_service._select_provider_and_model("user-1")

    # Should use user settings, not forced Gemini
    assert selection.provider == "cerebras"
    assert selection.model == "llama-3.3-70b"


def test_legacy_gemini_models_are_mapped(monkeypatch):
    # Use an actual legacy model that redirects (gemini-2.5-pro → gemini-2.0-flash)
    # Note: gemini-2.5-flash is a valid current model, NOT a legacy redirect
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {"llm_provider": "gemini", "gemini_model": "gemini-2.5-pro"},
    )

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == constants.DEFAULT_LLM_PROVIDER
    assert selection.model == llm_service.DEFAULT_MODEL


def test_invalid_gemini_model_defaults(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {"llm_provider": "gemini", "gemini_model": "unsupported"},
    )

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == constants.DEFAULT_LLM_PROVIDER
    assert selection.model == llm_service.DEFAULT_MODEL


def test_prefers_openclaw_when_configured(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {"llm_provider": "openclaw"},
    )

    selection = llm_service._select_provider_and_model("user-1")

    assert selection.provider == "openclaw"
    assert selection.model == constants.DEFAULT_OPENCLAW_MODEL


def test_openclaw_gateway_port_read_from_user_settings(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {
            "llm_provider": "openclaw",
            "openclaw_gateway_port": 28999,
        },
    )

    port = llm_service._get_openclaw_gateway_port("user-1", "openclaw")

    assert port == 28999


def test_openclaw_gateway_port_none_for_non_openclaw_provider(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {"openclaw_gateway_port": 28999},
    )

    port = llm_service._get_openclaw_gateway_port("user-1", "gemini")

    assert port is None


def test_openclaw_gateway_port_invalid_when_out_of_range(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "get_user_settings",
        lambda user_id: {
            "llm_provider": "openclaw",
            "openclaw_gateway_port": 70000,
        },
    )

    port = llm_service._get_openclaw_gateway_port("user-1", "openclaw")

    assert port is None


def test_openclaw_not_in_byok_provider_map():
    assert "openclaw" not in llm_service._BYOK_PROVIDER_API_KEY_FIELDS


def test_provider_selection_uses_defaults_when_settings_missing(monkeypatch):
    monkeypatch.setattr(llm_service, "get_user_settings", lambda user_id: None)

    selection = llm_service._select_provider_and_model("user-openclaw")

    assert selection.provider == constants.DEFAULT_LLM_PROVIDER
    assert selection.model == llm_service.DEFAULT_MODEL


def test_provider_selection_no_cross_provider_fallback_on_settings_exception(
    monkeypatch,
):
    monkeypatch.setattr(llm_service, "get_user_settings", _raise_datastore_unavailable)

    with pytest.raises(
        llm_service.LLMRequestError,
        match="PROVIDER_SELECTION_SETTINGS_EXCEPTION",
    ):
        llm_service._select_provider_and_model("user-openclaw")


def test_process_action_openclaw_selection_failure_is_explicit(monkeypatch, caplog):
    monkeypatch.setattr(llm_service, "get_user_settings", _raise_datastore_unavailable)

    api_called = {"value": False}

    def _forbidden_api_call(*args, **kwargs):
        api_called["value"] = True
        raise AssertionError("LLM API should never be called on selection failure")

    monkeypatch.setattr(llm_service, "_call_llm_api_with_llm_request", _forbidden_api_call)

    with pytest.raises(
        llm_service.LLMRequestError,
        match="PROVIDER_SELECTION_SETTINGS_EXCEPTION",
    ):
        llm_service.continue_story(
            user_input="Look around",
            mode=constants.MODE_CHARACTER,
            story_context=[],
            current_game_state=GameState(),
            user_id="user-openclaw",
        )

    assert api_called["value"] is False
    assert "PROVIDER_SELECTION_SETTINGS_EXCEPTION" in caplog.text


def test_no_provider_swap_in_logs(monkeypatch, caplog):
    monkeypatch.setattr(llm_service, "get_user_settings", lambda user_id: None)

    selection = llm_service._select_provider_and_model("user-openclaw")

    assert selection.provider == constants.DEFAULT_LLM_PROVIDER
    assert selection.model == llm_service.DEFAULT_MODEL
    assert "falling back to default model" not in caplog.text
    assert "PROVIDER_SELECTION_SETTINGS_MISSING" in caplog.text
