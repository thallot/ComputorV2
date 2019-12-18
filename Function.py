from Parser import *
from calc import *
import re

class Function():
    """docstring for Function."""

    def __init__(self, strInput, value):
        self.value = value
        self.var, self.name = self.setFunction(strInput)
        self.valid = self.isValidFunction()
        self.string = self.getString()
        self.polynome = self.getPolynome()

    def __repr__(self):
        equation = self.reducedForm()
        return equation

    def reducedForm(self):
        equation = self.string.replace(' ', '')
        regexOp = '[^\^]\d+[\+|\-|\*]\d+[\+|\-|\*\d+]*'
        while re.findall(regexOp, equation):
            calc = re.findall(regexOp, equation)
            for c in calc:
                if c[0] == '=':
                    c = c[0:]
                if not c[len(c)-1].isnumeric():
                    c = c[:len(c)-1]
                equation = equation.replace(str(c[1:]) , str(eval(c[1:])))
        return equation

    def getPolynome(self):
        equation = self.reducedForm()
        find = re.findall('[\d+]?[\*]' + self.var + '[\^\d]*', equation)
        print('>>', find)
        print('>>', equation)
        return find

    def getString(self):
        value = str()
        for token in self.value:
            value += " " + str(token.value)
        return self.name + '(' + self.var + ') = ' + value

    def __repr__(self):
        return self.string

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
