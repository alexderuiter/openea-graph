# Repository format

A canonical repository consists of:

- `metadata.json`
- `resources.json`
- `relationships.json`

Implementations MAY split these files for scale, provided the logical model remains equivalent.

## Metadata

Metadata declares the repository URI, version, active metamodel packages and namespaces.

## Resources

`resources.json` contains explicit resources only.

## Relationships

`relationships.json` contains explicit relationships only. Derived relationships SHOULD be returned in a separate query result or cache.
