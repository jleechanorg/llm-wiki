"""Performance tests for dynamic schema-to-prompt generation.

Tests verify that schema doc generation and injection meet latency targets:
- Schema doc generation at startup: <50ms per type, <500ms total for 10 types
- Prompt loading with injection: <5ms overhead vs baseline
- Server startup impact: <100ms added to initialization
"""

import unittest
import time
from mvp_site import agent_prompts
from mvp_site.schemas.prompt_generator import generate_type_markdown, get_schema_instructions


class TestSchemaPromptPerformance(unittest.TestCase):
    """Performance tests for schema documentation caching and injection."""

    def test_schema_doc_cache_initialization_latency(self):
        """Verify init_schema_doc_cache() completes within target time."""
        # Clear cache to simulate cold start
        agent_prompts._SCHEMA_DOC_CACHE.clear()

        start = time.perf_counter()
        timing_metrics = agent_prompts.init_schema_doc_cache()
        end = time.perf_counter()

        total_time_ms = (end - start) * 1000

        # Verify total time under target
        self.assertLess(
            total_time_ms,
            500.0,
            f"Schema cache init took {total_time_ms:.2f}ms, expected <500ms"
        )

        # Verify per-type times are reasonable
        for type_name, type_time_ms in timing_metrics.items():
            if type_name == "__total__":
                continue
            self.assertLess(
                type_time_ms,
                50.0,
                f"Schema doc generation for {type_name} took {type_time_ms:.2f}ms, expected <50ms"
            )

        # Verify cache was populated
        self.assertGreater(len(agent_prompts._SCHEMA_DOC_CACHE), 0)
        print(f"✅ Cache init: {total_time_ms:.2f}ms for {len(timing_metrics)-1} types")

    def test_cached_schema_doc_retrieval_fast(self):
        """Verify cached schema doc retrieval is fast (<1ms)."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        # Measure cache hits
        test_types = ["CombatantState", "CombatState", "EntityType"]

        for type_name in test_types:
            start = time.perf_counter()
            doc = agent_prompts.get_cached_schema_doc(type_name)
            end = time.perf_counter()

            retrieval_time_ms = (end - start) * 1000

            self.assertIsNotNone(doc, f"Cache miss for {type_name}")
            self.assertLess(
                retrieval_time_ms,
                1.0,
                f"Cache retrieval for {type_name} took {retrieval_time_ms:.2f}ms, expected <1ms"
            )

        print(f"✅ Cache retrieval: <1ms for {len(test_types)} types")

    def test_prompt_injection_overhead_acceptable(self):
        """Verify prompt injection adds <5ms overhead vs baseline."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        # Create test content with placeholders
        test_content = """# Test Prompt

## Combat State
{{SCHEMA:CombatState}}

## Combatant State
{{SCHEMA:CombatantState}}

## Entity Type
{{SCHEMA:EntityType}}
"""

        # Measure injection time
        start = time.perf_counter()
        injected = agent_prompts._inject_dynamic_schema_docs(test_content)
        end = time.perf_counter()

        injection_time_ms = (end - start) * 1000

        # Verify overhead is minimal
        self.assertLess(
            injection_time_ms,
            5.0,
            f"Schema injection took {injection_time_ms:.2f}ms, expected <5ms"
        )

        # Verify placeholders were replaced
        self.assertNotIn("{{SCHEMA:", injected)
        self.assertIn("combat_phase", injected)  # combat_phase is in CombatState
        self.assertIn("CombatantState", injected)

        print(f"✅ Injection overhead: {injection_time_ms:.2f}ms for 3 placeholders")

    def test_prompt_loading_with_injection_fast(self):
        """Verify full prompt loading with schema injection is fast."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        # Clear instruction cache to ensure cold-path measurement
        agent_prompts._loaded_instructions_cache.clear()

        # Measure loading combat_system_instruction.md (has schema placeholders)
        # Use the correct instruction type constant
        start = time.perf_counter()
        content = agent_prompts._load_instruction_file("combat")  # PROMPT_TYPE_COMBAT
        end = time.perf_counter()

        load_time_ms = (end - start) * 1000

        # Verify load time is reasonable (file I/O + injection)
        self.assertLess(
            load_time_ms,
            20.0,
            f"Prompt loading with injection took {load_time_ms:.2f}ms, expected <20ms"
        )

        # Verify schema docs were injected
        self.assertIn("combat_phase", content)  # combat_phase is in CombatState
        self.assertIn("CombatantState", content)
        self.assertNotIn("{{SCHEMA:", content)

        print(f"✅ Full prompt load: {load_time_ms:.2f}ms (file I/O + injection)")

    def test_cache_correctness_matches_on_demand_generation(self):
        """Verify cached schema docs match on-demand generated docs."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        test_types = ["CombatantState", "CombatState", "EntityType"]

        for type_name in test_types:
            cached_doc = agent_prompts.get_cached_schema_doc(type_name)
            on_demand_doc = get_schema_instructions(type_name, "game_state")

            self.assertEqual(
                cached_doc,
                on_demand_doc,
                f"Cached doc for {type_name} doesn't match on-demand generation"
            )

        print(f"✅ Cache correctness: Verified {len(test_types)} types match on-demand generation")

    def test_cache_hit_rate_for_common_types(self):
        """Verify high cache hit rate for commonly used schema types."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        common_types = [
            "CombatantState", "CombatPhase", "EntityType",
            "CampaignTier", "Character", "NPC"
        ]

        hits = 0
        for type_name in common_types:
            if agent_prompts.get_cached_schema_doc(type_name) is not None:
                hits += 1

        hit_rate = (hits / len(common_types)) * 100

        self.assertGreaterEqual(
            hit_rate,
            80.0,
            f"Cache hit rate {hit_rate:.1f}% below target 80%"
        )

        print(f"✅ Cache hit rate: {hit_rate:.1f}% ({hits}/{len(common_types)} types)")

    def test_unresolved_placeholder_uses_fallback_marker(self):
        """Verify unresolved placeholders are replaced with a visible marker."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        # Create content with invalid placeholder (type that doesn't exist)
        test_content = """# Test Prompt

## Invalid Type
{{SCHEMA:NonExistentType}}

This should fail.
"""

        injected = agent_prompts._inject_dynamic_schema_docs(test_content)

        self.assertIn("[UNRESOLVED_SCHEMA:NonExistentType]", injected)
        self.assertNotIn("{{SCHEMA:", injected)
        print("✅ Unresolved placeholder fallback marker works correctly")

    def test_unresolved_placeholder_raises_error_when_strict(self):
        """Verify strict mode still raises on unresolved placeholders."""
        # Ensure cache is populated
        if not agent_prompts._SCHEMA_DOC_CACHE:
            agent_prompts.init_schema_doc_cache()

        # Create content with invalid placeholder (type that doesn't exist)
        test_content = """# Test Prompt

## Invalid Type
{{SCHEMA:NonExistentType}}

This should fail in strict mode.
"""

        # Verify that strict mode raises ValueError for unresolved placeholder
        with self.assertRaises(ValueError) as context:
            agent_prompts._inject_dynamic_schema_docs(
                test_content, raise_on_unresolved=True
            )

        self.assertIn("NonExistentType", str(context.exception))
        print("✅ Strict unresolved placeholder detection working correctly")

    def test_generate_type_markdown_handles_allof_cycles(self):
        """Verify allOf cycles do not cause recursion errors."""
        type_name = "CyclicType"
        definitions = {}
        cyclic_definition = {
            "type": "object",
            "description": "Cycle test",
            "allOf": [{"$ref": "#/$defs/CyclicType"}],
            "properties": {"name": {"type": "string"}},
        }
        definitions[type_name] = cyclic_definition

        markdown = generate_type_markdown(type_name, cyclic_definition, definitions)

        self.assertIn("### CyclicType", markdown)
        self.assertIn("name", markdown)


if __name__ == "__main__":
    unittest.main()
