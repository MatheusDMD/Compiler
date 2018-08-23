# Compiler
Using python3

## EBNF

n -> number token
expression = n, { (“*” | “/”), n}, { (“+” | “-”), n, { (“*” | “/”), n}} ;

