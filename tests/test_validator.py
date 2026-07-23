import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from openea.cli import main
from openea.initializer import InitializationError, initialize_repository
from openea.reasoner import derive_inverse_relationships
from openea.validator import expand_identifier, validate_repository


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO = PROJECT_ROOT / "examples" / "gemeente-demo"
WORKSPACE_START = PROJECT_ROOT / "examples" / "workspace-start"


class ValidatorTests(unittest.TestCase):
    def test_init_creates_a_minimal_valid_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "my-architecture"
            initialize_repository(
                target,
                name="My architecture",
                uri="oea://example.org/my-architecture/repository",
                namespace="oea://example.org/my-architecture/",
            )

            self.assertEqual(
                {"metadata.json", "resources.json", "relationships.json"},
                {path.name for path in target.iterdir()},
            )
            metadata = json.loads((target / "metadata.json").read_text())
            self.assertEqual("My architecture", metadata["name"])
            self.assertEqual("oea://example.org/my-architecture/repository", metadata["uri"])
            self.assertEqual(
                "oea://example.org/my-architecture/", metadata["namespaces"]["work"]
            )
            errors, _, _ = validate_repository(target, PROJECT_ROOT)
            self.assertEqual([], errors)

    def test_init_refuses_to_overwrite_a_non_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            existing = target / "keep.txt"
            existing.write_text("keep", encoding="utf-8")

            with self.assertRaises(InitializationError):
                initialize_repository(target)
            self.assertEqual("keep", existing.read_text(encoding="utf-8"))

    def test_init_cli_reports_the_next_command(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "first-repository"
            output = io.StringIO()
            with redirect_stdout(output):
                result = main(["init", str(target)])

            self.assertEqual(0, result)
            self.assertIn(f"openea validate {target}", output.getvalue())

    def test_init_uses_a_workspace_urn_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "personal-architecture"
            initialize_repository(target)

            metadata = json.loads((target / "metadata.json").read_text())
            self.assertEqual(
                "urn:openea:workspace:personal-architecture:repository",
                metadata["uri"],
            )
            self.assertEqual(
                {"work": "urn:openea:workspace:personal-architecture:"},
                metadata["namespaces"],
            )

    def test_gemeente_demo_is_valid(self):
        errors, _, _ = validate_repository(DEMO, PROJECT_ROOT)
        self.assertEqual([], errors)

    def test_workspace_urns_and_compact_identifiers_are_valid(self):
        errors, _, _ = validate_repository(WORKSPACE_START, PROJECT_ROOT)
        self.assertEqual([], errors)
        self.assertEqual(
            "urn:openea:workspace:alex:amsterdam:component/zaaksysteem",
            expand_identifier(
                "ams-work:component/zaaksysteem",
                {"ams-work": "urn:openea:workspace:alex:amsterdam:"},
            ),
        )

    def test_https_namespaces_remain_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            initialize_repository(
                target,
                uri="https://architecture.example/repository",
                namespace="https://architecture.example/resource/",
            )

            errors, _, _ = validate_repository(target, PROJECT_ROOT)
            self.assertEqual([], errors)

    def test_compact_and_expanded_identifiers_resolve_to_the_same_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            metadata = json.loads((WORKSPACE_START / "metadata.json").read_text())
            resources = json.loads((WORKSPACE_START / "resources.json").read_text())
            relationships = [
                {
                    "uri": "ams-work:relationship/self",
                    "type": "archimate://relationship-type/association",
                    "from": "ams-work:component/zaaksysteem",
                    "to": "urn:openea:workspace:alex:amsterdam:component/zaaksysteem",
                }
            ]
            for name, value in (
                ("metadata.json", metadata),
                ("resources.json", resources),
                ("relationships.json", relationships),
            ):
                (target / name).write_text(json.dumps(value), encoding="utf-8")

            errors, _, _ = validate_repository(target, PROJECT_ROOT)
            self.assertEqual([], errors)

    def test_malformed_resource_and_namespace_uris_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            metadata = json.loads((WORKSPACE_START / "metadata.json").read_text())
            resources = json.loads((WORKSPACE_START / "resources.json").read_text())
            metadata["namespaces"]["broken"] = "https://"
            resources[0]["uri"] = "not an absolute URI"
            resources.append(
                {
                    "uri": "https://exa[mple",
                    "type": "archimate://element-type/application-component",
                    "name": "Malformed HTTPS identifier",
                }
            )
            for name, value in (
                ("metadata.json", metadata),
                ("resources.json", resources),
                ("relationships.json", []),
            ):
                (target / name).write_text(json.dumps(value), encoding="utf-8")

            errors, _, _ = validate_repository(target, PROJECT_ROOT)
            messages = "\n".join(map(str, errors))
            self.assertIn("metadata.namespaces.broken", messages)
            self.assertIn("resources[0].uri", messages)
            self.assertIn("resources[1].uri", messages)

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
