# Core principles

## Generic graph

The OpenEA Graph core MUST remain independent of ArchiMate and other modelling languages.

## Explicit knowledge

The canonical repository MUST store explicit assertions. Derived assertions MUST be identifiable as derived and SHOULD be regenerated from facts and rules.

## Everything addressable

Every resource, relationship, type, changeset, rule and view MUST have a URI.

## Human-governed AI

AI-generated content MUST enter the system as a proposed change set. It MUST NOT silently overwrite the canonical repository.

## Portable JSON

A conforming repository MUST be representable as UTF-8 JSON without requiring a specialised graph database.

## Extensibility

Framework semantics MUST be supplied through metamodel packages. The core MUST NOT require changes when a new framework is introduced.
