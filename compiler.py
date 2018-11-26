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
FUNCTION = "FUNCTION"
COMMA = "COMMA"
RETURN = "RETURN"

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
missingCommaException = "Missing comma in function declaration"
numberOfArgumentsDoNotMatch = "Number of arguments in the function declaration doesn't match the number of arguments in the function call"

#VALUES
type_words = {"int":INT_TYPE, "char":CHAR_TYPE, "void":VOID_TYPE}
reserved_words = {"printf":PRINTF, "if":IF, "while":WHILE, "else":ELSE, "scanf":SCANF, "main":IDENTIFIER, "int":TYPE, "char":TYPE, "void":TYPE, "return": RETURN}

class Token:
    def __init__(self, value, var_type):
        self.value = value
        self.type = var_type

class Node:
    def __init__(self):
        self.value = None
        self.children = []
    def Evaluate(self,ST):
        pass

class BinOp(Node):
    def __init__(self,var_type,children):
        self.value = var_type
        self.children = children
    def Evaluate(self,ST):
        if self.value == ASSIGNMENT:
            ST.set_value(self.children[0].name, self.children[1].Evaluate(ST))
            return
        left = self.children[0].Evaluate(ST)
        right = self.children[1].Evaluate(ST)
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
                return left_child == right_child, CHAR_TYPE
            elif self.value == GREATER_THAN:
                return left_child > right_child, CHAR_TYPE
            elif self.value == LESS_THAN:
                return left_child < right_child, CHAR_TYPE
            elif self.value == AND:
                return left_child and right_child, CHAR_TYPE
            elif self.value == OR:
                return left_child or right_child, CHAR_TYPE
        else:
            Exception(differentTypesOperationException)

class UnOp(Node):
    def __init__(self,var_type,child):
        self.value = var_type
        self.children = [child]
    def Evaluate(self, ST):
        child, val_type = self.children[0].Evaluate(ST)
        if self.value == PLUS:
            return child, val_type
        elif self.value == MINUS:
            return -(child), val_type
        elif self.value == NOT:
            return not child, val_type

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    def Evaluate(self, ST):
        return self.value, INT_TYPE

class Identifier(Node):
    def __init__(self,name,var_type):
        self.value = var_type
        self.name = name
    def Evaluate(self,ST):
        value = ST.get_value(self.name)
        var_type = ST.get_type(self.name)
        return value, var_type

class Printf(Node):
    def __init__(self,child,var_type):
        self.value = var_type
        self.child = child
    def Evaluate(self,ST):
        print(self.child.Evaluate(ST)[0])

class Return(Node):
    def __init__(self,child,var_type):
        self.value = var_type
        self.child = child
    def Evaluate(self,ST):
        return self.child.Evaluate(ST)

class Scanf(Node):
    def __init__(self,var_type):
        self.value = var_type
    def Evaluate(self,ST):
        return int(input()), INT_TYPE

class Declaration(Node):
    def __init__(self,var_type,child):
        self.value = var_type
        self.children = [child]
    def Evaluate(self, ST):
        ST.set_type(self.children[0].name, self.value)

class Commands(Node):
    def __init__(self,children,var_type,new_scope = False):
        self.value = var_type
        self.children = children
        self.new_scope = new_scope
    def Evaluate(self, ST):
        if self.new_scope:
            New_ST = SymbolTable(ST)
        else:
            New_ST = ST
        for child in self.children:
            res = child.Evaluate(New_ST)
            if res is not None:
                result, var_type = res
                if result != None and var_type != None:
                    if var_type == INT_TYPE:
                        return result, INT_TYPE

class FunctionDeclaration(Node):
    def __init__(self,identifier,children,commands,var_type):
        self.value = var_type
        self.children = children
        self.identifier = identifier
        self.commands = commands
    def Evaluate(self, ST): 
        ST.set_type(self.identifier.name, FUNCTION)
        ST.set_value(self.identifier.name, (self,FUNCTION))

class FunctionCall(Node):
    def __init__(self,identifier,func_identifier,children,var_type):
        self.value = var_type
        self.children = children
        self.identifier = identifier
        self.func_identifier = func_identifier
    def Evaluate(self, ST):
        New_ST = SymbolTable(ST)
        functionDeclaration = ST.get_value(self.func_identifier.name)
        if len(functionDeclaration.children) != len(self.children):
            Exception(numberOfArgumentsDoNotMatch)
        else:
            for child_index in range(len(functionDeclaration.children)):
                New_ST.set_type(functionDeclaration.children[child_index].children[0].name,functionDeclaration.children[child_index].value)
                New_ST.set_value(functionDeclaration.children[child_index].children[0].name,self.children[child_index].Evaluate(ST))
            result = functionDeclaration.commands.Evaluate(New_ST)
            if self.identifier is not None:
                ST.set_value(self.identifier.name, result)
            else:
                return result

class IfCondition(Node):
    def __init__(self,children,var_type):
        self.value = var_type
        self.children = children
    def Evaluate(self, ST):
        if self.children[0].Evaluate(ST)[0]:
            self.children[1].Evaluate(ST)
        else: 
            self.children[2].Evaluate(ST)

class WhileLoop(Node):
    def __init__(self,children,var_type):
        self.value = var_type
        self.children = children
    def Evaluate(self, ST):
        while self.children[0].Evaluate(ST)[0]:
            self.children[1].Evaluate(ST)

class NoOp(Node):
    def __init__(self,var_type):
        self.value = var_type
    def Evaluate(self,ST):
        pass

class SymbolTable:
    def __init__(self, ancestor=None):
        self.ancestor = ancestor
        self.table = {}
    def set_value(self,identifier,value_type):
        if identifier not in self.table:
            raise Exception(referencedBeforeAssignedException)
        else:
            if self.table[str(identifier)][1] == value_type[1]:
                self.table[str(identifier)][0] = value_type[0]

    def set_type(self,identifier,var_type):
        if identifier not in self.table:
            self.table[str(identifier)] = [None, str(var_type)]
        else:
            if self.table[str(identifier)][1] is not None:
                raise Exception(doubleDeclarationException)

    def get_value(self,identifier):
        if str(identifier) not in self.table :
            if self.ancestor != None:
                return self.ancestor.get_value(identifier)
            else:
                raise Exception(declaredButNotAssignedException)
        else:
            return self.table[str(identifier)][0]

    def get_type(self,identifier):
        if str(identifier) not in self.table :
            if self.ancestor != None:
                return self.ancestor.get_type(identifier)
            else:
                raise Exception(declaredButNotAssignedException)
        else:
            return self.table[str(identifier)][1]

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.current_token = None
    def selectNextToken(self):
        value = ""
        isDigit = False
        isWord = False
        local_count = 0
        if self.position >= len(self.origin):
            self.current_token = Token("", EOF)
            return
        while self.position < len(self.origin) and self.origin[self.position] == " ":
            self.position += 1
            local_count += 1
        while self.position < len(self.origin) and self.origin[self.position].isdigit():
            value += self.origin[self.position]
            self.position += 1
            local_count += 1
            isDigit = True
        if isDigit:
            self.current_token = Token(int(value), INT)
            return
        if self.origin[self.position].isalpha():
            value += self.origin[self.position]
            self.position += 1
            local_count += 1
            isWord = True
            while self.position < len(self.origin) and (self.origin[self.position].isdigit() or self.origin[self.position].isalpha() or self.origin[self.position] == '_'):
                value += self.origin[self.position]
                self.position += 1
                local_count += 1
        if isWord:
            if value in reserved_words:
                self.current_token = Token(value, reserved_words[value])
            else:    
                self.current_token = Token(value, IDENTIFIER)
            return local_count
        if self.origin[self.position] == "+":
            value = "+"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, PLUS)
            return local_count
        if self.origin[self.position] == "-":
            value = "-"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, MINUS)
            return local_count
        if self.origin[self.position] == "/":
            value = "/"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, DIVISION)
            return local_count
        if self.origin[self.position] == "*":
            value = "*"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, MULTIPLICATION)
            return local_count
        if self.origin[self.position] == "(":
            value = "("
            self.position += 1
            local_count += 1
            self.current_token = Token(value, OPEN_PARENTHESIS)
            return local_count
        if self.origin[self.position] == ")":
            value = ")"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, CLOSE_PARENTHESIS)
            return local_count
        if self.origin[self.position] == "=":
            value = "="
            self.position += 1
            local_count += 1
            if self.origin[self.position] == "=":
                self.position += 1
                local_count += 1
                self.current_token = Token(value + "=", EQUALS)
            else:
                self.current_token = Token(value + "=", ASSIGNMENT)
            return local_count
        if self.origin[self.position] == "{":
            value = "{"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, OPEN_CURLY_BRACES)
            return local_count
        if self.origin[self.position] == "}":
            value = "}"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, CLOSE_CURLY_BRACES)
            return local_count
        if self.origin[self.position] == ";":
            value = ";"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, SEMICOLON)
            return local_count
        if self.origin[self.position] == ">":
            value = ">"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, GREATER_THAN)
            return local_count
        if self.origin[self.position] == "<":
            value = "<"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, LESS_THAN)
            return local_count
        if self.origin[self.position] == "!":
            value = "!"
            self.position += 1
            local_count += 1
            self.current_token = Token(value, NOT)
            return local_count
        if self.origin[self.position] == "&":
            value = "&"
            self.position += 1
            local_count += 1
            if self.origin[self.position] == "&":
                self.position += 1
                local_count += 1
                self.current_token = Token(value + "&", AND)
            else:
                raise Exception(digitAbsenceError)
            return local_count
        if self.origin[self.position] == "|":
            value = "|"
            self.position += 1
            local_count += 1
            if self.origin[self.position] == "|":
                self.position += 1
                local_count += 1
                self.current_token = Token(value + "|", OR)
            else:
                raise Exception(digitAbsenceError)
            return local_count
        if self.origin[self.position] == ",":
            value = ","
            self.position += 1
            local_count += 1
            self.current_token = Token(value, COMMA)
            return local_count
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
        
    #FUNCTIONCALL-ASSIGNMENT
    @staticmethod     
    def functionCallAssignmentTreatment(left_child):
        func_identifier = Identifier(Analyser.tokens.current_token.value, IDENTIFIER)
        local_step = Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
            children = []                 
            Analyser.tokens.selectNextToken()
            while Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                if Analyser.tokens.current_token.type == IDENTIFIER:
                    children.append(Identifier(Analyser.tokens.current_token.value, IDENTIFIER))
                elif Analyser.tokens.current_token.type == INT:
                    children.append(IntVal(Analyser.tokens.current_token.value))
                Analyser.tokens.selectNextToken()
                if Analyser.tokens.current_token.type == COMMA:
                        Analyser.tokens.selectNextToken()
                elif Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
                    pass
                else:
                    raise Exception(missingCommaException)
            result = FunctionCall(left_child, func_identifier,children,FUNCTION)
            Analyser.tokens.selectNextToken() 
        else:
            Analyser.tokens.position -= local_step + len(func_identifier.name)
            Analyser.tokens.selectNextToken() 
            result = BinOp(ASSIGNMENT, [left_child,Analyser.expressionTreatment()])    
        return result
    
    #FUNCTIONCALL-EXPRESSION
    @staticmethod     
    def functionCallExpressionTreatment(func_identifier):    
            children = []                 
            Analyser.tokens.selectNextToken()
            while Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                if Analyser.tokens.current_token.type == IDENTIFIER:
                    children.append(Identifier(Analyser.tokens.current_token.value, IDENTIFIER))
                elif Analyser.tokens.current_token.type == INT:
                    children.append(IntVal(Analyser.tokens.current_token.value))
                Analyser.tokens.selectNextToken()
                if Analyser.tokens.current_token.type == COMMA:
                        Analyser.tokens.selectNextToken()
                elif Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
                    pass
                else:
                    raise Exception(missingCommaException)
            result = FunctionCall(None, func_identifier, children,FUNCTION)
            Analyser.tokens.selectNextToken()   
            return result

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
                        raise Exception(parenthesisNotClosedException)
                    else:
                        Analyser.tokens.selectNextToken() 
                else:
                    raise Exception(parenthesNotOpenExceptionPrint)
            #FUNCTION-CALL-ASSIGNMENT
            elif Analyser.tokens.current_token.type == IDENTIFIER:
                result = Analyser.functionCallAssignmentTreatment(left_child)
            else:
                result = BinOp(ASSIGNMENT, [left_child,Analyser.expressionTreatment()])
        else:
            raise Exception(assignmentContainsNoIdentifier)
        return result

    #Integers
    @staticmethod
    def factorTreatment():
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
                raise Exception(parenthesisNotClosedException)                
            else:
                Analyser.tokens.selectNextToken()
        elif Analyser.tokens.current_token.type == IDENTIFIER:
            curr_value = Analyser.tokens.current_token.value
            local_step = Analyser.tokens.selectNextToken()
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                func_identifier = Identifier(curr_value, IDENTIFIER)
                result = Analyser.functionCallExpressionTreatment(func_identifier)
            else:
                Analyser.tokens.position -= local_step + len(curr_value)
                Analyser.tokens.selectNextToken()
                result = Identifier(curr_value, IDENTIFIER)
                Analyser.tokens.selectNextToken()
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
    def variableDeclaration():
        var_type = type_words[Analyser.tokens.current_token.value]
        Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.type == IDENTIFIER:
            identifier_value = Analyser.tokens.current_token.value
            Analyser.tokens.selectNextToken()
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                Analyser.tokens.selectNextToken()
                identifier = Identifier(identifier_value, FUNCTION)
                function_declaration_children = []
                while(Analyser.tokens.current_token.type != CLOSE_PARENTHESIS):
                    function_declaration_children.append(Analyser.variableDeclaration())
                    if Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
                        break
                    if Analyser.tokens.current_token.type == COMMA:
                        Analyser.tokens.selectNextToken()
                    else:
                        raise Exception(missingCommaException)
                if Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
                    Analyser.tokens.selectNextToken()
                    result = FunctionDeclaration(identifier,function_declaration_children,Analyser.commandsTreatment(),var_type)
                else:
                    raise Exception(parenthesisNotClosedException)
            else:
                identifier = Identifier(identifier_value, IDENTIFIER)
                result = Declaration(var_type, identifier)
            return result

    @staticmethod     
    def commandTreatment():
        #COMMANDS
        if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
            result = Analyser.commandsTreatment(True)
        #PRINTF
        elif Analyser.tokens.current_token.type == PRINTF:
            Analyser.tokens.selectNextToken() 
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                Analyser.tokens.selectNextToken() 
                result = Printf(Analyser.expressionTreatment(),PRINTF)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    raise Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken() 
            else:
                raise Exception(parenthesNotOpenExceptionPrint)
        #RETURN
        elif Analyser.tokens.current_token.type == RETURN:
            Analyser.tokens.selectNextToken() 
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                Analyser.tokens.selectNextToken() 
                result = Return(Analyser.expressionTreatment(),RETURN)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    raise Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken() 
            else:
                raise Exception(parenthesNotOpenExceptionPrint)
        #IF
        elif Analyser.tokens.current_token.type == IF:
            Analyser.tokens.selectNextToken()
            params = []
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                result = Analyser.booleanExpressionTreatment()
                params.append(result)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    raise Exception(parenthesisNotClosedException)
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
                        raise Exception(parenthesNotOpenExceptionIf)
            else:
                raise Exception(parenthesNotOpenExceptionIf)
        #WHILE
        elif Analyser.tokens.current_token.type == WHILE:
            Analyser.tokens.selectNextToken()
            params = []
            if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                result = Analyser.booleanExpressionTreatment()
                params.append(result)
                if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                    raise Exception(parenthesisNotClosedException)
                else:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
                        true_child = Analyser.commandsTreatment()
                        params.append(true_child)
                        result = WhileLoop(params, WHILE)
                    else:
                        raise Exception(parenthesNotOpenExceptionWhile)
            else:
                raise Exception(parenthesNotOpenExceptionWhile)
        #DECLARATION
        elif Analyser.tokens.current_token.type == TYPE:
            result =  Analyser.variableDeclaration()
        #ASSIGNMENT
        elif Analyser.tokens.current_token.type == IDENTIFIER:
            left_child = Identifier(Analyser.tokens.current_token.value, IDENTIFIER)
            result = Analyser.assignmentTreatment(left_child)
        else:
            raise Exception(commandAbsenceTreatment)
        return result

    @staticmethod     
    def commandsTreatment(new_scope = False):
        if Analyser.tokens.current_token.type == OPEN_CURLY_BRACES:
            children = []
            Analyser.tokens.selectNextToken()
            while Analyser.tokens.current_token.type != CLOSE_CURLY_BRACES:
                children.append(Analyser.commandTreatment())
                if Analyser.tokens.current_token.type == SEMICOLON:
                    Analyser.tokens.selectNextToken() 
                else:
                    raise Exception(commandNotClosedException)
            result = Commands(children, None, new_scope)
            Analyser.tokens.selectNextToken()
            return result
        else:
            raise Exception(noBlockException)

    @staticmethod     
    def programTreatment():
        commands_children = []
        while(Analyser.tokens.current_token.type != EOF):
            function_declaration_children = []
            if Analyser.tokens.current_token.type == TYPE:
                var_type = type_words[Analyser.tokens.current_token.value]
                Analyser.tokens.selectNextToken() 
                if Analyser.tokens.current_token.type == IDENTIFIER:
                    identifier = Identifier(Analyser.tokens.current_token.value, FUNCTION)
                    Analyser.tokens.selectNextToken() 
                    if Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
                        Analyser.tokens.selectNextToken()
                        while(Analyser.tokens.current_token.type != CLOSE_PARENTHESIS):
                            function_declaration_children.append(Analyser.variableDeclaration())
                            if Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
                                break
                            if Analyser.tokens.current_token.type == COMMA:
                                Analyser.tokens.selectNextToken()
                            else:
                                raise Exception(missingCommaException)
                        if Analyser.tokens.current_token.type == CLOSE_PARENTHESIS:
                            Analyser.tokens.selectNextToken()
                            function = FunctionDeclaration(identifier,function_declaration_children,Analyser.commandsTreatment(),var_type)
                            if identifier.name == "main":
                                main = FunctionCall(None,identifier,function_declaration_children,var_type)
                        else:
                            raise Exception(parenthesisNotClosedException)
                    else:
                        raise Exception(parenthesNotOpenExceptionFunction)     
                else:
                    raise Exception(notMainException)
            else:
                raise Exception(notTypeException)
            commands_children.append(function)
        commands_children.append(main)
        return Commands(commands_children, None)


if __name__ == "__main__":
    with open("input.c","r", encoding='utf-8') as input_file:
        program = input_file.read()
        program = program.replace('\n',' ')
        program = program.replace(' ',' ')
        processed_command = PreProcessing.process(program)
        Analyser.init(processed_command)
        ST = SymbolTable()
        p = Analyser.programTreatment()
        if(Analyser.tokens.current_token.type != EOF):
            raise Exception(NotEndOfFileExpection)
        p.Evaluate(ST)