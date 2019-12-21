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
            self.value = self.getValue()
            self.string = self.getStringTwo()
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

    def normalizeFunction(self):
        """ Remplace les nbX par nb * X et les X par 1*X"""
        equation = self.string.replace(' ', '')
        for i in range(0,9):
            equation = equation.replace(str(i) + self.var, str(i) + '*' + self.var)
        find = re.findall('[\+|\-|\=]' + self.var, equation)
        for token in find:
            newToken = token.replace(self.var, '1*' + self.var)
            equation = equation.replace(token, newToken)
        return equation

    def getFactor(self):
        """ retourne la liste des variable en liste de la forme ['2X[0]', '5X[2]'] """
        equation = self.normalizeFunction()
        find = re.findall('\d+[\.\d+]*\*' + self.var + '[\^\d]*', equation)
        test = equation
        for i, token in enumerate(find):
            nb = token.split('*')[0]
            power = token.split('^')
            if len(power) > 1:
                power = power[1]
            else:
                power = 1
            test = test.replace(token, str(nb) + 'X|' + str(power) + '|')
        test = self.reducedForm(test)
        find = re.findall('[\-]?\d+[\.\d+]*X\|\d+\|', test)
        for i, token in enumerate(find):
            test = test.replace(token, '')
        test = test.split('=')[1]
        if len(test) >= 1 and not (len(test) == 1 and (test == '+' or test == '-')):
            test = self.reducedForm(test, 2)
            find.append(test + 'X|0|')
        return find

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

    def getPolynome(self):
        """ Genere un dict avec en cle le degree et en value la valeur du polynome"""
        list = self.factor
        equation = str()
        element = {}
        maxDegree = - 1
        for token in list:
            tmp = token.split('X')
            tmp[0] = tmp[0].replace('+', '')
            tmp[1] = tmp[1].replace('|', '')
            if re.match('\-?\d+[\.\d+]?', tmp[0]):
                if tmp[1] in element:
                    element[tmp[1]] += float(tmp[0])
                else:
                    element[tmp[1]] = float(tmp[0])
            if maxDegree < int(tmp[1]):
                maxDegree = int(tmp[1])
        return element, maxDegree

    def getStringTwo(self):
        equation = str()
        for token in self.value:
            equation += ' ' + str(token)
        equation = self.name + '(' + self.var + ') = ' + equation
        return equation

    def getValue(self):
        element, maxDegree = self.polynome
        degree = sorted(element)
        equation = str()
        cpt = 0
        for i in degree:
            if element[i] == 0:
                continue
            elif element[i] > 0 and cpt > 0:
                element[i] = '+' + str(element[i])
            if int(i) > 1:
                equation += str(element[i]) + '*' + self.var + '^' + str(i)
            elif int(i) == 1:
                equation += str(element[i]) + '*' + self.var
            elif int(i) == 0:
                equation += str(element[i])
            cpt += 1
        Parsing = Parser(equation)
        return Parsing.list

    def calc(self, nb, var, fun):
        value = str()
        for token in self.value:
            value += str(token.value)
        value = value.replace(self.var, nb)
        Parsing = Parser(value)
        if len(Parsing.list) == 0 or Parsing.error != "":
            error = 1
            res = None
        else:
            res, error = evaluate(Parsing.list, var, fun)
        return res, error
