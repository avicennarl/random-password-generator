# pwdgen

> Offline, cryptographically secure password and passphrase generator.

[![CI](https://github.com/avicennarl/random-password-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/avicennarl/random-password-generator/actions/workflows/ci.yml)
[![License: MPL-2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

`pwdgen` generates strong passwords and memorable passphrases using your
operating system's cryptographically secure random source. It has **no runtime
dependencies** and works **completely offline** — nothing is ever sent over the
network.

## Features

- 🔐 Secure randomness (`secrets` on the CLI, `crypto.getRandomValues()` on the web)
- 🎲 **Password mode** with configurable length and character classes
- 📝 **Passphrase mode** using the BIP39 English wordlist (2048 words)
- 📊 Entropy estimate (bits) and a human-readable strength label
- 👓 Option to exclude easily confused characters (`Il1O0o`)
- 🧾 `--json` output for scripting and automation
- 🌐 A static web build you can host anywhere (GitHub Pages included)

## Install

### pipx (recommended)

```bash
pipx install git+https://github.com/avicennarl/random-password-generator
```

### From source

```bash
git clone https://github.com/avicennarl/random-password-generator
cd random-password-generator
python -m pip install -e .
```

## Usage

```bash
# 20-character password (default: lowercase + uppercase + digits)
pwdgen -l 20

# include symbols, exclude ambiguous characters
pwdgen -l 24 -s --exclude-ambiguous

# a 4-word passphrase
pwdgen --passphrase --words 4

# ten passphrases, capitalized, with a number
pwdgen -p -w 5 --capitalize --number -n 10

# machine-readable output
pwdgen --json
```

```json
{
  "type": "password",
  "value": "HiricFJqPoWw5Ox1",
  "entropy_bits": 95.3,
  "strength": "strong"
}
```

### Options

| Flag | Description |
| --- | --- |
| `-l, --length` | Password length (default `16`) |
| `-n, --count` | Number of results (default `1`) |
| `-s, --symbols` | Include symbols |
| `--no-lower` / `--no-upper` / `--no-digits` | Exclude a character class |
| `--exclude-ambiguous` | Drop `I l 1 O 0 o` |
| `-p, --passphrase` | Generate a passphrase instead |
| `-w, --words` | Words per passphrase (default `4`) |
| `--separator` | Passphrase separator (default `-`) |
| `--capitalize` | Capitalize each word |
| `--number` | Insert a random digit into a passphrase |
| `--json` | Print JSON |

## Web version

A fully offline browser build lives in [`web/`](web). Open `web/index.html`
directly, or use the hosted version published to GitHub Pages. All generation
happens locally in your browser.

## Security

- Passwords and passphrases are generated with a cryptographically secure
  random number generator.
- `pwdgen` never stores, logs or transmits generated secrets.
- The passphrase wordlist is the standard [BIP39 English list](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md) (2048 words, MIT).

See [SECURITY.md](SECURITY.md) for the disclosure policy.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
