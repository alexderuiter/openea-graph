# OpenEA Graph Foundations

OpenEA Graph is an open knowledge representation for enterprise architecture. It is not an enterprise architecture application or a replacement for a modelling framework. It is a small, portable foundation on which repositories, tools, assistants, visualizations and framework-specific models can be built.

This document captures the project's enduring design philosophy. Implementation details belong in the specification, schemas and RFCs.

## Repository first

The repository is the source of truth. Diagrams, reports, search indexes, exports and AI-generated explanations are views of repository knowledge, not competing sources of knowledge.

OpenEA Graph stores explicit knowledge only: facts that a person or an identified source has asserted and that can be reviewed. Derived knowledge is never stored in the canonical repository. A reasoning engine may calculate inferred relationships, but it must keep them distinguishable from explicit facts and be able to reproduce their provenance.

This separation keeps the repository understandable, auditable and safe to edit without a particular reasoning engine.

## AI native, human governed

OpenEA Graph is AI-native. Its structures are intended to be easy for AI systems to read, propose and explain. AI does not silently redefine the source of truth. AI-assisted imports and edits should be expressed as reviewable change sets so that people can inspect, correct and approve them.

The repository should capture both the architecture and the confidence in that knowledge. Architecture work includes ideas, assumptions and incomplete information as well as verified facts. Representing that uncertainty explicitly is more truthful than presenting every resource as equally certain.

Lifecycle status and confidence are separate concepts. Lifecycle describes where a resource is in its evolution, such as a concept, something in use or something retired. Confidence describes how certain the repository is about the assertion. A retired resource can be verified, while an in-use resource can still be assumed or uncertain.

## Everything is addressable

Every resource has a URI. A URI is its stable identity, independent of its display name, location in a file or appearance in a diagram. Names may change; references should remain intact.

URI-based identity also allows repositories and frameworks to refer to one another without copying or merging their contents. Resources from Amsterdam, GEMMA or another organization can coexist and remain unambiguous.

## Framework-neutral core

The core knows only the generic concepts needed to represent resources and relationships. Frameworks such as ArchiMate, GEMMA, NORA, BPMN and UML are extensions or metamodel packages, not part of the core.

Different frameworks and organizational vocabularies can be aligned through explicit mapping relationships. A mapping may express equivalence, similarity, a broader or narrower meaning, or a deliberate deviation. These mappings are normal, inspectable facts; they are not hidden name matching or implicit conversion.

Keeping frameworks outside the core allows them to evolve independently and lets one repository use more than one framework.

## Minimal by design

Keep the core minimal. Prefer extensions over core changes. A capability belongs in the core only when it is broadly necessary for representing knowledge and cannot be expressed cleanly by an extension.

Favor explicitness over magic. Important meaning should be visible in the data or declared by an extension, rather than inferred from filenames, colors, naming conventions or undocumented behavior.

Human readability and Git friendliness are primary design goals. A person should be able to inspect a repository with ordinary text tools, understand a change in a diff and review it in a pull request. Plain, predictable structures are preferred over compact but opaque representations.

OpenEA Graph should remain useful without a database server, specialized editor or proprietary platform. More powerful implementations are welcome, but portability and transparent ownership of the knowledge come first.
