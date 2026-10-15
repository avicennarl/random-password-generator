# bash completion for pwdgen
# Install: source this file, or drop it in /usr/share/bash-completion/completions/pwdgen

_pwdgen_completions() {
  local cur opts
  cur="${COMP_WORDS[COMP_CWORD]}"
  opts="-h --help --version -l --length -n --count --json --no-lower --no-upper --no-digits -s --symbols --exclude-ambiguous -p --passphrase -w --words --separator --capitalize --number"
  # shellcheck disable=SC2207
  COMPREPLY=($(compgen -W "${opts}" -- "${cur}"))
  return 0
}

complete -F _pwdgen_completions pwdgen
