"""Command-line entry point for slugify-cli."""
from __future__ import annotations

import argparse
import os
import sys

from .core import plan_renames, slugify


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="slugify-cli",
        description="Convert text to URL-safe slugs, or slugify filenames in a directory.",
    )
    parser.add_argument(
        "text", nargs="*", help="Text to slugify, one slug per argument (if omitted, reads lines from stdin)"
    )
    parser.add_argument(
        "--rename", metavar="DIR", help="Slugify filenames in DIR instead of slugifying text arguments/stdin"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the renames planned by --rename (default is a dry run)",
    )
    parser.add_argument("--separator", default="-", help="Separator character to use in slugs (default: -)")
    return parser


def _slugify_text(text_args: list[str], separator: str) -> int:
    if text_args:
        lines = text_args
    else:
        lines = [line.rstrip("\n") for line in sys.stdin]

    for line in lines:
        print(slugify(line, separator))
    return 0


def _rename_directory(directory: str, apply: bool, separator: str) -> int:
    if not os.path.isdir(directory):
        print(f"slugify-cli: error: not a directory: {directory}", file=sys.stderr)
        return 2

    names = sorted(n for n in os.listdir(directory) if os.path.isfile(os.path.join(directory, n)))
    renames = plan_renames(names, separator)

    if not renames:
        print("slugify-cli: no filenames need changes")
        return 0

    for old, new in renames:
        print(f"{old} -> {new}")

    if not apply:
        print(f"\nDry run: {len(renames)} file(s) would be renamed. Re-run with --apply to rename them.")
        return 0

    had_error = False
    for old, new in renames:
        try:
            os.rename(os.path.join(directory, old), os.path.join(directory, new))
        except OSError as exc:
            print(f"slugify-cli: error: could not rename '{old}': {exc}", file=sys.stderr)
            had_error = True

    if had_error:
        return 2

    print(f"\nRenamed {len(renames)} file(s).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.rename:
        return _rename_directory(args.rename, args.apply, args.separator)
    return _slugify_text(args.text, args.separator)


if __name__ == "__main__":
    raise SystemExit(main())
