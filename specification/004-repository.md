# Repository format

A canonical repository consists of:

- `metadata.json`
- `resources.json`
- `relationships.json`

Implementations MAY split these files for scale, provided the logical model remains equivalent.

## Metadata

Metadata declares the repository URI, version, active metamodel packages and
namespaces. Namespace values MUST be valid absolute URIs but need not use HTTP
or resolve publicly. Declared prefixes MAY abbreviate identifiers as specified
in `003-uri.md`.

## Resources

`resources.json` contains explicit resources only. Every resource MUST declare `uri`, `type` and `name`. It MAY declare `description`, `status`, `confidence` and free-form `properties`. Implementations MUST NOT infer a missing lifecycle status or confidence value from a view, diagram style or repository context. Resource confidence MUST remain distinct from numeric confidence scores in provenance and change sets.

Version 0.1 lifecycle values are `concept`, `planned`, `inUse`, `phasingOut`, `retired` and `rejected`. Confidence values are `proposed`, `assumed`, `uncertain` and `verified`; `deprecated` is not a confidence value.

## Relationships

`relationships.json` contains explicit relationships only. Derived relationships SHOULD be returned in a separate query result or cache.
