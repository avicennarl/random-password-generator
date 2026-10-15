# Security Policy

`pwdgen` generates secrets, so security is taken seriously.

## Supported versions

This project follows a rolling release model; the latest commit on `main`
is the only supported version.

## Reporting a vulnerability

Please **do not** open a public issue for security problems. Instead, use
GitHub's private reporting:

1. Go to the **Security** tab of this repository.
2. Click **Report a vulnerability**.
3. Describe the issue, including steps to reproduce, the affected version
   and the potential impact.

You can expect an initial response within **7 days**. Once a fix is
available it will be released and, if you wish, you will be credited.

## Scope

In scope:

- Weakness in how randomness is obtained or used.
- Situations where a generated secret could be biased, predictable or leak.
- Supply-chain issues in this repository's own code.

Out of scope:

- The strength of secrets that users choose to reuse elsewhere.
- Vulnerabilities in third-party services hosting the web build.

## Design notes

- The CLI uses Python's `secrets` module (an OS-backed CSPRNG).
- The web build uses the Web Crypto API (`crypto.getRandomValues`) with
  rejection sampling to avoid modulo bias.
- Randomness is injectable purely for deterministic unit tests; production
  code paths never pass a custom generator.
