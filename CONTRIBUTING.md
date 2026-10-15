# Contributing to pwdgen

Thanks for taking the time to contribute! 🎉

## Development setup

```bash
git clone https://github.com/avicennarl/random-password-generator
cd random-password-generator

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Running the checks

```bash
pytest          # run the test suite
ruff check .    # lint
ruff format .   # optional formatting
```

Please make sure both `pytest` and `ruff check .` pass before opening a
pull request.

## Project layout

```
src/pwdgen/      CLI and core logic
src/pwdgen/data/ bundled wordlist
tests/           pytest suite
web/             static browser build
```

## Guidelines

- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `ci:`, `build:`, `test:`, `refactor:` …).
- **Tests** are required for behaviour changes; add or update cases in `tests/`.
- **Scope** — keep pull requests focused on a single change.
- **Docs** — update the README or `docs/` when you change user-facing behaviour.

## Reporting bugs and requesting features

Use the issue templates. For security issues, see [SECURITY.md](SECURITY.md)
instead — please do not file them publicly.
