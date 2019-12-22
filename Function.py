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
        self.otherVar = self.getOtherVar()
        self.formalize = self.formalize()
        self.validPolynome = False
        self.factor = self.getFactor()

    def __str__(self):
        return self.formalize.replace('1 *', '')

    def __repr__(self):
        return self.formalize.replace('1 *', '')

    def actualValue(self, var):
        toPrint = str()
        for token in self.value:
            if token.type == 'var' and self.var != token.value:
                if token.value in var.keys():
                    toPrint += str(var[token.value])
                else:
                    return "\033[31mUnknown variable ["+ str(token.value) +"]\033[0m"
            else:
                toPrint += str(token.value)
        return toPrint

    def getOtherVar(self):
        for token in self.value:
            if token.type == 'var' and self.var != token.value:
                return True
            elif token.type == 'Matrice' or token.type == 'Complex' or token.type == 'defFunction':
                return True
        return False

    def formalize(self):
        equation = self.string.replace(' ', '')
        for i in range(0,9):
            equation = equation.replace(str(i) + self.var, str(i) + '*' + self.var)
        return equation

    def getFactor(self):
        equation = self.formalize.split('=')[1]
        calc = re.findall('(\-)?(\d+|\d+\.\d+)(\*|\^|\/)(\d+\.\d+|\d+)', equation)
        tmp = ''
        for toCalc in calc:
            for token in toCalc:
                tmp += token
            res = eval(tmp)
            equation = equation.replace(tmp, str(res))
        print(equation)
        find = re.findall('(\+|\-)?(\d+|\d+\.\d+)(\*' + self.var + ')(\^\d+)?' , equation)
        for token in find:
            tmp = ""
            for element in token:
                tmp += str(element)
            print(tmp)
        print('Factor', find)

    def getString(self):
        value = str()
        for token in self.value:
            value += " " + str(token.value)
        return self.name + '(' + self.var + ') = ' + value

    def isValidFunction(self):
        """ Verifie que la fonction ne s'appel pas elle meme """
        for token in self.value:
            if token.type == 'defFunction' or token.type == 'callFunction':
                if token.value.split('(')[0] == self.name:
                    return False
        return True








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
        """ Remplace les nb X par nb * X | les X par 1*X | les X * nb par nb * X"""
        equation = self.string.replace(' ', '')
        for i in range(0,9):
            equation = equation.replace(str(i) + self.var, str(i) + '*' + self.var)
        for i in range(0,9):
            equation = equation.replace(self.var + '*' + str(i), str(i) + '*' + self.var)
        find = re.findall('[\+|\-|\=]' + self.var, equation)
        for token in find:
            newToken = token.replace(self.var, '1*' + self.var)
            equation = equation.replace(token, newToken)
        find = re.findall(self.var + '[\*]' + self.var, equation)
        for token in find:
            newToken = token.replace(self.var + '*' + self.var, self.var + '^2')
            equation = equation.replace(token, newToken)
        return equation

    def getFactors(self):
        """ retourne la liste des variable en liste de la forme ['2X[0]', '5X[2]'] """
        equation = self.normalizeFunction()
        find = re.findall('\d+[\.\d+]+\*' + self.var + '[\^\d]*', equation)
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
        find = re.findall('[\-]?\d+[\.\d+]+X\|\d+\|\*[\-]?\d+[\.\d+]*X\|\d+\|', test)
        if find:
            print('1',find)
            self.validPolynome = False
        find = re.findall('[\-|\+]?\d+[\.\d+]+X\|\d+\|', test)
        for i, token in enumerate(find):
            test = test.replace(token, '')
        test = test.split('=')[1]
        if self.var in test:
            print('2', test)
            self.validPolynome = False
        if len(test) >= 1 and not (len(test) == 1 and (test == '+' or test == '-')):
            test = self.reducedForm(test, 2)
            find.append(test + 'X|0|')
        return find

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
        if self.otherVar:
            return self.value
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
