# First repository experience

Status: Implemented for v0.1

## Placement

Repository initialization belongs in the reference tooling, not in the core
conceptual model. It materializes the repository structure already defined by
the specification and introduces no new canonical facts or inferred semantics.

## Command

`openea init <directory>` creates `metadata.json`, `resources.json` and
`relationships.json`. The generated repository activates only the framework-
neutral core metamodel. The resources and relationships collections are empty.

The optional `--name`, `--uri` and `--namespace` arguments set explicit
repository metadata. The repository URI identifies the repository; the
namespace is the base URI for resources governed by it. Neither implies the
other. When omitted, the command writes a human-readable name based on the
directory name and visible `oea://local/` identifiers. These are initial values,
not semantics inferred later from the directory name. Users intending to
exchange or publish the repository should replace both local identifiers with
identifiers they govern.

Initialization never overwrites a non-empty directory.
