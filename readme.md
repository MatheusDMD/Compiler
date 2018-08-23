# Compiler
Using python3

## EBNF

n -> number token
expression = n, { (“*” | “/”), n}, { (“+” | “-”), n, { (“*” | “/”), n}} ;

## Syntactic diagram

![Syntactic diagram](https://raw.githubusercontent.com/MatheusDMD/Compiler/master/images/syntactic%20diagram.png)