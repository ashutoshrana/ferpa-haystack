# Contributing to ferpa-haystack

Thank you for your interest in contributing. This project is a FERPA-compliant document filter for Haystack RAG pipelines, and we welcome contributions from the Haystack and higher-education AI community.

## Ways to Contribute

- **Bug reports** — open an issue with a minimal reproduction case
- **Feature requests** — open an issue describing the use case and expected behavior
- **Pull requests** — bug fixes, new features, documentation improvements, additional test coverage
- **Peer review** — review open pull requests and leave feedback

## Getting Started

### Prerequisites

- Python 3.10, 3.11, or 3.12
- [Hatch](https://hatch.pypa.io/) for environment and test management

```bash
pip install hatch
```

### Setup

```bash
git clone https://github.com/ashutoshrana/ferpa-haystack.git
cd ferpa-haystack
hatch env create
```

### Run Tests

```bash
hatch run test
```

### Run Linter

```bash
hatch run lint
```

All tests must pass and lint must be clean before a PR will be reviewed.

## Project Structure

```
src/
  haystack_integrations/
    components/
      filters/
        ferpa_filter/
          __init__.py
          __about__.py
          ferpa_metadata_filter.py   ← main component
tests/
  test_ferpa_metadata_filter.py
examples/
  basic_pipeline.py
```

## Submitting a Pull Request

1. Fork the repository and create a branch from `main`.
2. Make your changes with clear, focused commits.
3. Add or update tests for any changed behavior.
4. Ensure `hatch run test` and `hatch run lint` both pass locally.
5. Open a pull request against `main` with a clear description of what changed and why.

## Issue Labels

| Label | Meaning |
|-------|---------|
| `good first issue` | Beginner-friendly — no deep codebase knowledge needed |
| `help wanted` | Maintainer is actively seeking contributions |
| `bug` | Confirmed defect with documented behavior |
| `enhancement` | New feature or improvement to existing behavior |
| `documentation` | Docs-only change |

## Code Style

- Line length: 120 characters (enforced by ruff)
- Type hints required on all public functions
- No comments explaining *what* code does — only *why* when non-obvious

## Regulatory Context

This project enforces 34 CFR § 99 (FERPA). If you are adding or changing filtering logic, please reference the specific regulation section in your PR description. Incorrect filtering behavior is a compliance defect, not just a functional bug.

## Code of Conduct

Be respectful and constructive. Maintainers will close issues or PRs that are dismissive, harassing, or off-topic without warning.

## Questions

Open an issue with the `question` label or start a [GitHub Discussion](https://github.com/ashutoshrana/ferpa-haystack/discussions).
