from Parser import *
from calc import *

class Function():
    """docstring for Function."""

    def __init__(self, strInput, value):
        self.value = value
        self.var, self.name = self.setFunction(strInput)
        self.valid = self.isValidFunction()

    def __repr__(self):
        value = str()
        for token in self.value:
            value += str(token.value)
        return self.name + '(' + self.var + ') = ' + value

    def isValidFunction(self):
        for token in self.value:
            if token.type == 'defFunction' or token.type == 'callFunction':
                if token.value.split('(')[0] == self.name:
                    return False
        return True

    def setFunction(self, strInput):
        strInput = strInput.split('(')
        name = strInput[0]
        var = strInput[1].replace(')', '')
        return var, name

    def calc(self, nb, var, fun):
        value = str()
        for token in self.value:
            value += str(token.value)
        value = value.replace(self.var, nb)
        Parsing = Parser(value)
        if len(Parsing.list) == 0:
            error = 1
            res = 0
        else:
            res, error = evaluate(Parsing.list, var, fun)
        return res, error
