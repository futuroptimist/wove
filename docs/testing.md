# Testing Guide

To keep the codebase stable, run the following commands before opening a pull request:

```bash
pre-commit run --all-files
pytest
```

`pre-commit` checks formatting, spelling, and links across the repository.
`pytest` runs unit tests in the `tests` directory.

Running these tools helps keep contributions consistent and reliable.
