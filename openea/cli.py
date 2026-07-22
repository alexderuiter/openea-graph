from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reasoner import derive_inverse_relationships
from .validator import validate_repository


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openea", description="OpenEA Graph 0.1 reference CLI")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "reason"):
        child = commands.add_parser(command)
        child.add_argument("repository", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
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
