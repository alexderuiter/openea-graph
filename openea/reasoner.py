from __future__ import annotations


def derive_inverse_relationships(relationships: list[dict], rules: list[dict]) -> list[dict]:
    """Return inverse assertions derived from explicit relationships."""
    inverse_rules = {
        rule.get("relationshipType"): rule
        for rule in rules
        if rule.get("kind") == "inverse" and rule.get("relationshipType") and rule.get("inverseType")
    }
    derived = []
    for relationship in relationships:
        rule = inverse_rules.get(relationship.get("type"))
        if not rule:
            continue
        derived.append(
            {
                "type": rule["inverseType"],
                "from": relationship["to"],
                "to": relationship["from"],
                "derived": True,
                "provenance": {
                    "rule": rule["uri"],
                    "sourceRelationships": [relationship["uri"]],
                },
            }
        )
    return derived
