"""Fixture-driven routing and modal invariants for agent selection."""

import json
from pathlib import Path
from types import SimpleNamespace

from mvp_site import agents, world_logic
from mvp_site.tests.test_modal_base import ModalTestBase

_FIXTURE_PATH = Path(__file__).parent / "data" / "modal_routing_fixtures.json"
_MODAL_AGENT_BY_NAME = {
    "LevelUpAgent": agents.LevelUpAgent,
    "CharacterCreationAgent": agents.CharacterCreationAgent,
}


class TestModalRoutingFixtures(ModalTestBase):
    """Machine-checkable fixture scenarios for routing/modal behavior."""

    @classmethod
    def setUpClass(cls):
        payload = json.loads(_FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.scenarios = payload.get("scenarios", [])

    def _mock_game_state(self, state: dict):
        custom_campaign_state = state.get("custom_campaign_state", {})
        rewards_pending = state.get("rewards_pending", {})
        player_character_data = state.get("player_character_data", {})
        return SimpleNamespace(
            custom_campaign_state=custom_campaign_state,
            rewards_pending=rewards_pending,
            player_character_data=player_character_data,
            campaign={
                "custom_campaign_state": custom_campaign_state,
                "campaign_version": 2,
            },
            in_combat=False,
            is_campaign_upgrade_available=lambda: False,
            get_character=lambda: player_character_data,
        )

    def test_fixture_scenarios(self):
        self.assertGreater(len(self.scenarios), 0, "Expected non-empty modal fixture set")

        for scenario in self.scenarios:
            with self.subTest(scenario=scenario.get("name")):
                state_kwargs = scenario["state"]
                full_state = self.create_base_state(
                    character_level=state_kwargs.get("character_level", 1),
                    character_xp=state_kwargs.get("character_xp", 0),
                    custom_campaign_state=state_kwargs.get("custom_campaign_state"),
                    rewards_pending=state_kwargs.get("rewards_pending"),
                )
                mock_game_state = self._mock_game_state(full_state)
                agent, metadata = agents.get_agent_for_input(
                    scenario["user_input"],
                    mock_game_state,
                )
                expect = scenario["expect"]

                # Invariant: routing and finish-choice injection must agree.
                routing_modal_active = isinstance(
                    agent,
                    (agents.LevelUpAgent, agents.CharacterCreationAgent),
                )
                planning_block = {
                    "thinking": "fixture-check",
                    "choices": {"explore": {"text": "Explore"}},
                }
                injected = world_logic._inject_modal_finish_choice_if_needed(
                    planning_block,
                    {
                        "custom_campaign_state": mock_game_state.custom_campaign_state,
                        "rewards_pending": mock_game_state.rewards_pending,
                        "player_character_data": mock_game_state.player_character_data,
                    },
                )
                choices = (injected or {}).get("choices", {}) if isinstance(injected, dict) else {}
                if isinstance(choices, dict):
                    injection_modal_active = (
                        "finish_character_creation_start_game" in choices
                        or "finish_level_up_return_to_game" in choices
                    )
                elif isinstance(choices, list):
                    choice_ids = {
                        choice.get("id")
                        for choice in choices
                        if isinstance(choice, dict)
                    }
                    injection_modal_active = (
                        "finish_character_creation_start_game" in choice_ids
                        or "finish_level_up_return_to_game" in choice_ids
                    )
                else:
                    injection_modal_active = False

                self.assertEqual(
                    routing_modal_active,
                    injection_modal_active,
                    (
                        f"Routing/injection invariant failed for scenario "
                        f"{scenario.get('name')}: {scenario.get('description')} "
                        f"routing_modal_active={routing_modal_active}, "
                        f"injection_modal_active={injection_modal_active}"
                    ),
                )

                modal_active = routing_modal_active
                self.assertEqual(
                    modal_active,
                    expect["modal_active"],
                    (
                        f"Scenario {scenario.get('name')} expected modal_active="
                        f"{expect['modal_active']} but got {type(agent).__name__}"
                    ),
                )

                modal_agent_name = expect.get("modal_agent")
                if modal_agent_name:
                    expected_cls = _MODAL_AGENT_BY_NAME[modal_agent_name]
                    self.assertIsInstance(
                        agent,
                        expected_cls,
                        (
                            f"Scenario {scenario.get('name')} expected "
                            f"{modal_agent_name} but got {type(agent).__name__}"
                        ),
                    )

                expected_priority = expect.get("routing_priority")
                if expected_priority:
                    self.assertEqual(
                        metadata.get("routing_priority"),
                        expected_priority,
                        (
                            f"Scenario {scenario.get('name')} expected routing_priority "
                            f"{expected_priority} but got {metadata.get('routing_priority')}"
                        ),
                    )
