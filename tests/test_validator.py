import json
import tempfile
import unittest
from pathlib import Path

from openea.reasoner import derive_inverse_relationships
from openea.validator import validate_repository


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO = PROJECT_ROOT / "examples" / "gemeente-demo"


class ValidatorTests(unittest.TestCase):
    def test_gemeente_demo_is_valid(self):
        errors, _, _ = validate_repository(DEMO, PROJECT_ROOT)
        self.assertEqual([], errors)

    def test_reports_invalid_values_duplicates_and_dangling_references(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            metadata = json.loads((DEMO / "metadata.json").read_text())
            resources = json.loads((DEMO / "resources.json").read_text())
            relationships = json.loads((DEMO / "relationships.json").read_text())
            resources[1]["uri"] = resources[0]["uri"]
            resources[1]["status"] = "active"
            resources[1]["confidence"] = "deprecated"
            resources[2]["type"] = "unknown://resource-type/example"
            relationships[0]["type"] = "unknown://relationship-type/example"
            relationships[0]["to"] = "oea://missing/resource"
            for name, value in (
                ("metadata.json", metadata),
                ("resources.json", resources),
                ("relationships.json", relationships),
            ):
                (target / name).write_text(json.dumps(value), encoding="utf-8")

            errors, _, _ = validate_repository(target, PROJECT_ROOT)
            messages = "\n".join(map(str, errors))
            self.assertIn("duplicate URI", messages)
            self.assertIn("resources[1].status", messages)
            self.assertIn("resources[1].confidence", messages)
            self.assertIn("unknown resource type", messages)
            self.assertIn("unknown relationship type/predicate", messages)
            self.assertIn("references unknown resource", messages)

    def test_inverse_rule_derives_replaces_relationship(self):
        errors, relationships, rules = validate_repository(DEMO, PROJECT_ROOT)
        self.assertEqual([], errors)
        derived = derive_inverse_relationships(relationships, rules)
        self.assertEqual(1, len(derived))
        self.assertEqual("oea://relationship-type/replaces", derived[0]["type"])
        self.assertEqual("oea://amsterdam/application/new-case-platform", derived[0]["from"])
        self.assertTrue(derived[0]["derived"])


if __name__ == "__main__":
    unittest.main()
