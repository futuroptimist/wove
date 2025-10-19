#!/usr/bin/env python3
"""Serve the Three.js product assembly viewer.

This convenience script wraps ``http.server`` with sensible defaults so
contributors can preview ``viewer/index.html`` locally.
"""

from __future__ import annotations

import argparse
import functools
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIEWER_ROOT = PROJECT_ROOT / "viewer"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the Wove Three.js viewer")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind (default: 8000)",
    )
    parser.add_argument(
        "--directory",
        default=str(VIEWER_ROOT),
        help="Directory to serve (default: %(default)s)",
    )
    return parser.parse_args()


def run_server(host: str, port: int, directory: Path) -> None:
    if not directory.exists():
        raise SystemExit(f"Viewer directory not found: {directory}")

    handler_factory = functools.partial(
        SimpleHTTPRequestHandler,
        directory=str(directory),
    )
    server_address: Tuple[str, int] = (host, port)
    httpd = ThreadingHTTPServer(server_address, handler_factory)

    viewer_url = f"http://{host}:{port}/index.html"
    print(f"Serving Wove viewer from {directory}")
    print(
        "Open %s in your browser to explore the assembly line." % viewer_url
    )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down viewer server…")
    finally:
        httpd.server_close()


def main() -> None:
    args = parse_args()
    directory = Path(args.directory).resolve()

    # Ensure assets can reference relative paths when imported from tooling.
    os.chdir(directory)
    run_server(args.host, args.port, directory)


if __name__ == "__main__":
    main()
