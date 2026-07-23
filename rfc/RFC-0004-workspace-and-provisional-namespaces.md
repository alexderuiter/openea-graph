# RFC-0004 — Workspace and provisional namespaces

Status: Accepted

## Context

Early architecture work often begins before a modeler controls a public domain
or an organization publishes canonical identifiers. Requiring an official,
resolvable namespace would delay useful work and could encourage modelers to
claim organizational authority they do not have.

OpenEA Graph already requires stable URI identity, but URI identity does not
require HTTP resolution or official organizational ownership.

## Decision

1. Workspace and provisional URIs are ordinary valid resource URIs.
2. A recommended workspace namespace has the form
   `urn:openea:workspace:<owner-or-project>:`. Additional segments MAY be used
   to organize a workspace.
3. The owner or project segment is a local disambiguator. It does not assert
   that the workspace is official or endorsed by an organization with a
   similar name.
4. Declared namespace prefixes MAY be used as compact identifiers. A compact
   identifier is expanded by replacing its declared `<prefix>:` with the
   namespace value before URI validation, uniqueness checks and reference
   resolution.
5. Resources MAY later be mapped to canonical identifiers or migrated in a
   reviewable change. The availability of a canonical identifier does not
   invalidate the earlier workspace identifier or the history that used it.
6. The core does not add an identifier status, governance object or profile
   mechanism for this capability.

## Consequences

- Modeling can start without a public domain or official namespace assignment.
- Validators must accept valid non-HTTP URI schemes, including workspace URNs.
- Validators must resolve declared compact identifiers consistently.
- Existing absolute identifiers and HTTP(S) namespaces remain valid.
- Namespace governance remains explicit documentation and repository policy,
  rather than a new core data structure.
