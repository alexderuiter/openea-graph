from __future__ import annotations

import argparse
import json
from pathlib import Path

from .initializer import InitializationError, initialize_repository
from .reasoner import derive_inverse_relationships
from .validator import validate_repository


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openea", description="OpenEA Graph 0.1 reference CLI")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create a minimal OpenEA Graph repository")
    init.add_argument("repository", type=Path)
    init.add_argument("--name", help="repository display name")
    init.add_argument("--uri", help="stable repository URI")
    init.add_argument("--namespace", help="base URI for resources owned by the repository")
    for command in ("validate", "reason"):
        child = commands.add_parser(command)
        child.add_argument("repository", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        try:
            initialize_repository(
                args.repository,
                name=args.name,
                uri=args.uri,
                namespace=args.namespace,
            )
        except InitializationError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Created OpenEA Graph repository at {args.repository}.")
        print(f"Next: openea validate {args.repository}")
        return 0

    errors, relationships, rules = validate_repository(args.repository)
    if errors:
        for error in errors:
            print(error)
        print(f"Validation failed with {len(errors)} error(s).")
        return 1
    if args.command == "validate":
        print(f"OK: {args.repository} is a valid OpenEA Graph 0.1 repository.")
        return 0
    print(json.dumps(derive_inverse_relationships(relationships, rules), indent=2, ensure_ascii=False))
    return 0
