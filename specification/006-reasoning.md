# Reasoning

Reasoning is optional and modular.

## Inverse rules

An inverse rule can derive `B parentOf A` from `A childOf B`.

Version 0.1 represents an inverse rule as:

```json
{
  "uri": "oea://rule/replaced-by-inverse",
  "kind": "inverse",
  "relationshipType": "oea://relationship-type/replaced-by",
  "inverseType": "oea://relationship-type/replaces"
}
```

The reference reasoner implements inverse rules only. Given an explicit assertion that the historical case system `replaced-by` the new platform, it emits the derived assertion that the new platform `replaces` the historical system. The derived assertion is output separately and is not written to the canonical repository.

## Symmetric rules

A symmetric relationship can derive `B relatedTo A` from `A relatedTo B`.

## Transitive rules

A transitive relationship can derive `A partOf C` from `A partOf B` and `B partOf C`.

## Property chains

A property chain can derive a new relationship from a sequence of relationships.

Example:

```text
Application realizes ApplicationService
ApplicationService serves BusinessService
=> Application indirectlySupports BusinessService
```

## Provenance

Every derived assertion MUST identify:

- the rule used;
- the source assertions;
- that it is derived;
- the reasoning run or engine version when materialised.

Derived assertions MUST NOT be presented as manually confirmed facts.
