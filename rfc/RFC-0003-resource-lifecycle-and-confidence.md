# RFC-0003 — Resource Lifecycle and Confidence

Status: Accepted

## Summary

OpenEA Graph resources may declare two independent properties:

- `status` describes the resource's lifecycle;
- `confidence` describes how certain the repository is about its knowledge of the resource.

Both properties are optional. When present, they use the controlled values defined in this RFC.

## Lifecycle status

The allowed lifecycle status values are:

- `concept` — an idea under consideration, without a commitment to implement it;
- `planned` — intended or approved, but not yet operational;
- `inUse` — currently operational or actively used;
- `phasingOut` — still in use, but being replaced or withdrawn;
- `retired` — no longer in use;
- `rejected` — considered and explicitly not selected.

Lifecycle status captures intended and historical architecture as well as current reality. A concept resource is therefore a valid part of the repository, provided its status makes its nature explicit.

## Confidence

The allowed confidence values are:

- `proposed` — submitted as a proposal or hypothesis and awaiting assessment;
- `assumed` — treated as true for now, but not confirmed;
- `uncertain` — evidence is incomplete or conflicting;
- `verified` — confirmed against an authoritative person or source.

Confidence concerns the quality of the repository's knowledge. It does not describe whether the resource itself is current or desirable.

## Orthogonality

Lifecycle status and confidence are orthogonal because they answer different questions:

- lifecycle: *Where is this resource in its evolution?*
- confidence: *How certain are we that this information is correct?*

No lifecycle value implies a confidence value, and no confidence value implies a lifecycle value. For example:

```json
{
  "name": "New Case Platform",
  "status": "concept",
  "confidence": "verified"
}
```

This means that the platform is verifiably being considered; it does not mean that implementation is certain.

```json
{
  "name": "Legacy Case System",
  "status": "inUse",
  "confidence": "uncertain"
}
```

This means that current use has been reported but still needs confirmation.

Keeping these dimensions separate prevents diagrams and reports from presenting ideas as operational reality or assumptions as verified facts. Clients may filter or style resources by either dimension, but the meaning remains in the repository data rather than in visual conventions.

## Consequences

Metamodel packages may use these core values without redefining them. Extensions may add contextual lifecycle observations or richer evidence models, but must not change the meaning of the values in this RFC.

Changes to `status` or `confidence` are explicit repository changes and should retain ordinary change-set provenance. Inference engines must not silently promote confidence or advance lifecycle status.
