"""Generate a Markdown summary of Codex prompt docs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repos-from",
        type=Path,
        required=True,
        help="Path to a text file containing repository names and roots.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output path for the generated summary Markdown file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from wove.prompt_summary import generate_summary, write_summary

    summary = generate_summary(args.repos_from)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_summary(args.out, summary)


if __name__ == "__main__":
    main()
