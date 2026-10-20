#!/usr/bin/env python3
"""CLI entry point for conflict-marker."""
import argparse
import json
import sys

from scanner import scan_dir


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="conflict-marker",
        description="Find leftover Git conflict markers in a directory tree.",
    )
    parser.add_argument("path", nargs="?", default=".", help="root directory to scan")
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="NAME",
        help="directory or glob to ignore (repeatable)",
    )
    parser.add_argument(
        "--ext",
        action="append",
        default=[],
        metavar="EXT",
        help="only scan files with these extensions (repeatable, e.g. .py)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    findings = scan_dir(args.path, ignore=args.ignore, extensions=args.ext)

    if args.json:
        payload = [{"file": f, "line": ln, "marker": m} for f, ln, m in findings]
        print(json.dumps(payload, indent=2))
    else:
        for f, ln, m in findings:
            print(f"{f}:{ln}: {m}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
