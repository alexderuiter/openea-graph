from __future__ import annotations

import json
import re
from pathlib import Path


SPECIFICATION_VERSION = "0.1.0-draft"
CORE_METAMODEL = "oea://metamodel/core/0.1"


class InitializationError(Exception):
    """Raised when a repository cannot be initialized safely."""


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "repository"


def initialize_repository(
    target: Path,
    name: str | None = None,
    uri: str | None = None,
    namespace: str | None = None,
) -> None:
    target = target.resolve()
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise InitializationError(f"{target} exists and is not an empty directory")

    repository_name = name or target.name.replace("-", " ").replace("_", " ").strip().title()
    repository_name = repository_name or "OpenEA Graph repository"
    workspace_namespace = f"urn:openea:workspace:{_slug(target.name)}:"
    repository_uri = uri or f"{workspace_namespace}repository"
    metadata = {
        "uri": repository_uri,
        "name": repository_name,
        "specificationVersion": SPECIFICATION_VERSION,
        "metamodels": [CORE_METAMODEL],
        "namespaces": {"work": namespace or workspace_namespace},
    }

    target.mkdir(parents=True, exist_ok=True)
    for filename, value in (
        ("metadata.json", metadata),
        ("resources.json", []),
        ("relationships.json", []),
    ):
        (target / filename).write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
