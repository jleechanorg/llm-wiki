import types

import pytest

from mvp_site.llm_providers import openrouter_provider
from mvp_site.llm_providers import openai_chat_common


class DummyResponse:
    def __init__(self, payload: dict):
        self._payload = payload
        self.status_code = 200
        self.ok = True

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


class DummyStreamResponse:
    def __init__(self, lines: list[str], status_code: int = 200, ok: bool = True):
        self._lines = lines
        self.status_code = status_code
        self.ok = ok
        self.closed = False

    def iter_lines(self, decode_unicode=True):
        del decode_unicode
        for line in self._lines:
            yield line

    def raise_for_status(self):
        return None

    def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")


def test_builds_openrouter_payload(monkeypatch):
    captured = {}

    def fake_post(url, json=None, headers=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        return DummyResponse(
            {"choices": [{"message": {"content": '{"narrative": "ok"}'}}]}
        )

    monkeypatch.setattr(
        openai_chat_common, "requests", types.SimpleNamespace(post=fake_post)
    )

    response = openrouter_provider.generate_content(
        prompt_contents=["first", "second"],
        model_name="meta-llama/llama-3.1-70b-instruct",
        system_instruction_text="system rules",
        temperature=0.4,
        max_output_tokens=400,
    )

    assert captured["url"] == openrouter_provider.OPENROUTER_URL
    assert captured["json"]["model"] == "meta-llama/llama-3.1-70b-instruct"
    assert captured["json"]["messages"][0]["role"] == "system"
    assert captured["json"]["messages"][1]["content"]
    assert captured["json"]["response_format"]["type"] == "json_object"
    assert response.text == '{"narrative": "ok"}'


def test_openrouter_missing_api_key(monkeypatch):
    """Test that ValueError is raised when OPENROUTER_API_KEY is missing."""
    # Ensure environment variable is unset
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(
        ValueError, match="CRITICAL: OPENROUTER_API_KEY environment variable not found"
    ):
        openrouter_provider.generate_content(
            prompt_contents=["test"],
            model_name="test-model",
            system_instruction_text="system",
            temperature=0.7,
            max_output_tokens=100,
            api_key=None,  # Explicitly None
        )


def test_generate_content_stream_sync_parses_sse_chunks(monkeypatch):
    captured = {}
    dummy_response = DummyStreamResponse(
        lines=[
            'data: {"choices":[{"delta":{"content":"Hello"}}]}',
            'data: {"choices":[{"delta":{"content":" world"}}]}',
            "data: [DONE]",
        ]
    )

    def fake_post(url, json=None, headers=None, timeout=None, stream=None):
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        captured["timeout"] = timeout
        captured["stream"] = stream
        return dummy_response

    monkeypatch.setattr(
        openrouter_provider, "requests", types.SimpleNamespace(post=fake_post)
    )

    chunks = list(
        openrouter_provider.generate_content_stream_sync(
            prompt_contents=["player action"],
            model_name="x-ai/grok-4.1-fast",
            system_instruction_text="system",
            temperature=0.5,
            max_output_tokens=512,
            json_mode=True,
        )
    )

    assert chunks == ["Hello", " world"]
    assert captured["url"] == openrouter_provider.OPENROUTER_URL
    assert captured["json"]["stream"] is True
    assert captured["stream"] is True
    assert dummy_response.closed is True


def test_generate_content_stream_sync_preserves_system_instruction_with_messages(monkeypatch):
    """Verify that system_instruction_text is prepended when messages are pre-built."""
    captured = {}
    dummy_response = DummyStreamResponse(
        lines=[
            'data: {"choices":[{"delta":{"content":"Test"}}]}',
            "data: [DONE]",
        ]
    )

    def fake_post(url, json=None, headers=None, timeout=None, stream=None):
        captured["json"] = json
        return dummy_response

    monkeypatch.setattr(
        openrouter_provider, "requests", types.SimpleNamespace(post=fake_post)
    )

    pre_built_messages = [
        {"role": "user", "content": "First prompt"},
        {"role": "assistant", "content": "First response"},
        {"role": "user", "content": "Tool results: dice rolled 15"},
    ]

    list(
        openrouter_provider.generate_content_stream_sync(
            prompt_contents=[],
            model_name="x-ai/grok-4.1-fast",
            system_instruction_text="Critical game rules and context",
            temperature=0.5,
            max_output_tokens=512,
            json_mode=True,
            messages=pre_built_messages,
        )
    )

    messages_sent = captured["json"]["messages"]
    assert messages_sent[0]["role"] == "system"
    assert messages_sent[0]["content"] == "Critical game rules and context"
    assert len(messages_sent) == 4
    assert messages_sent[1] == pre_built_messages[0]
    assert messages_sent[2] == pre_built_messages[1]
    assert messages_sent[3] == pre_built_messages[2]


def test_generate_content_stream_sync_no_response_format_for_unsupported_models(monkeypatch):
    """Regression: non-schema-support models must NOT send response_format in streaming.

    Llama 3.1 70B (and similar) return a bare JSON array like [4214.03] instead of
    a narrative dict when response_format=json_object is combined with stream=True.
    The streaming path must omit response_format for those models and rely on the
    system-prompt JSON instructions instead.
    """
    captured = {}
    dummy_response = DummyStreamResponse(
        lines=[
            'data: {"choices":[{"delta":{"content":"{}"}}]}',
            "data: [DONE]",
        ]
    )

    def fake_post(url, json=None, headers=None, timeout=None, stream=None):
        captured["json"] = json
        return dummy_response

    monkeypatch.setattr(
        openrouter_provider, "requests", types.SimpleNamespace(post=fake_post)
    )

    list(
        openrouter_provider.generate_content_stream_sync(
            prompt_contents=["player action"],
            model_name="meta-llama/llama-3.1-70b-instruct",
            system_instruction_text="system",
            temperature=0.5,
            max_output_tokens=512,
            json_mode=True,
        )
    )

    # response_format must be absent (or None) for non-schema-support models in streaming.
    assert captured["json"].get("response_format") is None


def test_generate_content_stream_sync_response_format_for_schema_models(monkeypatch):
    """Schema-support models (e.g. Grok) must still send response_format in streaming."""
    captured = {}
    dummy_response = DummyStreamResponse(
        lines=[
            'data: {"choices":[{"delta":{"content":"{}"}}]}',
            "data: [DONE]",
        ]
    )

    def fake_post(url, json=None, headers=None, timeout=None, stream=None):
        captured["json"] = json
        return dummy_response

    monkeypatch.setattr(
        openrouter_provider, "requests", types.SimpleNamespace(post=fake_post)
    )

    list(
        openrouter_provider.generate_content_stream_sync(
            prompt_contents=["player action"],
            model_name="x-ai/grok-4.1-fast",
            system_instruction_text="system",
            temperature=0.5,
            max_output_tokens=512,
            json_mode=True,
        )
    )

    assert captured["json"].get("response_format") is not None
    assert captured["json"]["response_format"].get("type") == "json_schema"
