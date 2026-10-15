#compdef pwdgen

# zsh completion for pwdgen
# Install: place in one of your $fpath directories (or source it)

local -a opts
opts=(
  '(-h --help)'{-h,--help}'[show help]'
  '--version[show version]'
  '(-l --length)'{-l,--length}'[password length]'
  '(-n --count)'{-n,--count}'[number of results]'
  '--json[print JSON]'
  '--no-lower[exclude lowercase]'
  '--no-upper[exclude uppercase]'
  '--no-digits[exclude digits]'
  '(-s --symbols)'{-s,--symbols}'[include symbols]'
  '--exclude-ambiguous[drop ambiguous characters (Il1O0o)]'
  '(-p --passphrase)'{-p,--passphrase}'[generate passphrase]'
  '(-w --words)'{-w,--words}'[words per passphrase]'
  '--separator[word separator]'
  '--capitalize[capitalize each word]'
  '--number[insert a random digit]'
)

_arguments -s $opts
