# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Secure password generation built on Python's `secrets` module.
- Passphrase mode backed by the bundled BIP39 English wordlist (2048 words).
- `pwdgen` command line interface with character-class options,
  `--exclude-ambiguous`, `--json`, and passphrase flags.
- Entropy estimate (bits) and human-readable strength label.
- Static offline web build under `web/`.
- Continuous integration (ruff + pytest) and GitHub Pages deployment.
- Packaging with `pyproject.toml` (installable via pipx/pip).

[Unreleased]: https://github.com/avicennarl/random-password-generator/commits/main
