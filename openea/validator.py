from __future__ import annotations

import json
import re
import sysconfig
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


LIFECYCLE_STATUSES = {"concept", "planned", "inUse", "phasingOut", "retired", "rejected"}
CONFIDENCE_VALUES = {"proposed", "assumed", "uncertain", "verified"}
URI_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:(.+)$")
PREFIX_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")
INVALID_URI_CHARACTERS = re.compile(r"[\x00-\x20<>\"{}|\\^`]")
INVALID_PERCENT_ENCODING = re.compile(r"%(?![0-9A-Fa-f]{2})")


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
    if not isinstance(value, str) or INVALID_URI_CHARACTERS.search(value):
        return False
    match = URI_PATTERN.fullmatch(value)
    if match is None or INVALID_PERCENT_ENCODING.search(value):
        return False
    scheme = value.split(":", 1)[0].lower()
    remainder = match.group(1)
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if scheme in {"http", "https"}:
        return bool(parsed.netloc)
    if remainder.startswith("//") and not parsed.netloc:
        return False
    if scheme == "urn":
        namespace_identifier, separator, namespace_specific = remainder.partition(":")
        return bool(separator and namespace_identifier and namespace_specific)
    return bool(remainder)


def expand_identifier(value: object, namespaces: dict[str, str]) -> object:
    """Expand a declared compact identifier; leave other values unchanged."""
    if not isinstance(value, str):
        return value
    prefix, separator, reference = value.partition(":")
    if separator and prefix in namespaces:
        return f"{namespaces[prefix]}{reference}"
    return value


def _load_namespaces(metadata: dict, errors: list[ValidationError]) -> dict[str, str]:
    value = metadata.get("namespaces", {})
    if not isinstance(value, dict):
        errors.append(ValidationError("metadata.namespaces", "must be an object"))
        return {}

    namespaces: dict[str, str] = {}
    for prefix, namespace in value.items():
        location = f"metadata.namespaces.{prefix}"
        if not isinstance(prefix, str) or PREFIX_PATTERN.fullmatch(prefix) is None:
            errors.append(ValidationError(location, "prefix is invalid"))
            continue
        if not _is_uri(namespace):
            errors.append(
                ValidationError(location, f"{namespace!r} is not a valid absolute URI")
            )
            continue
        namespaces[prefix] = namespace
    return namespaces


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

    namespaces = _load_namespaces(metadata, errors)
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
        expanded_uri = expand_identifier(uri, namespaces)
        if uri is not None and not _is_uri(expanded_uri):
            errors.append(ValidationError(f"{location}.uri", f"{uri!r} is not a valid absolute URI"))
        elif isinstance(expanded_uri, str):
            if expanded_uri in all_uris:
                errors.append(ValidationError(f"{location}.uri", f"duplicate URI {uri!r}"))
            all_uris.add(expanded_uri)
            resource_uris.add(expanded_uri)
        type_uri = expand_identifier(resource.get("type"), namespaces)
        if type_uri is not None and type_uri not in resource_types:
            errors.append(ValidationError(f"{location}.type", f"unknown resource type {resource.get('type')!r}"))
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
        expanded_uri = expand_identifier(uri, namespaces)
        if uri is not None and not _is_uri(expanded_uri):
            errors.append(ValidationError(f"{location}.uri", f"{uri!r} is not a valid absolute URI"))
        elif isinstance(expanded_uri, str):
            if expanded_uri in all_uris:
                errors.append(ValidationError(f"{location}.uri", f"duplicate URI {uri!r}"))
            all_uris.add(expanded_uri)
        predicate = expand_identifier(relationship.get("type"), namespaces)
        if predicate is not None and predicate not in relationship_types:
            errors.append(ValidationError(f"{location}.type", f"unknown relationship type/predicate {relationship.get('type')!r}"))
        for field in ("from", "to"):
            target = relationship.get(field)
            expanded_target = expand_identifier(target, namespaces)
            if target is not None and expanded_target not in resource_uris:
                errors.append(ValidationError(f"{location}.{field}", f"references unknown resource {target!r}"))

    return errors, relationships, rules
