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

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Node:
    def __init__(self):
        self.value = None
        self.children = []
    def Evaluate(self,SymbolTable):
        pass

class BinOp(Node):
    def __init__(self,type,children):
        self.value = type
        self.children = children
    def Evaluate(self,SymbolTable):
        if self.value == ASSIGNMENT:
            SymbolTable.set_value(self.children[0].name, self.children[1].Evaluate(SymbolTable))
            return
        left = self.children[0].Evaluate(SymbolTable)
        right = self.children[1].Evaluate(SymbolTable)
        left_child = left[0]
        left_val_type = left[1]
        right_child = right[0]
        right_val_type = right[1]
        if left_val_type == right_val_type:
            if self.value == PLUS:
                return left_child + right_child, left_val_type
            elif self.value == MINUS:
                return left_child - right_child, left_val_type
            elif self.value == MULTIPLICATION:
                return left_child * right_child, left_val_type
            elif self.value == DIVISION:
                return left_child // right_child, left_val_type
            elif self.value == EQUALS:
                return left_child == right_child, left_val_type
            elif self.value == GREATER_THAN:
                return left_child > right_child, left_val_type
            elif self.value == LESS_THAN:
                return left_child < right_child, left_val_type
            elif self.value == AND:
                return left_child and right_child, left_val_type
            elif self.value == OR:
                return left_child or right_child, left_val_type
        else:
            Exception(differentTypesOperationException)

class UnOp(Node):
    def __init__(self,type,child):
        self.value = type
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
        self.value = value
    def Evaluate(self, SymbolTable):
        return self.value, INT_TYPE

class Identifier(Node):
    def __init__(self,name,type):
        self.value = type
        self.name = name
    def Evaluate(self,SymbolTable):
        value = SymbolTable.get_value(self.name)
        type = SymbolTable.get_type(self.name)
        return value, type

class Printf(Node):
    def __init__(self,child,type):
        self.value = type
        self.child = child
    def Evaluate(self,SymbolTable):
        print(self.child.Evaluate(SymbolTable)[0])

class Scanf(Node):
    def __init__(self,type):
        self.value = type
    def Evaluate(self,SymbolTable):
        return int(input()), INT_TYPE

class Declaration(Node):
    def __init__(self,type,child):
        self.value = type
        self.children = [child]
    def Evaluate(self, SymbolTable):
        SymbolTable.set_type(self.children[0].name, self.value)

class Commands(Node):
    def __init__(self,children,type):
        self.value = type
        self.children = children
    def Evaluate(self, SymbolTable):
        for child in self.children:
            child.Evaluate(SymbolTable)

class IfCondition(Node):
    def __init__(self,children,type):
        self.value = type
        self.children = children
    def Evaluate(self, SymbolTable):
        if self.children[0].Evaluate(SymbolTable):
            self.children[1].Evaluate(SymbolTable)
        else: 
            self.children[2].Evaluate(SymbolTable)

class WhileLoop(Node):
    def __init__(self,children,type):
        self.value = type
        self.children = children
    def Evaluate(self, SymbolTable):
        while self.children[0].Evaluate(SymbolTable):
            self.children[1].Evaluate(SymbolTable)

class NoOp(Node):
    def __init__(self,type):
        self.value = type
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

    def set_type(self,identifier,type):
        if identifier not in SymbolTable.table:
            SymbolTable.table[str(identifier)] = [None, str(type)]
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
        if Analyser.tokens.current_token.type == ASSIGNMENT:
            Analyser.tokens.selectNextToken()
            #SCANF
            if Analyser.tokens.current_token.type == SCANF:
                Analyser.tokens.selectNextToken() 
                if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                    Analyser.tokens.selectNextToken()
                    result = BinOp(ASSIGNMENT, [left_child,Scanf(SCANF)])
                    if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
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
        if Analyser.tokens.current_token.type == INT:
            result = IntVal(Analyser.tokens.current_token.value)
            Analyser.tokens.selectNextToken()
        elif Analyser.tokens.current_token.type == PLUS or Analyser.tokens.current_token.type == MINUS:
            curr_type = Analyser.tokens.current_token.type
            Analyser.tokens.selectNextToken()
            result = UnOp(curr_type, Analyser.factorTreatment())
        elif Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
            Analyser.tokens.selectNextToken()
            result = Analyser.expressionTreatment()
            if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                Exception(parenthesisNotClosedException)                
            else:
                Analyser.tokens.selectNextToken()
        elif Analyser.tokens.current_token.type == IDENTIFIER:
            curr_value = Analyser.tokens.current_token.value
            Analyser.tokens.selectNextToken()
            result = Identifier(curr_value, IDENTIFIER)
        else:
            raise Exception(digitAbsenceError)
        return result

    @staticmethod
    def termTreatment():
        result = Analyser.factorTreatment()
        while(Analyser.tokens.current_token.type == MULTIPLICATION or Analyser.tokens.current_token.type == DIVISION):
            curr_type = Analyser.tokens.current_token.type
            Analyser.tokens.selectNextToken()
            result = BinOp(curr_type, [result,Analyser.factorTreatment()])
        return result

    @staticmethod     
    def expressionTreatment():
        result = Analyser.termTreatment()
        while(Analyser.tokens.current_token.type == PLUS or Analyser.tokens.current_token.type == MINUS):
            curr_type = Analyser.tokens.current_token.type
            Analyser.tokens.selectNextToken()
            result = BinOp(curr_type, [result,Analyser.termTreatment()])
        return result

    @staticmethod
    def relationalExpression():
        left_child  = Analyser.expressionTreatment()
        BinOp_type = Analyser.tokens.current_token.type
        Analyser.tokens.selectNextToken()
        right_child = Analyser.expressionTreatment()
        return BinOp(BinOp_type, [left_child, right_child])

    #Boolean
    @staticmethod
    def booleanFactorTreatment():
        Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.type == NOT:
            result = UnOp(Analyser.tokens.current_token.type, Analyser.booleanFactorTreatment())
        else:
            result = Analyser.relationalExpression()
        # Analyser.tokens.selectNextToken()
        return result

    @staticmethod
    def booleanTermTreatment():
        result = Analyser.booleanFactorTreatment()
        while(Analyser.tokens.current_token.type == AND):
            result = BinOp(Analyser.tokens.current_token.type, [result,Analyser.booleanFactorTreatment()])
        return result

    @staticmethod     
    def booleanExpressionTreatment():
        result = Analyser.booleanTermTreatment()
        while(Analyser.tokens.current_token.type == OR):
            result = BinOp(Analyser.tokens.current_token.type, [result,Analyser.booleanTermTreatment()])
        return result

    @staticmethod     
    def commandTreatment():
        #COMMANDS
        if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
            result = Analyser.commandsTreatment()
        #PRINTF
        elif Analyser.tokens.current_token.type == PRINTF:
            Analyser.tokens.selectNextToken() 
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                result = Printf(Analyser.expressionTreatment(),PRINTF)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken() 
            else:
                Exception(parenthesNotOpenExceptionPrint)
        #IF
        elif Analyser.tokens.current_token.type == IF:
            Analyser.tokens.selectNextToken()
            params = []
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                result = Analyser.booleanExpressionTreatment()
                params.append(result)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
                        true_child = Analyser.commandsTreatment()
                        params.append(true_child)
                        if Analyser.tokens.current_token.type == ELSE:
                            Analyser.tokens.selectNextToken()
                            false_child = Analyser.commandsTreatment()
                            params.append(false_child)
                        result = IfCondition(params, IF)
                    else:
                        Exception(parenthesNotOpenExceptionIf)
            else:
                Exception(parenthesNotOpenExceptionIf)
        #WHILE
        elif Analyser.tokens.current_token.type == WHILE:
            Analyser.tokens.selectNextToken()
            params = []
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                result = Analyser.booleanExpressionTreatment()
                params.append(result)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
                        true_child = Analyser.commandsTreatment()
                        params.append(true_child)
                        result = WhileLoop(params, WHILE)
                    else:
                        Exception(parenthesNotOpenExceptionWhile)
            else:
                Exception(parenthesNotOpenExceptionWhile)
        #DECLARATION
        elif Analyser.tokens.current_token.type == TYPE:
            type = type_words[Analyser.tokens.current_token.value]
            Analyser.tokens.selectNextToken()
            if Analyser.tokens.current_token.type == IDENTIFIER:
                identifier = Identifier(Analyser.tokens.current_token.value, IDENTIFIER)
                result = Declaration(type, identifier)
                Analyser.tokens.selectNextToken()
        #ASSIGNMENT
        elif Analyser.tokens.current_token.type == IDENTIFIER:
            left_child = Identifier(Analyser.tokens.current_token.value, IDENTIFIER)
            result = Analyser.assignmentTreatment(left_child)
        else:
            raise Exception(commandAbsenceTreatment)
        return result

    @staticmethod     
    def commandsTreatment():
        if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
            children = []
            Analyser.tokens.selectNextToken()
            while Analyser.tokens.current_token.type != CLOSE_CURLY_BRACES:
                children.append(Analyser.commandTreatment())
                if Analyser.tokens.current_token.type == SEMICOLON:
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
        if Analyser.tokens.current_token.type == TYPE:
            type = type_words[Analyser.tokens.current_token.value]
            Analyser.tokens.selectNextToken() 
            if Analyser.tokens.current_token.type == MAIN:
                Analyser.tokens.selectNextToken() 
                if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                    Analyser.tokens.selectNextToken() 
                    if Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
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
        if(Analyser.tokens.current_token.type != EOF):
            Exception(NotEndOfFileExpection)
        ST = SymbolTable()
        Analyser.programTreatment().Evaluate(ST)