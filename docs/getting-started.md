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
  --name "My architecture"
openea validate my-architecture
```

The generated repository uses a provisional workspace namespace such as:

```json
{
  "uri": "urn:openea:workspace:my-architecture:repository",
  "namespaces": {
    "work": "urn:openea:workspace:my-architecture:"
  }
}
```

This is a valid working namespace. It requires no public domain and makes no
claim to be an official namespace of an organization.

The repository contains three plain JSON files:

- `metadata.json` identifies the repository and its active metamodel packages.
- `resources.json` contains explicit architecture resources.
- `relationships.json` contains explicit relationships between resources.

The initial collections are empty and valid. To see a populated provisional
repository, inspect `examples/workspace-start`. Its `amsterdam` segment describes
the subject of the working model; it is not an official Gemeente Amsterdam
namespace. The larger `examples/gemeente-demo` shows an end-to-end repository.

You can use compact identifiers after declaring a prefix:

```json
{
  "namespaces": {
    "ams-work": "urn:openea:workspace:alex:amsterdam:"
  }
}
```

For example, `ams-work:component/zaaksysteem` expands to
`urn:openea:workspace:alex:amsterdam:component/zaaksysteem`.

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
