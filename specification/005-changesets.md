# Change sets

A change set is an auditable proposal containing one or more operations.

Supported initial operations:

- `createResource`
- `updateResource`
- `deleteResource`
- `createRelationship`
- `updateRelationship`
- `deleteRelationship`

A change set SHOULD include:

- URI
- creator
- creation time
- source references
- confidence
- status
- operations

Allowed statuses in version 0.1:

- `proposed`
- `approved`
- `rejected`
- `applied`

AI-generated operations MUST begin with status `proposed`.
