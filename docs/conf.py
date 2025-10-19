import os
import re
import sys

from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Number, Text
from sphinx.highlighting import lexers

sys.path.insert(0, os.path.abspath(".."))

project = "wove"

extensions = [
    "myst_parser",
]

html_theme = "furo"

exclude_patterns = ["_build"]

html_static_path = ["_static"]


class PatternCliLexer(RegexLexer):
    """Minimal syntax highlighting for the pattern CLI DSL."""

    name = "Pattern CLI"
    aliases = ["pattern-cli"]
    flags = re.IGNORECASE

    tokens = {
        "root": [
            (r"#.*$", Comment.Single),
            (r"\s+", Text),
            (
                r"(CHAIN|SLIP|SINGLE|DOUBLE|MOVE|TURN|PAUSE)\b",
                Keyword.Reserved,
            ),
            (r"-?\d+(?:\.\d+)?", Number.Float),
            (r".+", Text),
        ]
    }


lexers["pattern-cli"] = PatternCliLexer()
