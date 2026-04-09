"""
Utilities for generating LLM instructions and documentation from JSON Schemas.
(ADR-0003 Phase 4, Commit 10).
"""

from typing import Any

from mvp_site.schemas.validation import load_schema


def _gather_properties(
    schema_part: dict[str, Any],
    definitions: dict[str, Any],
    visited: set[int] | None = None,
) -> dict[str, Any]:
    """Recursively gather all properties from a schema fragment, resolving allOf/refs."""
    if visited is None:
        visited = set()
    schema_id = id(schema_part)
    if schema_id in visited:
        return {}
    visited.add(schema_id)
    props: dict[str, Any] = {}
    for sub_schema in schema_part.get("allOf", []):
        resolved = resolve_refs(sub_schema, definitions) if definitions else sub_schema
        props.update(_gather_properties(resolved, definitions, visited))
    props.update(schema_part.get("properties", {}))
    visited.remove(schema_id)
    return props


def resolve_refs(schema: dict[str, Any], definitions: dict[str, Any]) -> dict[str, Any]:
    """
    Follows $ref pointers to their source in the definitions.

    Args:
        schema: Part of a schema that may contain a $ref.
        definitions: The $defs or definitions dictionary.

    Returns:
        dict: The resolved schema fragment.
    """
    if "$ref" in schema:
        ref_path = schema["$ref"]
        # Handle simple internal refs like #/$defs/TypeName or #/definitions/TypeName
        type_name = ref_path.split("/")[-1]
        return definitions.get(type_name, schema)
    return schema


def _infer_property_type(prop_def: dict[str, Any]) -> str:
    """Infer a user-facing type label when `type` is omitted in schema fragments."""
    explicit_type = prop_def.get("type")
    if explicit_type:
        return str(explicit_type)

    if "items" in prop_def:
        return "array"

    if "properties" in prop_def or "allOf" in prop_def or "anyOf" in prop_def:
        return "object"

    if "$ref" in prop_def:
        return "ref"

    return "any"


def generate_type_markdown(
    type_name: str, type_def: dict[str, Any], definitions: dict[str, Any] | None = None
) -> str:
    """
    Generates a markdown documentation block for a schema type.

    Args:
        type_name: Name of the type (e.g., 'Stats').
        type_def: The schema definition for this type.
        definitions: Global definitions for ref resolution.

    Returns:
        str: Formatted markdown.
    """
    markdown = [f"### {type_name}"]

    if "description" in type_def:
        markdown.append(type_def["description"])

    markdown.append("")

    properties = _gather_properties(type_def, definitions)

    if properties:
        for prop_name, prop_def in properties.items():
            if not isinstance(prop_def, dict):
                continue
            resolved_prop_def = prop_def
            if definitions:
                resolved_prop_def = resolve_refs(prop_def, definitions)
            if not isinstance(resolved_prop_def, dict):
                continue

            p_type = _infer_property_type(resolved_prop_def)
            p_desc = resolved_prop_def.get("description", "No description provided")

            constraints = []
            if "minimum" in resolved_prop_def:
                constraints.append(f"Min: {resolved_prop_def['minimum']}")
            if "maximum" in resolved_prop_def:
                constraints.append(f"Max: {resolved_prop_def['maximum']}")
            if "enum" in resolved_prop_def:
                constraints.append(
                    f"Allowed: {', '.join(map(str, resolved_prop_def['enum']))}"
                )

            constraint_str = f" [{', '.join(constraints)}]" if constraints else ""

            markdown.append(f"- `{prop_name}` ({p_type}): {p_desc}{constraint_str}")

    # Handle top-level enums
    elif "enum" in type_def:
        markdown.append(f"Allowed values: {', '.join(map(str, type_def['enum']))}")

    return "\n".join(markdown)


def generate_schema_documentation(schema_name: str) -> str:
    """
    Generates a full markdown document from a JSON Schema file.

    Args:
        schema_name: Base name of the schema (e.g., 'game_state').

    Returns:
        str: Full documentation as a markdown string.
    """
    schema = load_schema(schema_name)
    title = schema.get("title", schema_name.replace("_", " ").title())
    description = schema.get("description", "")

    markdown = [
        f"# {title} Schema Documentation",
        description,
        "",
        "## Data Structures",
        "",
    ]

    definitions = schema.get("$defs", schema.get("definitions", {}))

    # Order definitions logically - complex ones first or alphabetical
    sorted_types = sorted(definitions.keys())

    for type_name in sorted_types:
        markdown.append(
            generate_type_markdown(type_name, definitions[type_name], definitions)
        )
        markdown.append("")

    # Also add top-level properties
    markdown.append("## Root Properties")
    markdown.append(generate_type_markdown("Root", schema, definitions))

    return "\n".join(markdown)


def get_schema_instructions(type_name: str, schema_name: str = "game_state") -> str:
    """
    Retrieves documentation for a specific schema type.

    Args:
        type_name: Name of the type to document.
        schema_name: Base name of the schema file.

    Returns:
        str: Markdown documentation for the type.
    """
    schema = load_schema(schema_name)
    definitions = schema.get("$defs", schema.get("definitions", {}))

    if type_name == "Root":
        return generate_type_markdown("Root", schema, definitions)

    if type_name in definitions:
        return generate_type_markdown(type_name, definitions[type_name], definitions)

    raise ValueError(f"Type '{type_name}' not found in schema '{schema_name}'.")


def get_schema_fields_instructions(
    type_name: str,
    field_names: list[str],
    schema_name: str = "game_state",
) -> str:
    """Return markdown documentation for selected fields from a schema type."""
    schema = load_schema(schema_name)
    definitions = schema.get("$defs", schema.get("definitions", {}))

    if type_name not in definitions:
        raise ValueError(f"Type '{type_name}' not found in schema '{schema_name}'.")

    type_def = definitions[type_name]

    properties = _gather_properties(type_def, definitions)
    markdown = [f"### {type_name} Schema Fields", ""]

    for field_name in field_names:
        prop_def = properties.get(field_name)
        if not isinstance(prop_def, dict):
            raise ValueError(
                f"Field '{field_name}' not found in type '{type_name}' for schema '{schema_name}'."
            )

        resolved_prop_def = resolve_refs(prop_def, definitions)
        p_type = _infer_property_type(resolved_prop_def)
        p_desc = resolved_prop_def.get("description", "No description provided")
        markdown.append(f"- `{field_name}` ({p_type}): {p_desc}")

    return "\n".join(markdown)
