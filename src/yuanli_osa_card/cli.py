"""Command-line interface for the canonical OSA v2 package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .engine import CardValidationError, contract_sha256, evaluate_card, load_schema
from .migration import migrate_v1


def _read(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _emit(value: Any, path: str | None) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path:
        Path(path).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="yuanli-osa-card")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("score", "validate"):
        cmd = sub.add_parser(name)
        cmd.add_argument("card")
        cmd.add_argument("--output")
    migrate = sub.add_parser("migrate-v1")
    migrate.add_argument("card")
    migrate.add_argument("--output")
    migrate.add_argument("--card-id")
    schema = sub.add_parser("schema")
    schema.add_argument("--output")
    sub.add_parser("schema-hash")
    args = parser.parse_args(argv)

    if args.command == "schema-hash":
        print(contract_sha256())
        return 0
    if args.command == "schema":
        _emit(load_schema(), args.output)
        return 0
    if args.command == "migrate-v1":
        _emit(migrate_v1(_read(args.card), card_id=args.card_id), args.output)
        return 0

    try:
        result = evaluate_card(_read(args.card))
    except CardValidationError as exc:
        _emit({"valid": False, "errors": exc.errors}, args.output)
        return 2
    _emit(result, args.output)
    return 0 if (args.command == "score" or result["valid"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
