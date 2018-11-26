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
![program](DS/DS1.png =250x)
### Commands
![DS](DS/DS2.png =250x)
### Type
![DS](DS/DS3.png =250x)
### Command
![DS](DS/DS4.png =250x)
### if
![DS](DS/DS5.png =250x)
### while
![DS](DS/DS6.png =250x)
### return
![DS](DS/DS7.png =250x)
### Declaration
![DS](DS/DS8.png =250x)
### Attribution
![DS](DS/DS9.png =250x)
### Printf
![DS](DS/DS10.png =250x)
### Expression
![DS](DS/DS11.png =250x)
### Term
![DS](DS/DS12.png =250x)
### Factor
![DS](DS/DS13.png =250x)
### Bool_Expression
![DS](DS/DS14.png =250x)
### Bool_Term
![DS](DS/DS15.png =250x)
### Bool_Factor
![DS](DS/DS16.png =250x)
### Func_Call
![DS](DS/DS17.png =250x)