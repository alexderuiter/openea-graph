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
- `lifecycle.status`
- `confidence`

Every resource MUST have exactly one primary lifecycle status:

- `concept` — an idea that has not been approved;
- `planned` — approved or intended, but not yet in use;
- `inUse` — currently in operational use;
- `phasingOut` — still in use, but being retired or replaced;
- `retired` — no longer in use;
- `rejected` — considered and explicitly not selected.

The lifecycle MAY include `validFrom` and `expectedUntil` dates. These dates MUST use the ISO 8601 full-date format (`YYYY-MM-DD`). Lifecycle status is a property of the resource, not of a view. Context-specific lifecycle status is outside the scope of version 0.1.

Every resource MUST also have exactly one confidence value describing how certain the stored information is:

- `proposed` — an idea or hypothesis;
- `assumed` — accepted as an assumption but not yet confirmed;
- `verified` — confirmed and considered reliable;
- `deprecated` — outdated or no longer considered reliable.

`confidence` and `lifecycle.status` are independent. For example, an `inUse` resource can have `assumed` confidence when its operational status has not yet been verified, while a `planned` resource can be `verified` when the plan is formally confirmed.

Resource confidence is categorical and describes the reliability of architecture knowledge. It is distinct from the optional numeric confidence score used in provenance and change sets to describe an extraction or proposal.

Example:

```json
{
  "uri": "oea://gemeente-demo/application/new-case-system",
  "type": "archimate://element-type/application-component",
  "name": "Nieuw zaaksysteem",
  "lifecycle": {
    "status": "planned",
    "validFrom": "2027-01-01"
  },
  "confidence": "verified"
}
```

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
