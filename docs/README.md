---
orphan: true
---

# Documentation

To preview the documentation locally, install the dependencies and build the HTML site:

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html` in a browser.

- [Knitting Basics](knitting-basics.md)
- [Crochet Basics](crochet-basics.md)
- [Wove v1c Mechanical Crochet System Design](wove-v1c-design.md)
- [Robotic Knitting Machine](robotic-knitting-machine.md) – architecture, module parameters, and
  assembly simplifications for the automated knitting platform.
- [Pattern translation CLI](pattern-cli.md)
- [Gauge utilities](gauge.md)
- [Python Style Guide](styleguides/python.md)
- [Markdown Style Guide](styleguides/markdown.md)
- [Codex Prompt](prompts/codex/automation.md)
- [Codex Implement Prompt](prompts/codex/implement.md)
- [Codex Design Doc Upgrade Prompt](prompts/codex/design-doc-upgrade.md)
- [Codex CAD Prompt](prompts/codex/cad.md)
- [Testing](testing.md)
- [Prompt documentation summary](prompt-docs-summary.md)
