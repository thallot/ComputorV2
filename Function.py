from Parser import *
from calc import *
from Number import *
import re

class Function():
    """docstring for Function."""

    def __init__(self, strInput, value):
        self.value = value
        self.var, self.name = self.setFunction(strInput)
        self.valid = self.isValidFunction()
        self.string = self.getString()
        try:
            self.factor = self.getFactor()
            self.polynome = self.getPolynome()
            self.validPolynome = True
        except:
            self.validPolynome = False

    def __str__(self):
        return self.string

    def formalize(self):
        equation = self.string.replace(' ', '')

    def reducedForm(self, equation, op=1):
        """ Calcul les multiplication, et les autres operateur si op ==2 puis retourne la str """
        regexOp = '[^\^]\d+[\*]\d+'
        if op == 2:
            regexOp = '[^\^]\d+[\*\+\-]\d+'
        while re.findall(regexOp, equation):
            calc = re.findall(regexOp, equation)
            for c in calc:
                if c[0] == '=':
                    c = c[0:]
                if not c[len(c)-1].isnumeric():
                    c = c[:len(c)-1]
                equation = equation.replace(str(c[1:]) , str(eval(c[1:])))
        return equation

    def getFactor(self):
        """ retourne la liste des variable en liste sous forme de ['2X[0]', '5X[2]'] """
        equation = self.string.replace(' ', '')
        for i in range(0,9):
            equation = equation.replace(str(i) + self.var, str(i) + '*' + self.var)
        find = re.findall('\d+[\.\d+]*\*' + self.var + '[\^\d]*', equation)
        test = equation
        for i, token in enumerate(find):
            nb = token.split('*')[0]
            power = token.split('^')
            if len(power) > 1:
                power = power[1]
            else:
                power = 1
            test = test.replace(token, str(nb) + 'X[' + str(power) + ']')
        test = self.reducedForm(test)
        find = re.findall('[\-]?\d+[\.\d+]*?X\[\d+\]', test)
        for i, token in enumerate(find):
            test = test.replace(token, '')
        test = test.split('=')[1]
        if len(test) >= 1 and not (len(test) == 1 and (test == '+' or test == '-')):
            test = self.reducedForm(test, 2)
            find.append(test + 'X[0]')
        return find

    def getPolynome(self):
        """ retourne le degre max et une liste contenant a b et c pour le calcul de polynome """
        MaxDegree = -1
        factor = [0, 0, 0]
        for token in self.factor:
            nb = token.split('X')[0]
            if nb == '':
                continue
            elif nb[0].isnumeric() or nb[0] == '-':
                nb = float(nb)
            else:
                nb = 1
            degree = float(token.split('X')[1].replace('[', '').replace(']', ''))
            if degree == 0:
                factor[0] += nb
            elif degree == 1:
                factor[1] += nb
            elif degree == 2:
                factor[2] += nb
            if degree > MaxDegree:
                MaxDegree = degree
        return factor, MaxDegree

    def getString(self):
        value = str()
        for token in self.value:
            value += " " + str(token.value)
        return self.name + '(' + self.var + ') = ' + value

    def __repr__(self):
        return self.string

    def isValidFunction(self):
        """ Verifie que la fonction ne s'appel pas elle meme """
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
        if len(Parsing.list) == 0 or Parsing.error != "":
            error = 1
            res = 0
        else:
            res, error = evaluate(Parsing.list, var, fun)
        return res, error
