# Compiler
Using python3

## EBNF

program = type, identifier, "(" ((type, identifier), ',')+ ")", commands ;

commands = “{”, command, “;”, { command, “;” }, “}” ;

command = assignment | commands | printf | if | while | declaration ;

assignment = identifier, “=”, expression | scanf | function_call ;

function_call = identifier, "(" ,((expression) ",")+, ")" ;

scanf = "scanf", “(”,“)” ;

printf = "printf", “(”, expression, “)” ;

if = "if", “(”, bool_expression, “)”, commands ;

while = "while",“(”, bool_expression, “)”, commands ;

declaration = type, identifier, { "(" ((type, identifier), ',')+ ")", commands };

return = "return", "(", { ((expression), ",")+ },")"; 

type = "int" | "char" | "void" ;

expression = term, { (“+” | “-”), term } ;

term = factor, { (“*” | “/”), factor } ;

factor = (“+” | “-”), factor | num | “(”, expression, “)” | identifier ;

bool_expression = bool_term, { "||", bool_term } ;

bool_term = bool_factor, { “&&”, bool_factor } ;

bool_factor = { expression, (">" | "<" | "==" ), expression } | bool_factor ;

identifier = letter, { letter | digit | “_” } ;

num = digit, { digit } ;

letter = ( a | ... | z | A | ... | Z ) ;

digit = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
## Syntactic diagram
### Program
![program](DS/DS1.png)
### Commands
![DS](DS/DS2.png)
### Type
![DS](DS/DS3.png)
### Command
![DS](DS/DS4.png)
### if
![DS](DS/DS5.png)
### while
![DS](DS/DS6.png)
### return
![DS](DS/DS7.png)
### Declaration
![DS](DS/DS8.png)
### Attribution
![DS](DS/DS9.png)
### Printf
![DS](DS/DS10.png)
### Expression
![DS](DS/DS11.png)
### Term
![DS](DS/DS12.png)
### Factor
![DS](DS/DS13.png)
### Bool_Expression
![DS](DS/DS14.png)
### Bool_Term
![DS](DS/DS15.png)
### Bool_Factor
![DS](DS/DS16.png)
### Func_Call
![DS](DS/DS17.png)