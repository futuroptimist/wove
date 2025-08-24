# Testing

Run local checks to keep the project healthy.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run checks

Use pre-commit to lint, format, and validate docs:

```bash
pre-commit run --all-files
```

Run the test suite:

```bash
pytest
```
