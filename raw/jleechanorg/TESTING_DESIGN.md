# Testing Design Document

**Project:** WorldArchitect.AI  
**Purpose:** Comprehensive test design for MCP, HTTP, and UI test suites  
**Date:** 2026-03-18

---

## Overview

This document defines the test design strategy for WorldArchitect.AI across three testing layers:

1. **MCP Tests** (`testing_mcp/`) - Protocol-level tests using the MCP client
2. **HTTP Tests** (`testing_http/`) - REST API tests using HTTP requests
3. **UI Tests** (`testing_ui/`) - Browser-based tests using Playwright

Each layer builds upon the base test classes and addresses core user flows identified from manual testing.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      UI Tests (Playwright)                      │
│            testing_ui/lib/browser_test_base.py                  │
├─────────────────────────────────────────────────────────────────┤
│                    HTTP Tests (requests)                        │
│              testing_http/lib/__init__.py                      │
├─────────────────────────────────────────────────────────────────┤
│                     MCP Tests (MCPClient)                       │
│            testing_mcp/lib/base_test.py                          │
├─────────────────────────────────────────────────────────────────┤
│                      WorldArchitect Backend                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Base Test Classes

### MCP Test Base (`testing_mcp/lib/base_test.py`)

The `MCPTestBase` class provides:
- Local MCP server lifecycle management
- `MCPClient` wrapper for protocol communication
- `TestContext` for state management across scenarios
- Evidence collection and bundling
- Streaming SSE event capture
- Campaign state helpers (`create_campaign`, `process_action`, etc.)

**Key Methods:**
- `start_server()` / `restart_server()` - Server lifecycle
- `run_scenarios(ctx: TestContext)` - Abstract method for test scenarios
- `ctx.create_campaign()` - Campaign creation helper
- `ctx.process_action()` - Send user input to campaign
- `ctx.collect_route_stream_events()` - Capture SSE streaming

### HTTP Test Base (`testing_http/lib/`)

The HTTP test utilities provide:
- `WAHttpTest` - Base class extending `testing_utils.http_test.HttpTestBase`
- Pre-configured test auth bypass headers
- Session management (`get_test_session()`)
- Test data fixtures (`CAMPAIGN_TEST_DATA`, `TEST_SCENARIOS`)
- Validation helpers (`validate_campaign_created_successfully()`, etc.)

**Key Components:**
- `WAHttpTest.BASE_URL` - Default `http://localhost:8086`
- `get_test_session()` - Authenticated requests session
- `make_authenticated_request()` - Helper for authenticated calls

### UI Test Base (`testing_ui/lib/browser_test_base.py`)

The `BrowserTestBase` class provides:
- Playwright browser automation
- Server lifecycle (`start_test_server()`)
- Firebase auth token generation
- Campaign/game helpers
- Screenshot utilities
- SSE event capture for streaming verification

**Key Features:**
- Automatic Firebase token creation for auth
- `wait_for_element()` / `click()` / `fill()` helpers
- Screenshot capture with `save_screenshot()`
- Video recording support
- Stream event collection for validation

---

## Core User Flows

### 1. Authentication

**Flow:** Google OAuth Login → Firebase Auth → Session Establishment

#### MCP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_google_oauth_flow` | Complete OAuth token exchange | Token contains correct `aud` claim |
| `test_test_auth_bypass` | Test mode auth bypass | Requests succeed without real auth |
| `test_token_refresh` | Firebase ID token refresh | New token obtained after expiry |

**Implementation Pattern:**
```python
class AuthTest(MCPTestBase):
    TEST_NAME = "auth_flow"
    MODEL = "gemini-3-flash-preview"
    
    def run_scenarios(self, ctx: TestContext) -> list[dict]:
        # Test auth bypass header
        headers = self._build_test_identity_headers()
        assert "X-Test-Bypass-Auth" in headers
        return [{"name": "auth_header", "passed": True}]
```

#### HTTP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_auth_endpoint_health` | Auth endpoint responds | 200 OK on `/health` |
| `test_session_cookie_set` | Session cookie after login | Set-Cookie header present |
| `test_invalid_token_rejected` | Invalid token rejected | 401 response |

#### UI Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_google_sign_in_button` | OAuth button visible | Button with `data-testid="google-sign-in"` |
| `test_oauth_redirect` | Redirect after OAuth | URL contains Firebase auth callback |
| `test_authenticated_state` | UI shows logged-in state | Avatar/profile visible |

---

### 2. Campaign Creation (3-Step Wizard)

**Flow:** Enter Title → Select Setting → Configure Characters → Launch

#### MCP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_campaign_wizard_complete` | Full 3-step wizard via MCP | Campaign created with all fields |
| `test_campaign_title_validation` | Empty title rejected | Error returned for blank title |
| `test_campaign_setting_options` | Setting selection works | Setting stored in campaign state |
| `test_campaign_presets` | Pre-built campaign presets | Campaign loads with preset data |

**Implementation Pattern:**
```python
class CampaignCreationTest(MCPTestBase):
    TEST_NAME = "campaign_creation"
    MODEL = "gemini-3-flash-preview"
    
    def run_scenarios(self, ctx: TestContext) -> list[dict]:
        # Step 1: Create campaign
        campaign_id = ctx.create_campaign(
            title="Test Campaign",
            setting="A roadside ambush outside Phandalin",
            character="Aric the Fighter (STR 16)"
        )
        
        # Verify campaign state
        state = ctx.get_campaign_state(campaign_id)
        campaign = state.get("campaign", {})
        
        results = [{
            "name": "campaign_created",
            "passed": campaign.get("title") == "Test Campaign",
            "campaign_id": campaign_id
        }]
        return results
```

#### HTTP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_campaign_create_api` | POST to campaign endpoint | 201 Created, campaign ID returned |
| `test_campaign_list_api` | GET campaign list | 200 OK, array of campaigns |
| `test_campaign_update_api` | PATCH campaign settings | Updates reflected in GET |
| `test_campaign_delete_api` | DELETE campaign | 204 No Content |

#### UI Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_wizard_step_1_title` | Title input accepts text | Input field functional |
| `test_wizard_step_2_setting` | Setting dropdown works | Options selectable |
| `test_wizard_step_3_character` | Character creation form | Character saved |
| `test_wizard_navigation` | Back/Next buttons work | State preserved across steps |
| `test_campaign_launch` | Launch button starts game | Redirect to gameplay |

---

### 3. Character Creation and Management

**Flow:** Select Race → Select Class → Assign Stats → Choose Background → Name Character

#### MCP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_character_creation_flow` | Full character creation | Character in game state |
| `test_character_stats_assignment` | Stat allocation | Stats stored correctly |
| `test_character_equipment` | Starting equipment selection | Equipment in character data |
| `test_character_level_up` | Level up mechanics | XP and level updated |
| `test_character_inventory` | Inventory management | Items tracked correctly |

**Implementation Pattern:**
```python
class CharacterManagementTest(MCPTestBase):
    TEST_NAME = "character_management"
    MODEL = "gemini-3-flash-preview"
    
    def run_scenarios(self, ctx: TestContext) -> list[dict]:
        campaign_id = ctx.create_campaign_and_start_story()
        
        # Complete character creation
        response = ctx.process_action(
            campaign_id,
            "My character is Elara, a Level 1 Half-Elf Ranger."
        )
        
        # Verify character in state
        game_state = ctx.get_game_state(campaign_id)
        pc_data = game_state.get("pc_data", {})
        
        return [{
            "name": "character_created",
            "passed": bool(pc_data.get("name")),
            "campaign_id": campaign_id
        }]
```

#### HTTP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_character_api_create` | POST new character | 201, character data returned |
| `test_character_api_get` | GET character details | Character data matches |
| `test_character_api_update` | PATCH character | Updates persisted |
| `test_character_api_delete` | DELETE character | 204, character removed |

#### UI Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_race_selection` | Race dropdown functional | Selection persists |
| `test_class_selection` | Class selection works | Class displayed |
| `test_stats_roll` | Roll stats button | Random values generated |
| `test_character_name_input` | Name field accepts input | Name saved |
| `test_character_sheet_display` | Character sheet renders | All fields visible |

---

### 4. Story/World Interactions (Chat, Streaming)

**Flow:** User Input → LLM Processing → Streaming Response → State Update

#### MCP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_chat_basic` | Basic user message | Response contains narrative |
| `test_streaming_response` | SSE streaming works | Multiple chunks received |
| `test_stream_chunk_ordering` | Chunk sequence valid | Sequence numbers increment |
| `test_combat_round` | Combat mechanics | Dice rolls, damage applied |
| `test_npc_interaction` | NPC dialogue | NPC responds appropriately |
| `test_world_state_changes` | World state updates | Changes persist after response |

**Key Validation:**
- `ctx.collect_route_stream_events()` - Captures SSE chunks
- `validate_timed_chunks()` - Validates timestamp ordering
- Done payload contains `structured_response` and `chunk_count`

```python
class StoryInteractionTest(MCPTestBase):
    TEST_NAME = "story_interaction"
    MODEL = "gemini-3-flash-preview"
    
    def run_scenarios(self, ctx: TestContext) -> list[dict]:
        campaign_id = ctx.create_campaign_and_start_story()
        
        # Test streaming response
        passed, errors, details, mode_details, events, done = \
            ctx.collect_streaming_mode_contract(
                campaign_id=campaign_id,
                mode="character",
                user_input="I look around the room",
                user_email=self.test_user_email,
                min_chunks=2
            )
        
        return [{
            "name": "streaming_response",
            "passed": passed,
            "errors": errors,
            "campaign_id": campaign_id,
            "chunk_count": details.get("chunk_count_observed")
        }]
```

#### HTTP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_interaction_api` | POST user input | 200, response returned |
| `test_streaming_endpoint` | SSE endpoint works | EventStream content-type |
| `test_interaction_timeout` | Long response timeout | Timeout handled gracefully |

#### UI Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_chat_input_sends` | Enter key sends message | Message appears in chat |
| `test_streaming_display` | Response streams to UI | Text appears incrementally |
| `test_response_complete` | Done state indicated | "Generating..." clears |
| `test_chat_history` | History scroll works | Previous messages visible |

---

### 5. Save/Load Functionality

**Flow:** Save Trigger → State Serialization → Storage → Load → State Restoration

#### MCP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_campaign_save` | Save campaign state | State persisted to Firestore |
| `test_campaign_load` | Load saved campaign | State restored correctly |
| `test_save_after_changes` | Save with modifications | Changes preserved |
| `test_multi_slot_save` | Multiple save slots | Slots independent |
| `test_cloud_sync` | Cloud save/load | Cross-session persistence |

**Implementation Pattern:**
```python
class SaveLoadTest(MCPTestBase):
    TEST_NAME = "save_load"
    MODEL = "gemini-3-flash-preview"
    
    def run_scenarios(self, ctx: TestContext) -> list[dict]:
        campaign_id = ctx.create_campaign_and_start_story()
        
        # Make changes
        ctx.process_action(campaign_id, "I search the room")
        
        # Save campaign (via MCP tool)
        save_result = ctx.client.tools_call(
            "save_campaign",
            {"user_id": ctx.user_id, "campaign_id": campaign_id}
        )
        
        # Create new campaign and load
        new_campaign_id = ctx.create_campaign()
        load_result = ctx.client.tools_call(
            "load_campaign",
            {
                "user_id": ctx.user_id,
                "campaign_id": new_campaign_id,
                "source_campaign_id": campaign_id
            }
        )
        
        return [{
            "name": "save_load",
            "passed": load_result.get("success"),
            "campaign_id": new_campaign_id
        }]
```

#### HTTP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_save_endpoint` | POST save endpoint | 200, save confirmation |
| `test_load_endpoint` | GET load endpoint | 200, campaign data |
| `test_save_not_found` | Load non-existent save | 404 response |

#### UI Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_save_button` | Save button triggers save | Toast/confirmation shown |
| `test_load_menu` | Load menu displays saves | Slots visible |
| `test_autosave_indicator` | Autosave works | Indicator updates |

---

### 6. Settings/Profile Management

**Flow:** Access Settings → Modify Preferences → Save → Changes Applied

#### MCP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_update_model_settings` | Change LLM model | Setting persisted |
| `test_update_preferences` | Update user preferences | Preferences in user data |
| `test_difficulty_setting` | Change game difficulty | Difficulty affects gameplay |

```python
class SettingsTest(MCPTestBase):
    TEST_NAME = "settings"
    MODEL = "gemini-3-flash-preview"
    HAS_LLM_CALLS = False  # No LLM needed for settings tests
    
    def run_scenarios(self, ctx: TestContext) -> list[dict]:
        # Update settings via MCP
        result = ctx.client.tools_call(
            "update_user_settings",
            {
                "user_id": ctx.user_id,
                "settings": {"llm_provider": "gemini", "model": "gemini-2-flash"}
            }
        )
        
        # Verify settings applied
        user_data = ctx.client.tools_call(
            "get_user_data",
            {"user_id": ctx.user_id}
        )
        
        return [{
            "name": "settings_updated",
            "passed": user_data.get("settings", {}).get("model") == "gemini-2-flash"
        }]
```

#### HTTP Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_settings_api_get` | GET user settings | 200, settings JSON |
| `test_settings_api_update` | PATCH settings | Updates persisted |
| `test_profile_api` | Profile CRUD | All endpoints functional |

#### UI Tests

| Test Case | Description | Validation |
|-----------|-------------|------------|
| `test_settings_page_loads` | Settings accessible | Page renders |
| `test_model_selector` | Model dropdown works | Selection saved |
| `test_profile_update` | Update display name | Name updated in header |
| `test_logout` | Logout clears session | Redirect to login |

---

## Test Data Management

### Test Fixtures

Each test layer should leverage shared fixtures from `testing_http/lib/test_data.py`:

```python
# Shared test data
CAMPAIGN_TEST_DATA = {
    "default_title": "Test Adventure",
    "default_setting": "Tavern",
    "sample_characters": [...]
}

TEST_SCENARIOS = [
    {"name": "combat", "input": "I attack the goblin"},
    {"name": "exploration", "input": "I search the room"},
    ...
]
```

### Test Users

- **MCP Tests:** Use `MCP_TEST_USER_ID` or generated `test-{name}-{timestamp}`
- **HTTP Tests:** Default `test-http-user`
- **UI Tests:** Firebase test auth or real test account

---

## Evidence Collection

### MCP Test Evidence

The `MCPTestBase` automatically collects:
- Server logs (`server.log`)
- MCP request/response captures
- LLM HTTP traces (when enabled)
- Campaign state snapshots
- Streaming event logs

Evidence directory: `/tmp/worldarchitectai/{branch}/{test_name}/`

### HTTP Test Evidence

- Request/response logs
- Screenshot on failure
- Response time metrics

### UI Test Evidence

- Screenshots (pass/fail)
- Video recordings (optional)
- Console logs
- Network traces

---

## Running the Tests

### MCP Tests
```bash
cd testing_mcp
python -m lib.base_test --model gemini-3-flash-preview
```

### HTTP Tests
```bash
cd testing_http
python -m lib.http_test
```

### UI Tests
```bash
cd testing_ui
python -m lib.browser_test
# or
playwright test
```

---

## Best Practices

1. **Use base classes** - Extend `MCPTestBase`, `WAHttpTest`, `BrowserTestBase`
2. **Isolate state** - Each test should create its own campaign/character
3. **Validate streaming** - Use `collect_streaming_mode_contract()` for SSE tests
4. **Capture evidence** - Save screenshots/state on failure
5. **Use test fixtures** - Reuse `CAMPAIGN_TEST_DATA` for consistency
6. **Mark LLM dependency** - Set `HAS_LLM_CALLS = False` for config-only tests
7. **Parallel safely** - Use unique user IDs per worker

---

## Appendix: Class Reference

### MCPTestBase

| Attribute | Type | Description |
|-----------|------|-------------|
| `TEST_NAME` | str | Test identifier for evidence |
| `MODEL` | str | Default LLM model |
| `HAS_LLM_CALLS` | bool | Whether test uses LLM |
| `DEFAULT_LOCAL_TIMEOUT_S` | int | MCP call timeout (180s) |
| `DEFAULT_TEST_TIMEOUT` | int | Total test timeout (600s) |

### TestContext

| Method | Description |
|--------|-------------|
| `create_campaign()` | Create new campaign |
| `process_action()` | Send user input |
| `get_campaign_state()` | Fetch campaign state |
| `get_game_state()` | Fetch game_state section |
| `collect_streaming_mode_contract()` | Full streaming validation |

### WAHttpTest

| Attribute | Default |
|-----------|---------|
| `BASE_URL` | `http://localhost:8086` |
| `TEST_BYPASS_AUTH` | `True` |
| `TEST_USER_ID` | `test-http-user` |

### BrowserTestBase

| Method | Description |
|--------|-------------|
| `start_browser()` | Initialize Playwright |
| `navigate_to()` | Go to URL |
| `click()` | Click element |
| `fill()` | Input text |
| `save_screenshot()` | Capture screenshot |
| `wait_for_stream_complete()` | Wait for SSE done |
