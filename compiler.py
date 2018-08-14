#Compiler version 1.0

#CONSTANTS
EOF = "EOF"
PLUS = "PLUS"
MINUS = "MINUS"
INT = "INT"

#ERRORS
operatorError = "A non-digit followed a operator"
operatorAbsenceError = "A non-operator followed a digit"
digitAbsenceError = "A non-digit character started the command"

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.current_token = None
    def selectNextToken(self):
        value = ""
        isDigit = False
        if self.position >= len(self.origin):
            self.current_token = Token("", EOF)
            return
        while self.position < len(self.origin) and self.origin[self.position].isdigit():
            value += self.origin[self.position]
            self.position += 1
            isDigit = True
        if isDigit:
            self.current_token = Token(int(value), INT)
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
        raise ValueError(digitAbsenceError)
        
class Analyser:
    tokens = None
    def init(origin):
        Analyser.tokens = Tokenizer(origin)
           
    def analyseExpression():
        result = None
        Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.type == INT:
            result = Analyser.tokens.current_token.value
            Analyser.tokens.selectNextToken()
            while(Analyser.tokens.current_token.type != EOF):
                if Analyser.tokens.current_token.type == PLUS:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == INT:
                        result += Analyser.tokens.current_token.value
                    else:
                        raise ValueError(operatorError)
                elif Analyser.tokens.current_token.type == MINUS:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == INT:
                        result -= Analyser.tokens.current_token.value
                    else:
                        raise ValueError(operatorError)
                else:
                    raise ValueError(operatorAbsenceError)
                Analyser.tokens.selectNextToken()
        else:
            raise ValueError(digitAbsenceError)
        return result

command = (str(input("Calculator: "))).replace(" ", "")
Analyser.init(command)
print(Analyser.analyseExpression())