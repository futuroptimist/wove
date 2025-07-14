# 🧶 wove

[![Tests](https://img.shields.io/github/actions/workflow/status/futuroptimist/wove/ci.yml?label=tests)](https://github.com/futuroptimist/wove/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/futuroptimist/wove)](LICENSE)

**wove** aims to provide an open-source toolkit for learning to knit and for building a robotic knitting machine. Documentation in `docs/` walks through the basics of hand knitting while the `cad/` directory contains OpenSCAD files for printable hardware components.

## Getting Started

```bash
# clone your fork
git clone git@github.com:YOURNAME/wove.git
cd wove

# personalize badges and docs
./scripts/setup.sh YOURNAME wove

# create virtualenv and install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run checks
./scripts/checks.sh
```

See [AGENTS.md](AGENTS.md) for details on LLM helpers that keep this repo tidy. Contributions are welcome—see [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md). For AI helper context see [llms.txt](llms.txt).
