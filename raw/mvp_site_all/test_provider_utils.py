from __future__ import annotations

import json

from mvp_site.llm_providers.provider_utils import (
    build_tool_results_prompt,
    execute_openai_tool_calls,
    extract_json_payload_and_tool_requests,
    inject_tool_requests_if_missing,
    run_json_first_tool_requests_flow,
    run_openai_json_first_tool_requests_flow,
    run_openai_native_two_phase_flow,
    stringify_chat_parts,
)


def test_execute_openai_tool_calls():
    calls: list[tuple[str, dict]] = []

    def executor(name: str, args: dict) -> dict:
        calls.append((name, args))
        return {"ok": True, "name": name, "args": args}

    tool_calls = [
        {
            "id": "call_1",
            "type": "function",
            "function": {"name": "roll_dice", "arguments": '{"notation":"1d20+5"}'},
        }
    ]

    results = execute_openai_tool_calls(
        tool_calls, execute_tool_fn=executor, logger=None
    )
    assert len(results) == 1
    assert results[0]["tool_call_id"] == "call_1"
    assert results[0]["tool"] == "roll_dice"
    assert results[0]["args"]["notation"] == "1d20+5"
    assert calls[0][0] == "roll_dice"


def test_run_openai_json_first_tool_requests_flow_runs_phase2():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    calls: list[dict] = []

    def gen(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return Resp(
                '{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}'
            )
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    def exec_tool_requests(tool_requests):
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_openai_json_first_tool_requests_flow(
        generate_content_fn=gen,
        prompt_contents=["hi"],
        model_name="m",
        system_instruction_text="sys",
        temperature=0.0,
        max_output_tokens=10,
        provider_no_tool_requests_log_prefix="X",
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        logger=Logger(),
    )
    assert out.text == '{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}'
    assert len(calls) == 3
    phase2_messages = calls[1].get("messages", [])
    assert phase2_messages, "Phase 2 should pass messages"
    assert "Tool results" in phase2_messages[-1]["content"]


def test_run_json_first_tool_requests_flow_runs_phase2():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase2_calls: list[object] = []

    def phase1():
        return Resp(
            '{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}'
        )

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(tool_requests):
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        return {
            "prompt_contents": prompt_contents,
            "phase1_text": phase1_text,
            "tool_results_prompt": tool_results_prompt,
        }

    def phase2(history):
        phase2_calls.append(history)
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
    )

    assert out.text == '{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}'
    assert len(phase2_calls) == 2
    history = phase2_calls[0]
    assert history["prompt_contents"] == ["hi"]
    assert "Tool results" in history["tool_results_prompt"]


def test_run_json_first_tool_requests_flow_returns_phase1_for_wrapped_json_text():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase2_calls: list[object] = []

    def phase1():
        return Resp(
            """```json
{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}
```"""
        )

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(tool_requests):
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        return {
            "prompt_contents": prompt_contents,
            "phase1_text": phase1_text,
            "tool_results_prompt": tool_results_prompt,
        }

    def phase2(history):
        phase2_calls.append(history)
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
    )

    assert out.text.startswith("```json")
    assert len(phase2_calls) == 0


def test_run_json_first_tool_requests_flow_decodes_json_string_response():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase2_calls: list[object] = []

    inner = '{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}'

    def phase1():
        return Resp(json.dumps(inner))

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(tool_requests):
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        return {
            "prompt_contents": prompt_contents,
            "phase1_text": phase1_text,
            "tool_results_prompt": tool_results_prompt,
        }

    def phase2(history):
        phase2_calls.append(history)
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
    )

    assert out.text == '{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}'
    assert len(phase2_calls) == 2
    assert phase2_calls[0]["phase1_text"] == inner


def test_inject_tool_requests_if_missing_handles_response_text_getter_error():
    class Resp:
        def __init__(self):
            self._stored_text = None

        @property
        def text(self):
            raise ValueError("text getter failed")

        @text.setter
        def text(self, value):
            self._stored_text = value

    response = Resp()
    expected_tool_requests = [{"tool": "faction_calculate_power", "args": {}}]

    inject_tool_requests_if_missing(
        response, expected_tool_requests=expected_tool_requests
    )

    assert response._stored_text is not None
    parsed = json.loads(response._stored_text)
    assert parsed["tool_requests"] == expected_tool_requests


def test_extract_json_payload_and_tool_requests_supports_top_level_list():
    response_data, tool_requests = extract_json_payload_and_tool_requests(
        '[{"tool":"faction_calculate_power","args":{"soldiers":10}}]'
    )

    assert response_data == {}
    assert tool_requests == [
        {"tool": "faction_calculate_power", "args": {"soldiers": 10}}
    ]


def test_run_json_first_tool_requests_flow_retries_phase2_when_dice_rolls_missing():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase2_calls: list[object] = []

    def phase1():
        return Resp(
            '{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}'
        )

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(tool_requests):
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"notation": "1d20", "rolls": [7], "modifier": 0, "total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        return {
            "prompt_contents": prompt_contents,
            "phase1_text": phase1_text,
            "tool_results_prompt": tool_results_prompt,
        }

    def phase2(history):
        phase2_calls.append(history)
        if len(phase2_calls) == 1:
            # Missing dice_rolls despite tool injection
            return Resp('{"narrative":"ok","dice_rolls":[]}')
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
    )

    assert out.text == '{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}'
    assert len(phase2_calls) == 2
    assert "IMPORTANT:" in phase2_calls[1]["tool_results_prompt"]


def test_run_json_first_tool_requests_flow_retries_phase2_when_phase2_invalid_json():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase2_calls: list[object] = []
    tool_exec_calls: list[list[dict]] = []

    def phase1():
        return Resp(
            '{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}'
        )

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(tool_requests):
        tool_exec_calls.append(tool_requests)
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"notation": "1d20", "rolls": [7], "modifier": 0, "total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        return {
            "prompt_contents": prompt_contents,
            "phase1_text": phase1_text,
            "tool_results_prompt": tool_results_prompt,
        }

    def phase2(history):
        phase2_calls.append(history)
        if len(phase2_calls) == 1:
            # Malformed JSON (truncated)
            return Resp('{"narrative":"ok"')
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
    )

    assert out.text == '{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}'
    assert len(tool_exec_calls) == 1, "Tools must only execute once (no rerolls)"
    assert len(phase2_calls) == 2
    assert "malformed JSON" in phase2_calls[1]["tool_results_prompt"]


def test_run_json_first_tool_requests_flow_returns_phase1_when_no_tools():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase2_calls: list[object] = []

    def phase1():
        return Resp('{"narrative":"ok"}')

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(_tool_requests):
        raise AssertionError("should not execute tools")

    def format_results(_results):
        raise AssertionError("should not format results")

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        raise AssertionError("should not build history")

    def phase2(history):
        phase2_calls.append(history)
        return Resp('{"narrative":"phase2"}')

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
    )

    assert out.text == '{"narrative":"ok"}'
    assert phase2_calls == []


def test_run_json_first_tool_requests_flow_retries_phase1_invalid_json():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase1_calls = {"count": 0}
    phase2_calls: list[object] = []

    def phase1():
        phase1_calls["count"] += 1
        if phase1_calls["count"] == 1:
            return Resp("not-json")
        return Resp('{"narrative":"ok"}')

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(_tool_requests):
        raise AssertionError("should not execute tools")

    def format_results(_results):
        raise AssertionError("should not format results")

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        raise AssertionError("should not build history")

    def phase2(history):
        phase2_calls.append(history)
        return Resp('{"narrative":"phase2"}')

    class Logger:
        def info(self, _m, *args): ...

        def warning(self, _m, *args): ...

        def debug(self, _m, *args): ...

        def error(self, _m, *args): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
        phase1_invalid_json_retries=1,
    )

    assert out.text == '{"narrative":"ok"}'
    assert phase1_calls["count"] == 2
    assert phase2_calls == []


def test_run_json_first_tool_requests_flow_extracts_embedded_json_without_retry():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase1_calls = {"count": 0}
    phase2_calls: list[object] = []

    def phase1():
        phase1_calls["count"] += 1
        return Resp(
            '[Mode: Story-Mode]\n{"tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}'
        )

    def extract_text(resp: Resp) -> str:
        return resp.text

    def exec_tool_requests(tool_requests):
        return [
            {
                "tool": tool_requests[0]["tool"],
                "args": tool_requests[0]["args"],
                "result": {"total": 7},
            }
        ]

    def format_results(_results):
        return "- roll_dice: total=7"

    def build_history(*, prompt_contents, phase1_text, tool_results_prompt):
        return {
            "prompt_contents": prompt_contents,
            "phase1_text": phase1_text,
            "tool_results_prompt": tool_results_prompt,
        }

    def phase2(history):
        phase2_calls.append(history)
        return Resp('{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}')

    class Logger:
        def info(self, _m, *args): ...

        def warning(self, _m, *args): ...

        def debug(self, _m, *args): ...

        def error(self, _m, *args): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=exec_tool_requests,
        format_tool_results_text_fn=format_results,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
        phase1_invalid_json_retries=3,
    )

    assert out.text == '{"narrative":"ok","dice_rolls":["Roll: 1d20 = 7"]}'
    assert phase1_calls["count"] == 1
    assert len(phase2_calls) == 2
    assert phase2_calls[0]["phase1_text"].startswith("[Mode: Story-Mode]")


def test_run_json_first_tool_requests_flow_returns_phase1_after_retry_exhausted():
    class Resp:
        def __init__(self, text: str):
            self.text = text

    phase1_calls = {"count": 0}

    def phase1():
        phase1_calls["count"] += 1
        return Resp("not-json")

    def extract_text(resp: Resp) -> str:
        return resp.text

    class Logger:
        def info(self, _m, *args): ...

        def warning(self, _m, *args): ...

        def debug(self, _m, *args): ...

        def error(self, _m, *args): ...

    out = run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=["hi"],
        execute_tool_requests_fn=lambda _tr: [],
        format_tool_results_text_fn=lambda _r: "",
        build_history_fn=lambda **_k: {},
        phase2_generate_fn=lambda _h: Resp('{"narrative":"phase2"}'),
        logger=Logger(),
        no_tool_requests_log_msg="no tool requests",
        phase1_invalid_json_retries=1,
    )

    assert out.text == "not-json"
    assert phase1_calls["count"] == 2


def test_run_openai_native_two_phase_flow_injects_tool_messages():
    class Resp:
        def __init__(self, text: str, tool_calls=None):
            self.text = text
            self._tool_calls = tool_calls

        @property
        def tool_calls(self):
            return self._tool_calls

    calls: list[dict] = []

    tool_calls = [
        {
            "id": "call_1",
            "type": "function",
            "function": {"name": "roll_dice", "arguments": '{"notation":"1d20"}'},
        }
    ]

    def gen(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return Resp("", tool_calls=tool_calls)
        return Resp('{"narrative":"ok"}', tool_calls=None)

    def exec_tool(name: str, args: dict):
        return {"tool": name, "args": args, "total": 3}

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    out = run_openai_native_two_phase_flow(
        generate_content_fn=gen,
        prompt_contents=["hi"],
        model_name="m",
        system_instruction_text="sys",
        temperature=0.0,
        max_output_tokens=10,
        dice_roll_tools=[{"function": {"name": "roll_dice"}}],
        execute_tool_fn=exec_tool,
        logger=Logger(),
    )
    assert out.text == '{"narrative":"ok"}'
    assert len(calls) == 2
    phase2_messages = calls[1].get("messages", [])
    assert any(m.get("role") == "tool" for m in phase2_messages)
    tool_msgs = [m for m in phase2_messages if m.get("role") == "tool"]
    assert tool_msgs[0]["tool_call_id"] == "call_1"


def test_run_openai_native_two_phase_flow_requests_action_resolution_dice():
    class Resp:
        def __init__(self, text: str, tool_calls=None):
            self.text = text
            self._tool_calls = tool_calls

        @property
        def tool_calls(self):
            return self._tool_calls

    calls: list[dict] = []

    tool_calls = [
        {
            "id": "call_1",
            "type": "function",
            "function": {"name": "roll_dice", "arguments": '{"notation":"1d20"}'},
        }
    ]

    def gen(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return Resp("", tool_calls=tool_calls)
        return Resp('{"narrative":"ok"}', tool_calls=None)

    def exec_tool(name: str, args: dict):
        return {"tool": name, "args": args, "total": 3}

    class Logger:
        def info(self, _m): ...

        def warning(self, _m): ...

        def debug(self, _m): ...

        def error(self, _m): ...

    _ = run_openai_native_two_phase_flow(
        generate_content_fn=gen,
        prompt_contents=["hi"],
        model_name="m",
        system_instruction_text="sys",
        temperature=0.0,
        max_output_tokens=10,
        dice_roll_tools=[{"function": {"name": "roll_dice"}}],
        execute_tool_fn=exec_tool,
        logger=Logger(),
    )

    phase2_messages = calls[1].get("messages", [])
    final_user_msg = [m for m in phase2_messages if m.get("role") == "user"][-1][
        "content"
    ]
    assert "action_resolution.mechanics" in final_user_msg
    assert "Do NOT populate dice_rolls" in final_user_msg


def test_stringify_chat_parts():
    assert stringify_chat_parts([]) == ""
    assert stringify_chat_parts(["a", "b"]) == "a\n\nb"
    text = stringify_chat_parts([{"x": 1}])
    assert '"x"' in text


def test_build_tool_results_prompt():
    base = build_tool_results_prompt('- roll_dice({}): {"total": 1}')
    assert "Tool results" in base
    assert "Do NOT include tool_requests" in base
    assert "action_resolution.mechanics" in base
    assert "dice_rolls array" not in base
    assert "Do NOT populate dice_rolls" in base

    with_extra = build_tool_results_prompt("X", extra_instructions="EXTRA")
    assert "EXTRA" in with_extra
