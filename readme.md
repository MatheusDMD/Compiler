# Compiler
Using python3

## EBNF

expression = term, { (“+” | “-”), term } ;
term = factor, { (“*” | “/”), factor } ;
factor = (“+” | “-”) factor, number, “(” expression “)” ;
number = “-263” | ... | “263” ;

## Syntactic diagram

![Syntactic diagram](https://raw.githubusercontent.com/MatheusDMD/Compiler/master/images/syntactic%20diagram.png)