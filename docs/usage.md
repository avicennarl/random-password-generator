# Usage

Detailed guide to the `pwdgen` command line interface and the web build.

## Password mode

Generate a random password from a pool of characters.

```bash
pwdgen -l 24 -s
```

| Flag | Default | Description |
| --- | --- | --- |
| `-l, --length` | `16` | Number of characters |
| `-n, --count` | `1` | How many passwords to print |
| `-s, --symbols` | off | Include symbols |
| `--no-lower` | off | Exclude lowercase letters |
| `--no-upper` | off | Exclude uppercase letters |
| `--no-digits` | off | Exclude digits |
| `--exclude-ambiguous` | off | Remove `I l 1 O 0 o` to avoid confusion |

At least one character class must remain enabled.

## Passphrase mode

Generate a passphrase from the BIP39 English wordlist.

```bash
pwdgen --passphrase --words 5 --separator . --capitalize --number
```

| Flag | Default | Description |
| --- | --- | --- |
| `-p, --passphrase` | off | Enable passphrase mode |
| `-w, --words` | `4` | Number of words |
| `--separator` | `-` | Separator between words |
| `--capitalize` | off | Capitalize each word |
| `--number` | off | Insert one random digit |

A four-word passphrase is roughly 44 bits of entropy; six words is ~66 bits.

## JSON output

Add `--json` for scripting. A single result prints as an object; multiple
results (with `-n`) print as an array.

```bash
pwdgen -l 20 --json
```

```json
{
  "type": "password",
  "value": "HiricFJqPoWw5Ox1",
  "entropy_bits": 95.3,
  "strength": "strong"
}
```

## Web build

Open `web/index.html` in any modern browser, or use the GitHub Pages
deployment. The web build mirrors the CLI (password and passphrase modes)
and runs entirely offline using `crypto.getRandomValues()`.

## Understanding the strength label

| Entropy | Label |
| --- | --- |
| < 28 bits | very weak |
| 28–35 bits | weak |
| 36–59 bits | reasonable |
| 60–127 bits | strong |
| ≥ 128 bits | very strong |
