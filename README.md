# OpenEA Graph

**OpenEA Graph** is an open, lightweight and AI-native knowledge graph format for enterprise architecture.

The core is framework-neutral. ArchiMate, GEMMA, NORA, BPMN and other modelling languages are represented as metamodel packages on top of the same graph.

New contributors should start with [FOUNDATIONS.md](FOUNDATIONS.md), which describes the project's enduring design philosophy and the boundaries of the core.

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

The `examples/gemeente-demo` repository is the normative end-to-end v0.1 example. It combines Amsterdam resources, a GEMMA reference component, lifecycle and confidence values, framework alignment, validation and one inverse reasoning rule.

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

## Run the v0.1 reference tooling

Python 3.10 or newer is required. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
openea init my-architecture
openea validate my-architecture
openea validate examples/gemeente-demo
```

Expected result:

```text
OK: examples/gemeente-demo is a valid OpenEA Graph 0.1 repository.
```

See [Getting started](docs/getting-started.md) for the complete first-repository
walkthrough.

## Start without an official namespace

You do not need a public domain or an organization-assigned namespace to begin.
`openea init` creates a valid provisional workspace URN:

```bash
openea init my-architecture
```

```json
{
  "uri": "urn:openea:workspace:my-architecture:repository",
  "namespaces": {
    "work": "urn:openea:workspace:my-architecture:"
  }
}
```

Workspace names are local disambiguators, not claims of organizational
authority. They can be used directly or through compact identifiers such as
`work:component/zaaksysteem`. Resources can later be mapped or migrated to
canonical identifiers without invalidating the early modeling history.

Run the minimal inverse reasoner without changing the repository:

```bash
openea reason examples/gemeente-demo
```

It derives that the new platform `replaces` the historical system from the explicit inverse `replaced-by` assertion and includes provenance in the output.

Run all tests:

```bash
python -m unittest discover -s tests -v
```

Every push and pull request runs these tests across the supported Python
versions. CI also builds the distributable package and exercises `openea init`
and `openea validate` from an isolated wheel installation.

Without installing the package, equivalent commands from the repository root are:

```bash
python -m openea validate examples/gemeente-demo
python -m openea reason examples/gemeente-demo
```

## Validator scope

The v0.1 validator checks:

- unique resource and relationship URIs;
- absolute HTTP(S), URN and other valid URI schemes;
- declared namespace values and compact identifier expansion;
- required Resource fields (`uri`, `type`, `name`);
- known resource types and relationship predicates from active metamodel packages;
- lifecycle status and confidence values when present;
- relationship endpoints that reference existing resources;
- readable, location-specific errors for invalid repositories.

## Next milestones

- complete the ArchiMate 3.2 metamodel package;
- add spreadsheet-to-changeset instructions;
- add ArchiMate Open Exchange export;
- add JSON-LD export.

Release criteria and the intentionally manual publication boundary are
documented in [Releasing](docs/releasing.md). User-visible changes are recorded
in the [Changelog](CHANGELOG.md).

## License

OpenEA Graph is licensed under the [Apache License 2.0](LICENSE).

The license permits commercial and non-commercial use, modification and
distribution, subject to its terms. It does not grant permission to use project
names or trademarks except as required to describe the origin of the work.
