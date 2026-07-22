# Core model

OpenEA Graph has six primary concepts.

## ResourceType

Defines a class of resources, such as an ArchiMate Application Component.

## RelationshipType

Defines a class of directed relationships, such as Serving or Assignment.

## Resource

Represents an instance such as Djuma, Team Vergunningen or Permit Application Service.

Required fields:

- `uri`
- `type`
- `name`

## Relationship

Represents a directed assertion from one resource to another.

Required fields:

- `uri`
- `type`
- `from`
- `to`

## Rule

Describes optional inference semantics, including inverse, symmetric, transitive and property-chain rules.

## ChangeSet

Contains proposed repository operations plus provenance, confidence and approval status.
