# Reasoning

Reasoning is optional and modular.

## Inverse rules

An inverse rule can derive `B parentOf A` from `A childOf B`.

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
