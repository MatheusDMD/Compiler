# Compiler

## EBNF

n -> number token
expression = n, { (“*” | “/”), n}, { (“+” | “-”), n, { (“*” | “/”), n}} ;