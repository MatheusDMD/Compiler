#Compiler version 1.0
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

#ERRORS
operatorError = "A non-digit followed a operator"
operatorAbsenceError = "A non-operator followed a digit"
digitAbsenceError = "A non-digit character started the command"
commentNotCloseException = "A comment was started but closing symbol '*/' is missing "
spaceInBetweenDigitsException = "Does not accept space in between digits without operators"
parenthesisNotClosedException = "Parenthesis was not closed"

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Node:
    def __init__(self):
        self.value = None
        self.children = []
    def Evaluate(self):
        pass
    # def __str__(self):
    #     s='[{0}]'.format(self.value)
    #     if self.children:
    #         for child in self.children:
    #             s+= str(child)
    #     return(s)

class BinOp(Node):
    def __init__(self,type,left_child):
        self.value = type
        self.children = [left_child]

    def add_right(self,right_node):
        self.children.append(right_node)

    def Evaluate(self):
        left_child = self.children[0].Evaluate()
        right_child = self.children[1].Evaluate()
        if self.value == PLUS:
            return left_child + right_child
        elif self.value == MINUS:
            return left_child - right_child
        elif self.value == MULTIPLICATION:
            return left_child * right_child
        elif self.value == DIVISION:
            return left_child // right_child
        
class UnOp(Node):
    def __init__(self,type,child):
        self.value = type
        self.children = [child]
    def Evaluate(self):
        child = self.children[0].Evaluate()
        if self.value == PLUS:
            return child
        elif self.value == MINUS:
            return -(child)

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self,type):
        self.value = type
    def Evaluate(self):
        pass

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
    def factorTreatment():
        Analyser.tokens.selectNextToken()
        if Analyser.tokens.current_token.type == INT:
            return IntVal(Analyser.tokens.current_token.value)
        elif Analyser.tokens.current_token.type == PLUS or Analyser.tokens.current_token.type == MINUS:
            return UnOp(Analyser.tokens.current_token.type, Analyser.factorTreatment())
        elif Analyser.tokens.current_token.type == OPEN_PARENTHESIS:
            result = Analyser.analyseExpression()
            if Analyser.tokens.current_token.type != CLOSE_PARENTHESIS:
                Exception(parenthesisNotClosedException)
            else:
                return result
        else:
            raise Exception(digitAbsenceError)

    @staticmethod
    def termTreatment():
        result = Analyser.factorTreatment()
        Analyser.tokens.selectNextToken()
        while(Analyser.tokens.current_token.type == MULTIPLICATION or Analyser.tokens.current_token.type == DIVISION):
            result = BinOp(Analyser.tokens.current_token.type, result)
            result.add_right(Analyser.factorTreatment())
            Analyser.tokens.selectNextToken()
        return result

    @staticmethod     
    def analyseExpression():
        result = Analyser.termTreatment()
        while(Analyser.tokens.current_token.type == PLUS or Analyser.tokens.current_token.type == MINUS):
            result = BinOp(Analyser.tokens.current_token.type, result)
            result.add_right(Analyser.termTreatment())
        return result


if __name__ == "__main__":
    with open("input.c","r", encoding='utf-8') as input_file:
        for line in input_file:
            line = line.strip()
            processed_command = PreProcessing.process(line)
            Analyser.init(processed_command)
            print(Analyser.analyseExpression().Evaluate())