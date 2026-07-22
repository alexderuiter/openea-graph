# OpenEA Graph

**OpenEA Graph** is an open, lightweight and AI-native knowledge graph format for enterprise architecture.

The core is framework-neutral. ArchiMate, GEMMA, NORA, BPMN and other modelling languages are represented as metamodel packages on top of the same graph.

## Status

Version: `0.1.0-draft`

This repository is the initial foundation. It defines:

- a generic graph core;
- URI-based identity;
- explicit facts as the repository source of truth;
- metamodel packages;
- validation constraints;
- reasoning rules;
- reviewable change sets for AI-assisted imports.

## Core idea

A stored relationship is an explicit fact:

```json
{
  "uri": "oea://example/relationship/djuma-serves-permits",
  "type": "archimate://relationship-type/serving",
  "from": "oea://example/application/djuma",
  "to": "oea://example/business-service/permit-application"
}
```

Derived knowledge is calculated separately and is never confused with source facts.

## Repository layout

- `specification/` — normative specification
- `schemas/` — JSON Schemas for validation
- `metamodels/` — framework-specific type definitions and rules
- `repository/` — empty canonical repository files
- `examples/` — small working examples
- `changesets/` — example AI/import proposals
- `rfc/` — architecture decision records and proposals

## Design principles

1. Repository first
2. Generic graph core
3. Everything addressable by URI
4. Explicit facts remain distinguishable from derived knowledge
5. AI proposes changes; humans approve them
6. Metamodels and reasoning are replaceable modules
7. Plain JSON remains the portable interchange format
8. RDF/JSON-LD and ArchiMate Exchange are export targets, not hard dependencies

## Next milestones

- complete the ArchiMate 3.2 metamodel package;
- add a validator;
- add spreadsheet-to-changeset instructions;
- add ArchiMate Open Exchange export;
- add JSON-LD export.

## License

No license has been selected yet. Add a license only after deciding whether the project should be permissive, reciprocal, or initially private.
