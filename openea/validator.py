from __future__ import annotations

import json
import sysconfig
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


LIFECYCLE_STATUSES = {"concept", "planned", "inUse", "phasingOut", "retired", "rejected"}
CONFIDENCE_VALUES = {"proposed", "assumed", "uncertain", "verified"}


@dataclass(frozen=True)
class ValidationError:
    location: str
    message: str

    def __str__(self) -> str:
        return f"ERROR {self.location}: {self.message}"


def _load_json(path: Path, errors: list[ValidationError]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(ValidationError(path.name, "required file is missing"))
    except json.JSONDecodeError as exc:
        errors.append(ValidationError(path.name, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"))
    return None


def _is_uri(value: object) -> bool:
    return isinstance(value, str) and bool(urlparse(value).scheme)


def _package_directory(metamodel_root: Path, package_uri: str) -> Path | None:
    for package_file in metamodel_root.glob("*/package.json"):
        try:
            package = json.loads(package_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if package.get("uri") == package_uri:
            return package_file.parent
    return None


def load_vocabulary(metamodel_root: Path, metadata: dict, errors: list[ValidationError]):
    resource_types: set[str] = set()
    relationship_types: set[str] = set()
    rules: list[dict] = []

    for index, package_uri in enumerate(metadata.get("metamodels", [])):
        directory = _package_directory(metamodel_root, package_uri)
        if directory is None:
            errors.append(ValidationError(f"metadata.metamodels[{index}]", f"unknown metamodel package {package_uri!r}"))
            continue
        package = _load_json(directory / "package.json", errors) or {}
        files = package.get("files", {})
        for key, target in (("resourceTypes", resource_types), ("relationshipTypes", relationship_types)):
            filename = files.get(key)
            if filename:
                values = _load_json(directory / filename, errors)
                if isinstance(values, list):
                    target.update(item.get("uri") for item in values if isinstance(item, dict) and _is_uri(item.get("uri")))
        reasoning_file = files.get("reasoning")
        if reasoning_file:
            reasoning = _load_json(directory / reasoning_file, errors)
            if isinstance(reasoning, dict) and isinstance(reasoning.get("rules"), list):
                rules.extend(rule for rule in reasoning["rules"] if isinstance(rule, dict))
    return resource_types, relationship_types, rules


def validate_repository(repository: Path, project_root: Path | None = None):
    repository = repository.resolve()
    if project_root is not None:
        metamodel_root = project_root.resolve() / "metamodels"
    else:
        source_root = Path(__file__).resolve().parents[1] / "metamodels"
        installed_root = (
            Path(sysconfig.get_path("data")) / "share" / "openea-graph" / "metamodels"
        )
        metamodel_root = source_root if source_root.is_dir() else installed_root
    errors: list[ValidationError] = []
    metadata = _load_json(repository / "metadata.json", errors)
    resources = _load_json(repository / "resources.json", errors)
    relationships = _load_json(repository / "relationships.json", errors)
    if not isinstance(metadata, dict) or not isinstance(resources, list) or not isinstance(relationships, list):
        return errors, [], []

    resource_types, relationship_types, rules = load_vocabulary(metamodel_root, metadata, errors)
    resource_uris: set[str] = set()
    all_uris: set[str] = set()

    for index, resource in enumerate(resources):
        location = f"resources[{index}]"
        if not isinstance(resource, dict):
            errors.append(ValidationError(location, "must be an object"))
            continue
        for field in ("uri", "type", "name"):
            if field not in resource:
                errors.append(ValidationError(f"{location}.{field}", "is required"))
        uri = resource.get("uri")
        if uri is not None and not _is_uri(uri):
            errors.append(ValidationError(f"{location}.uri", f"{uri!r} is not a valid absolute URI"))
        elif isinstance(uri, str):
            if uri in all_uris:
                errors.append(ValidationError(f"{location}.uri", f"duplicate URI {uri!r}"))
            all_uris.add(uri)
            resource_uris.add(uri)
        type_uri = resource.get("type")
        if type_uri is not None and type_uri not in resource_types:
            errors.append(ValidationError(f"{location}.type", f"unknown resource type {type_uri!r}"))
        name = resource.get("name")
        if name is not None and (not isinstance(name, str) or not name.strip()):
            errors.append(ValidationError(f"{location}.name", "must be a non-empty string"))
        status = resource.get("status")
        if status is not None and status not in LIFECYCLE_STATUSES:
            errors.append(ValidationError(f"{location}.status", f"{status!r} is invalid; allowed: {', '.join(sorted(LIFECYCLE_STATUSES))}"))
        confidence = resource.get("confidence")
        if confidence is not None and confidence not in CONFIDENCE_VALUES:
            errors.append(ValidationError(f"{location}.confidence", f"{confidence!r} is invalid; allowed: {', '.join(sorted(CONFIDENCE_VALUES))}"))

    for index, relationship in enumerate(relationships):
        location = f"relationships[{index}]"
        if not isinstance(relationship, dict):
            errors.append(ValidationError(location, "must be an object"))
            continue
        for field in ("uri", "type", "from", "to"):
            if field not in relationship:
                errors.append(ValidationError(f"{location}.{field}", "is required"))
        uri = relationship.get("uri")
        if uri is not None and not _is_uri(uri):
            errors.append(ValidationError(f"{location}.uri", f"{uri!r} is not a valid absolute URI"))
        elif isinstance(uri, str):
            if uri in all_uris:
                errors.append(ValidationError(f"{location}.uri", f"duplicate URI {uri!r}"))
            all_uris.add(uri)
        predicate = relationship.get("type")
        if predicate is not None and predicate not in relationship_types:
            errors.append(ValidationError(f"{location}.type", f"unknown relationship type/predicate {predicate!r}"))
        for field in ("from", "to"):
            target = relationship.get(field)
            if target is not None and target not in resource_uris:
                errors.append(ValidationError(f"{location}.{field}", f"references unknown resource {target!r}"))

    return errors, relationships, rules
