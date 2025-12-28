from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_node(script: str) -> dict:
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        check=True,
    )
    return json.loads(result.stdout)


def test_format_file_size_formats_common_ranges() -> None:
    script = textwrap.dedent(
        """
        import { formatFileSize } from './viewer/src/format.js';

        const payload = {
          bytes: formatFileSize(512),
          kilobytes: formatFileSize(1536),
          oneMegabyte: formatFileSize(1024 * 1024),
          multiMegabytes: formatFileSize(2.5 * 1024 * 1024),
        };

        console.log(JSON.stringify(payload));
        """
    )

    result = run_node(script)

    assert result == {
        "bytes": "512 B",
        "kilobytes": "1.5 kB",
        "oneMegabyte": "1.00 MB",
        "multiMegabytes": "2.50 MB",
    }


def test_format_file_size_handles_small_and_invalid_inputs() -> None:
    script = textwrap.dedent(
        """
        import { formatFileSize } from './viewer/src/format.js';

        const values = [
          formatFileSize(0),
          formatFileSize(-5),
          formatFileSize('not-a-number'),
          formatFileSize(undefined),
          formatFileSize(Number.NaN),
        ];

        console.log(JSON.stringify({ values }));
        """
    )

    result = run_node(script)

    assert result["values"] == ["0 B", None, None, None, None]
