#Compiler version 2.2
import re

#CONSTANTS
EOF = "EOF"
PLUS = "PLUS"
MINUS = "MINUS"
INT = "INT"
DIVISION = "DIVISION"
MULTIPLICATION = "MULTIPLICATION"
OPEN_PARENTHESIS = "OPEN_PARENTHESIS"
CLOSE_PARENTHESIS = "CLOSE_PARENTHESIS"
ASSIGNMENT = "ASSIGNMENT"
OPEN_CURLY_BRACES = "OPEN_CURLY_BRACES"
CLOSE_CURLY_BRACES = "CLOSE_CURLY_BRACES"
SEMICOLON = "SEMICOLON"
IDENTIFIER = "IDENTIFIER"
PRINTF = "PRINTF"
COMMANDS = "COMMANDS"
EQUALS = "EQUALS"
GREATER_THAN = "GREATER_THAN"
LESS_THAN = "LESS_THAN"
AND = "AND"
OR = "OR"
NOT = "NOT"
IF = "IF"
ELSE = "ELSE"
WHILE = "WHILE"
SCANF = "SCANF"
MAIN = "MAIN"
TYPE = "TYPE"
INT_TYPE = "INT_TYPE"
CHAR_TYPE = "CHAR_TYPE"
VOID_TYPE = "VOID_TYPE"

#ERRORS
operatorError = "A non-digit followed a operator"
operatorAbsenceError = "A non-operator followed a digit"
digitAbsenceError = "A non-digit character started the command"
commentNotCloseException = "A comment was started but closing symbol '*/' is missing "
spaceInBetweenDigitsException = "Does not accept space in between digits without operators"
parenthesNotOpenExceptionPrint = "Parenthesis was not open after print"
parenthesNotOpenExceptionIf = "Parenthesis was not open after if"
parenthesNotOpenExceptionWhile = "Parenthesis was not open after while"
parenthesNotOpenExceptionFunction = "Parenthesis was not open after function"
parenthesisNotClosedException = "Parenthesis was not closed"
curlyBracesNotClosedException = "Curly Braces was not closed"
noBlockException = "No block was declared, '{' "
commandNotClosedException = "Missing semicolon"
assignmentContainsNoIdentifier = "assignment Contains No Identifier"
commandAbsenceTreatment = "Values not treated by command"
NotEndOfFileExpection = "Concludes before the end of the file"
notTypeException = "Expected a type"
notMainException = "Expected a Main Function"
referencedBeforeAssignedException = "Variable referenced before assigned."
declaredButNotAssignedException = "Variable declared but not assigned"
doubleDeclarationException = "Variable declared multiple times"
differentTypesOperationException = "Operation executed between different types"

#VALUES
type_words = {"int":INT_TYPE, "char":CHAR_TYPE, "void":VOID_TYPE}
reserved_words = {"printf":PRINTF, "if":IF, "while":WHILE, "else":ELSE, "scanf":SCANF, "main":MAIN, "int":TYPE, "char":TYPE, "void":TYPE}

#ASSEMBLY
init_assembly = [
"; constants",
"SYS_EXIT equ 1",
"SYS_READ equ 3",
"SYS_WRITE equ 4",
"STDIN equ 0",
"STDOUT equ 1",
"True equ 1",
"False equ 0",
"segment .data",
"segment .bss ; variables"
]
default_function_declarations_assembly = [
"res RESB 1",
"section .text",
"global _start",
"print :  ; print",
"POP EBX",
"POP EAX",
"PUSH EBX",
"XOR ESI, ESI",
"print_dec :",
"MOV EDX, 0",
"MOV EBX, 0x000A",
"DIV EBX",
"ADD EDX, '0'",
"PUSH EDX",
"INC ESI",
"CMP EAX, 0",
"JZ print_next",
"JMP print_dec",
"print_next :",
"CMP ESI, 0",
"JZ print_exit",
"DEC ESI",
"MOV EAX, SYS_WRITE",
"MOV EBX, STDOUT",
"POP ECX",
"MOV [res], ECX",
"MOV ECX, res",
"MOV EDX, 1",
"INT 0x80",
"JMP print_next",
"print_exit :",
"RET",
"; subrotinas if/while",
"binop_je :",
"JE binop_true",
"JMP binop_false",
"binop_jg :",
"JG binop_true",
"JMP binop_false",
"binop_jl :",
"JL binop_true",
"JMP binop_false",
"binop_false :",
"MOV EBX, False",
"JMP binop_exit",
"binop_true :",
"MOV EBX, True",
"binop_exit : RET",
"_start :"
]
end = [
"; end interrupt",
"MOV EAX, 1",
"INT 0x80"
]

class Assembly:
    id = 0
    assembly_commands = []
    variable_declaration = []

    @staticmethod
    def get_ID():
        res = Assembly.id
        Assembly.id += 1
        return res

    @staticmethod
    def write():
        with open("program.asm", "w") as fw:
            for write_list in [init_assembly, Assembly.variable_declaration, default_function_declarations_assembly, Assembly.assembly_commands, end]:
                for line in write_list:
                    fw.write(line + '\n')
            
            # fw.write(line + '\n' for line in init_assembly) 
            # fw.write(line + '\n' for line in Assembly.variable_declaration) #VARIABLE DECLARATIONS
            # fw.write(line + '\n' for line in default_function_declarations_assembly)
            # fw.write(line + '\n' for line in Assembly.assembly_commands) #COMMANDS
            # fw.write(line + '\n' for line in end)

class Token:
    def __init__(self, value, var_type):
        self.value = value
        self.var_type = var_type

class Node:
    def __init__(self):
        self.id = Assembly.get_ID()
        self.value = None
        self.children = []
    def Evaluate(self,SymbolTable):
        pass

class BinOp(Node):
    def __init__(self,var_type,children):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.children = children
    def Evaluate(self,SymbolTable):
        if self.value == ASSIGNMENT:
            res = self.children[1].Evaluate(SymbolTable)
            assignment = "MOV [{0}_1], EBX".format(self.children[0].name)
            res.append(assignment)
        else:
            res = self.children[0].Evaluate(SymbolTable)
            res.append("PUSH EBX")
            right = self.children[1].Evaluate(SymbolTable)
            res += right
            res.append("POP EAX")
            if self.value == PLUS:
                res.append("ADD EAX, EBX")
                res.append("MOV EBX, EAX")
            elif self.value == MINUS:
                res.append("SUB EAX, EBX")
                res.append("MOV EBX, EAX")
            elif self.value == MULTIPLICATION:
                res.append("IMUL EAX, EBX")
                res.append("MOV EBX, EAX")
            elif self.value == DIVISION:
                res.append("IDIV EAX, EBX")
                res.append("MOV EBX, EAX")
            elif self.value == AND:
                res.append("AND EAX, EBX")
                res.append("MOV EBX, EAX")
            elif self.value == OR:
                res.append("OR EAX, EBX")
                res.append("MOV EBX, EAX")
            elif self.value == EQUALS:
                res.append("CMP EAX, EBX")
                res.append("CALL binop_je")
            elif self.value == GREATER_THAN:
                res.append("CMP EAX, EBX")
                res.append("CALL binop_jg")
            elif self.value == LESS_THAN:
                res.append("CMP EAX, EBX")
                res.append("CALL binop_jl")
        return res

class UnOp(Node):
    def __init__(self,var_type,child):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.children = [child]
    def Evaluate(self, SymbolTable):
        child, val_type = self.children[0].Evaluate(SymbolTable)
        if self.value == PLUS:
            return child, val_type
        elif self.value == MINUS:
            return -(child), val_type
        elif self.value == NOT:
            return not child, val_type

class IntVal(Node):
    def __init__(self,value):
        self.id = Assembly.get_ID()
        self.value = value
    def Evaluate(self, SymbolTable):
        result = "MOV EBX, {0}".format(self.value)
        return [result]

class Identifier(Node):
    def __init__(self,name,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.name = name
    def Evaluate(self,SymbolTable):
        # value = SymbolTable.get_value(self.name)
        result = "MOV EBX, [{0}_1]".format(self.name)
        # var_type = SymbolTable.get_type(self.name)
        return [result]

class Printf(Node):
    def __init__(self,child,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.child = child
    def Evaluate(self,SymbolTable):
        res = self.child.Evaluate(SymbolTable)
        res.append("PUSH EBX")
        res.append("CALL print")
        return res

class Scanf(Node):
    def __init__(self,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
    def Evaluate(self,SymbolTable):
        return int(input()), INT_TYPE

class Declaration(Node):
    def __init__(self,var_type,child):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.children = [child]
    def Evaluate(self, SymbolTable):
        result = ["{0}_1 RESD 1".format(self.children[0].name)]
        return result
        
class Commands(Node):
    def __init__(self,children,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.children = children
    def Evaluate(self, SymbolTable, main = True):
        result = []
        for child in self.children:
            res = child.Evaluate(SymbolTable)
            if main:
                if type(child) is Declaration:
                    for line in res:
                        Assembly.variable_declaration.append(line)  
                else:  
                    for line in res:
                        Assembly.assembly_commands.append(line)
            else:
                for line in res:
                    result.append(line)
        return result

class IfCondition(Node):
    def __init__(self,children,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.children = children
    def Evaluate(self, SymbolTable):
        # if self.children[0].Evaluate(SymbolTable):
        #     self.children[1].Evaluate(SymbolTable)
        # else: 
        #     self.children[2].Evaluate(SymbolTable)
        res = ["IF_{0}".format(self.id)]
        res += self.children[0].Evaluate(SymbolTable)
        res.append("CMP EBX, False")
        res.append("JE ELSE_{0}".format(self.id))
        res += self.children[1].Evaluate(SymbolTable, False)
        res.append("JMP EXIT_{0}".format(self.id))
        res = ["ELSE_{0}".format(self.id)]
        res += self.children[2].Evaluate(SymbolTable, False)
        res.append("EXIT_{0}".format(self.id))
        return res

class WhileLoop(Node):
    def __init__(self,children,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
        self.children = children
    def Evaluate(self, SymbolTable):
        res = ["LOOP_{0}".format(self.id)]
        res += self.children[0].Evaluate(SymbolTable)
        res.append("CMP EBX, False")
        res.append("JE EXIT_{0}".format(self.id))
        res += self.children[1].Evaluate(SymbolTable, False)
        res.append("JMP LOOP_{0}".format(self.id))
        res.append("EXIT_{0}".format(self.id))
        return res

class NoOp(Node):
    def __init__(self,var_type):
        self.id = Assembly.get_ID()
        self.value = var_type
    def Evaluate(self,SymbolTable):
        pass

class SymbolTable:
    table = {}
    def __init__(self):
        pass
    def set_value(self,identifier,value_type):
        if identifier not in SymbolTable.table:
            Exception(referencedBeforeAssignedException)
        else:
            if SymbolTable.table[str(identifier)][1] == value_type[1]:
                SymbolTable.table[str(identifier)][0] = int(value_type[0])

    def set_type(self,identifier,var_type):
        if identifier not in SymbolTable.table:
            SymbolTable.table[str(identifier)] = [None, str(var_type)]
        else:
            if SymbolTable.table[str(identifier)][1] is not None:
                Exception(doubleDeclarationException)

    def get_value(self,identifier):
        if SymbolTable.table[str(identifier)] is None:
            Exception(declaredButNotAssignedException)
        else:
            return SymbolTable.table[str(identifier)][0]

    def get_type(self,identifier):
        if SymbolTable.table[str(identifier)] is None:
            Exception(declaredButNotAssignedException)
        else:
            return SymbolTable.table[str(identifier)][1]

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.current_token = None
    def selectNextToken(self):
        value = ""
        isDigit = False
        isWord = False
        if self.position >= len(self.origin):
            self.current_token = Token("", EOF)
            return
        while self.position < len(self.origin) and self.origin[self.position] == " ":
            self.position += 1
        while self.position < len(self.origin) and self.origin[self.position].isdigit():
            value += self.origin[self.position]
            self.position += 1
            isDigit = True
        if isDigit:
            self.current_token = Token(int(value), INT)
            return
        if self.origin[self.position].isalpha():
            value += self.origin[self.position]
            self.position += 1
            isWord = True
            while self.position < len(self.origin) and (self.origin[self.position].isdigit() or self.origin[self.position].isalpha() or self.origin[self.position] == '_'):
                value += self.origin[self.position]
                self.position += 1
        if isWord:
            if value in reserved_words:
                self.current_token = Token(value, reserved_words[value])
            else:    
                self.current_token = Token(value, IDENTIFIER)
            return
        if self.origin[self.position] == "+":
            value = "+"
            self.position += 1
            self.current_token = Token(value, PLUS)
            return
        if self.origin[self.position] == "-":
            value = "-"
            self.position += 1
            self.current_token = Token(value, MINUS)
            return
        if self.origin[self.position] == "/":
            value = "/"
            self.position += 1
            self.current_token = Token(value, DIVISION)
            return
        if self.origin[self.position] == "*":
            value = "*"
            self.position += 1
            self.current_token = Token(value, MULTIPLICATION)
            return
        if self.origin[self.position] == "(":
            value = "("
            self.position += 1
            self.current_token = Token(value, OPEN_PARENTHESIS)
            return
        if self.origin[self.position] == ")":
            value = ")"
            self.position += 1
            self.current_token = Token(value, CLOSE_PARENTHESIS)
            return
        if self.origin[self.position] == "=":
            value = "="
            self.position += 1
            if self.origin[self.position] == "=":
                self.position += 1
                self.current_token = Token(value + "=", EQUALS)
            else:
                self.current_token = Token(value + "=", ASSIGNMENT)
            return
        if self.origin[self.position] == "{":
            value = "{"
            self.position += 1
            self.current_token = Token(value, OPEN_CURLY_BRACES)
            return
        if self.origin[self.position] == "}":
            value = "}"
            self.position += 1
            self.current_token = Token(value, CLOSE_CURLY_BRACES)
            return
        if self.origin[self.position] == ";":
            value = ";"
            self.position += 1
            self.current_token = Token(value, SEMICOLON)
            return
        if self.origin[self.position] == ">":
            value = ">"
            self.position += 1
            self.current_token = Token(value, GREATER_THAN)
            return
        if self.origin[self.position] == "<":
            value = "<"
            self.position += 1
            self.current_token = Token(value, LESS_THAN)
            return
        if self.origin[self.position] == "!":
            value = "!"
            self.position += 1
            self.current_token = Token(value, NOT)
            return
        if self.origin[self.position] == "&":
            value = "&"
            self.position += 1
            if self.origin[self.position] == "&":
                self.position += 1
                self.current_token = Token(value + "&", AND)
            else:
                Exception(digitAbsenceError)
            return
        if self.origin[self.position] == "|":
            value = "|"
            self.position += 1
            if self.origin[self.position] == "|":
                self.position += 1
                self.current_token = Token(value + "|", OR)
            else:
                Exception(digitAbsenceError)
            return
        raise Exception(digitAbsenceError)

class PreProcessing:
    @staticmethod
    def process(command):
        # return PreProcessing.removeComments(PreProcessing.removeSpaces(command))
        return PreProcessing.removeComments(command)
        
    @staticmethod
    def removeSpaces(command):
        extra_init_comment = re.search('[0-9] +[0-9]', command)
        if extra_init_comment:
            raise Exception(spaceInBetweenDigitsException)
        else:
            processed_command = command.replace(" ","") #to be improved later
        return processed_command

    @staticmethod
    def removeComments(command):
        processed_command = re.sub('/\*(.*?)\*/', '', command)
        extra_init_comment = re.search('/\*', processed_command)
        if extra_init_comment:
            raise Exception(commentNotCloseException)
        return processed_command

class Analyser:
    tokens = None
    @staticmethod
    def init(origin):
        Analyser.tokens = Tokenizer(origin)
        Analyser.tokens.selectNextToken()
        
    #ASSIGNMENT
    @staticmethod     
    def assignmentTreatment(left_child):
        Analyser.tokens.selectNextToken() 
        if Analyser.tokens.current_token.var_type == ASSIGNMENT:
            Analyser.tokens.selectNextToken()
            #SCANF
            if Analyser.tokens.current_token.var_type == SCANF:
                Analyser.tokens.selectNextToken() 
                if Analyser.tokens.current_token.var_type == OPEN_PARENTHESIS:
                    Analyser.tokens.selectNextToken()
                    result = BinOp(ASSIGNMENT, [left_child,Scanf(SCANF)])
                    if Analyser.tokens.current_token.var_type != CLOSE_PARENTHESIS:
                        Exception(parenthesisNotClosedException)
                    else:
                        Analyser.tokens.selectNextToken() 
                else:
                    Exception(parenthesNotOpenExceptionPrint)
            else:
                result = BinOp(ASSIGNMENT, [left_child,Analyser.expressionTreatment()])
        else:
            Exception(assignmentContainsNoIdentifier)
        return result

    #Integers
    @staticmethod
    def factorTreatment():
        # Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.var_type == INT:
            result = IntVal(Analyser.tokens.current_token.value)
            Analyser.tokens.selectNextToken()
        elif Analyser.tokens.current_token.var_type == PLUS or Analyser.tokens.current_token.var_type == MINUS:
            curr_type = Analyser.tokens.current_token.var_type
            Analyser.tokens.selectNextToken()
            result = UnOp(curr_type, Analyser.factorTreatment())
        elif Analyser.tokens.current_token.var_type == OPEN_PARENTHESIS:
            Analyser.tokens.selectNextToken()
            result = Analyser.expressionTreatment()
            if Analyser.tokens.current_token.var_type != CLOSE_PARENTHESIS:
                Exception(parenthesisNotClosedException)                
            else:
                Analyser.tokens.selectNextToken()
        elif Analyser.tokens.current_token.var_type == IDENTIFIER:
            curr_value = Analyser.tokens.current_token.value
            Analyser.tokens.selectNextToken()
            result = Identifier(curr_value, IDENTIFIER)
        else:
            raise Exception(digitAbsenceError)
        return result

    @staticmethod
    def termTreatment():
        result = Analyser.factorTreatment()
        while(Analyser.tokens.current_token.var_type == MULTIPLICATION or Analyser.tokens.current_token.var_type == DIVISION):
            curr_type = Analyser.tokens.current_token.var_type
            Analyser.tokens.selectNextToken()
            result = BinOp(curr_type, [result,Analyser.factorTreatment()])
        return result

    @staticmethod     
    def expressionTreatment():
        result = Analyser.termTreatment()
        while(Analyser.tokens.current_token.var_type == PLUS or Analyser.tokens.current_token.var_type == MINUS):
            curr_type = Analyser.tokens.current_token.var_type
            Analyser.tokens.selectNextToken()
            result = BinOp(curr_type, [result,Analyser.termTreatment()])
        return result

    @staticmethod
    def relationalExpression():
        left_child  = Analyser.expressionTreatment()
        BinOp_type = Analyser.tokens.current_token.var_type
        Analyser.tokens.selectNextToken()
        right_child = Analyser.expressionTreatment()
        return BinOp(BinOp_type, [left_child, right_child])

    #Boolean
    @staticmethod
    def booleanFactorTreatment():
        Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.var_type == NOT:
            result = UnOp(Analyser.tokens.current_token.var_type, Analyser.booleanFactorTreatment())
        else:
            result = Analyser.relationalExpression()
        # Analyser.tokens.selectNextToken()
        return result

    @staticmethod
    def booleanTermTreatment():
        result = Analyser.booleanFactorTreatment()
        while(Analyser.tokens.current_token.var_type == AND):
            result = BinOp(Analyser.tokens.current_token.var_type, [result,Analyser.booleanFactorTreatment()])
        return result

    @staticmethod     
    def booleanExpressionTreatment():
        result = Analyser.booleanTermTreatment()
        while(Analyser.tokens.current_token.var_type == OR):
            result = BinOp(Analyser.tokens.current_token.var_type, [result,Analyser.booleanTermTreatment()])
        return result

    @staticmethod     
    def commandTreatment():
        #COMMANDS
        if Analyser.tokens.current_token.var_type == OPEN_CURLY_BRACES:
            result = Analyser.commandsTreatment()
        #PRINTF
        elif Analyser.tokens.current_token.var_type == PRINTF:
            Analyser.tokens.selectNextToken() 
            if Analyser.tokens.current_token.var_type == OPEN_PARENTHESIS:
                result = Printf(Analyser.expressionTreatment(),PRINTF)
                if Analyser.tokens.current_token.var_type != CLOSE_PARENTHESIS:
                    Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken() 
            else:
                Exception(parenthesNotOpenExceptionPrint)
        #IF
        elif Analyser.tokens.current_token.var_type == IF:
            Analyser.tokens.selectNextToken()
            params = []
            if Analyser.tokens.current_token.var_type == OPEN_PARENTHESIS:
                result = Analyser.booleanExpressionTreatment()
                params.append(result)
                if Analyser.tokens.current_token.var_type != CLOSE_PARENTHESIS:
                    Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.var_type == OPEN_CURLY_BRACES:
                        true_child = Analyser.commandsTreatment()
                        params.append(true_child)
                        if Analyser.tokens.current_token.var_type == ELSE:
                            Analyser.tokens.selectNextToken()
                            false_child = Analyser.commandsTreatment()
                            params.append(false_child)
                        result = IfCondition(params, IF)
                    else:
                        Exception(parenthesNotOpenExceptionIf)
            else:
                Exception(parenthesNotOpenExceptionIf)
        #WHILE
        elif Analyser.tokens.current_token.var_type == WHILE:
            Analyser.tokens.selectNextToken()
            params = []
            if Analyser.tokens.current_token.var_type == OPEN_PARENTHESIS:
                result = Analyser.booleanExpressionTreatment()
                params.append(result)
                if Analyser.tokens.current_token.var_type != CLOSE_PARENTHESIS:
                    Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.var_type == OPEN_CURLY_BRACES:
                        true_child = Analyser.commandsTreatment()
                        params.append(true_child)
                        result = WhileLoop(params, WHILE)
                    else:
                        Exception(parenthesNotOpenExceptionWhile)
            else:
                Exception(parenthesNotOpenExceptionWhile)
        #DECLARATION
        elif Analyser.tokens.current_token.var_type == TYPE:
            var_type = type_words[Analyser.tokens.current_token.value]
            Analyser.tokens.selectNextToken()
            if Analyser.tokens.current_token.var_type == IDENTIFIER:
                identifier = Identifier(Analyser.tokens.current_token.value, IDENTIFIER)
                result = Declaration(var_type, identifier)
                Analyser.tokens.selectNextToken()
        #ASSIGNMENT
        elif Analyser.tokens.current_token.var_type == IDENTIFIER:
            left_child = Identifier(Analyser.tokens.current_token.value, IDENTIFIER)
            result = Analyser.assignmentTreatment(left_child)
        else:
            raise Exception(commandAbsenceTreatment)
        return result

    @staticmethod     
    def commandsTreatment():
        if Analyser.tokens.current_token.var_type == OPEN_CURLY_BRACES:
            children = []
            Analyser.tokens.selectNextToken()
            while Analyser.tokens.current_token.var_type != CLOSE_CURLY_BRACES:
                children.append(Analyser.commandTreatment())
                if Analyser.tokens.current_token.var_type == SEMICOLON:
                    Analyser.tokens.selectNextToken() 
                else:
                    Exception(commandNotClosedException)
            result = Commands(children, None)
            Analyser.tokens.selectNextToken()
            return result
        else:
            Exception(noBlockException)

    @staticmethod     
    def programTreatment():
        if Analyser.tokens.current_token.var_type == TYPE:
            var_type = type_words[Analyser.tokens.current_token.value]
            Analyser.tokens.selectNextToken() 
            if Analyser.tokens.current_token.var_type == MAIN:
                Analyser.tokens.selectNextToken() 
                if Analyser.tokens.current_token.var_type == OPEN_PARENTHESIS:
                    Analyser.tokens.selectNextToken() 
                    if Analyser.tokens.current_token.var_type == CLOSE_PARENTHESIS:
                        Analyser.tokens.selectNextToken()
                        return Analyser.commandsTreatment()
                    else:
                        Exception(parenthesisNotClosedException)
                else:
                    Exception(parenthesNotOpenExceptionFunction)     
            else:
                Exception(notMainException)
        else:
            Exception(notTypeException)


if __name__ == "__main__":
    with open("input.c","r", encoding='utf-8') as input_file:
        program = input_file.read()
        program = program.replace('\n',' ')
        program = program.replace(' ',' ')
        processed_command = PreProcessing.process(program)
        Analyser.init(processed_command)
        if(Analyser.tokens.current_token.var_type != EOF):
            Exception(NotEndOfFileExpection)
        ST = SymbolTable()
        Analyser.programTreatment().Evaluate(ST)
        Assembly.write()