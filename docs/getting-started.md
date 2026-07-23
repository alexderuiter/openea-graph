# Getting started

Install the reference tooling from a checkout using Python 3.10 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Create and validate your first repository:

```bash
openea init my-architecture \
  --name "My architecture" \
  --uri "oea://example.org/my-architecture/repository" \
  --namespace "oea://example.org/my-architecture/"
openea validate my-architecture
```

The repository contains three plain JSON files:

- `metadata.json` identifies the repository and its active metamodel packages.
- `resources.json` contains explicit architecture resources.
- `relationships.json` contains explicit relationships between resources.

The initial collections are empty and valid. To see a populated repository,
inspect `examples/gemeente-demo`. Its identifiers are examples; choose stable
URIs and namespaces governed by your organization for published knowledge.

Now introduce a safe validation error by replacing `resources.json` with:

```json
[
  {
    "uri": "not-an-absolute-uri",
    "type": "oea://resource-type/resource",
    "name": "Example resource"
  }
]
```

Run `openea validate my-architecture` again. The validator identifies the file
entry and explains that its URI is not absolute. Restore `resources.json` to
`[]` before continuing.
