#Compiler version 1.0
import re

#CONSTANTS
EOF = "EOF"
PLUS = "PLUS"
MINUS = "MINUS"
INT = "INT"
DIVISION = "DIVISION"
MULTIPLICATION = "MULTIPLICATION"

#ERRORS
operatorError = "A non-digit followed a operator"
operatorAbsenceError = "A non-operator followed a digit"
digitAbsenceError = "A non-digit character started the command"
commentNotCloseException = "A comment was started but closing symbol '*/' is missing "
spaceInBetweenDigitsException = "Does not accept space in between digits without operators"

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
        raise Exception(digitAbsenceError)

class PreProcessing:
    @staticmethod
    def process(command):
        return PreProcessing.removeComments(PreProcessing.removeSpaces(command))
        

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

    @staticmethod
    def termTreatment():
        result = None
        Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.type == INT:
            result = Analyser.tokens.current_token.value
            Analyser.tokens.selectNextToken()
            while(Analyser.tokens.current_token.type == MULTIPLICATION or Analyser.tokens.current_token.type == DIVISION):
                if Analyser.tokens.current_token.type == MULTIPLICATION:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == INT:
                        result *= Analyser.tokens.current_token.value
                    else:
                        raise Exception(operatorError)
                elif Analyser.tokens.current_token.type == DIVISION:
                    Analyser.tokens.selectNextToken()
                    if Analyser.tokens.current_token.type == INT:
                        result //= Analyser.tokens.current_token.value
                    else:
                        raise Exception(operatorError)
                else:
                    raise Exception(operatorAbsenceError)
                Analyser.tokens.selectNextToken()
        else:
            raise Exception(digitAbsenceError)
        return result

    @staticmethod     
    def analyseExpression():
        result = Analyser.termTreatment()
        while(Analyser.tokens.current_token.type != EOF):
            if Analyser.tokens.current_token.type == PLUS:
                    result += Analyser.termTreatment()
            elif Analyser.tokens.current_token.type == MINUS:
                    result -= Analyser.termTreatment()
            else:
                raise Exception(operatorAbsenceError)
        return result

command = (str(input("Calculator: ")))
processed_command = PreProcessing.process(command)
Analyser.init(processed_command)
print(Analyser.analyseExpression())