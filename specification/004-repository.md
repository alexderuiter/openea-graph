# Repository format

A canonical repository consists of:

- `metadata.json`
- `resources.json`
- `relationships.json`

Implementations MAY split these files for scale, provided the logical model remains equivalent.

## Metadata

Metadata declares the repository URI, version, active metamodel packages and namespaces.

## Resources

`resources.json` contains explicit resources only. Every resource MUST declare one primary lifecycle status in `lifecycle.status`. A lifecycle MAY additionally declare `validFrom` and `expectedUntil` dates. Implementations MUST NOT infer a missing status from a view, diagram style or repository context.

## Relationships

`relationships.json` contains explicit relationships only. Derived relationships SHOULD be returned in a separate query result or cache.
