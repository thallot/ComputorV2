from Parser import *
from calc import *
from Number import *
import re

class Function():
    """docstring for Function."""

    def __init__(self, strInput, value):
        self.finalForm = False
        self.validPolynome = True
        self.error = False
        self.value = value
        self.var, self.name = self.setFunction(strInput)
        self.valid = self.isValidFunction()
        self.string = self.getString()
        self.otherVar = self.getOtherVar()
        self.formalize = self.formalize()
        if self.valid:
            self.reduced = self.reducedForm()
            self.factor = self.getFactor()
            if self.factor != (None,None):
                self.finalForm = self.getFinalForm()

    def __str__(self):
        if self.finalForm:
            return self.finalForm
        elif not self.error:
            return self.name + '(' + self.var + ')' + ' = ' + self.reduced.replace('1*', '')
        else:
            return self.name + '(' + self.var + ')' + ' = ' + self.formalize.replace('1*', '')

    def __repr__(self):
        if self.finalForm:
            return self.finalForm
        elif not self.error:
            return self.name + '(' + self.var + ')' + ' = ' + self.reduced.replace('1*', '')
        else:
            return self.name + '(' + self.var + ')' + ' = ' + self.formalize.replace('1*', '')

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
        """ Formate les donnees :
            supprime les espace et split la chaine par '='
            remplace les [\d]x par [\d] * x
            remplaces les [+|-]x par [+|-]1*x
            """
        equation = self.string.replace(' ', '').split('=')[1]
        for i in range(0,9):
            equation = equation.replace(str(i) + self.var, str(i) + '*' + self.var)
        find = re.findall('(.)?(' + self.var + ')(\^\d+)?' , equation)
        for token in find:
            tmp = ''.join(map(str,token))
            if tmp[0] == '+' or tmp[0] == '-' or tmp[0].isalpha():
                equation = equation.replace(tmp, tmp.replace(self.var, '1*' + self.var))
        return equation

    def reducedForm(self):
        equation = self.formalize
        equation = self.reducedFormOne(equation)
        equation = self.reducedFormTwo(equation)
        find = find = re.findall('(\((\d+\.\d+|\d+)\))' , equation)
        for token in find:
            equation = equation.replace(token[0], token[1])
        equation = self.reducedFormOne(equation)
        equation = self.reducedFormTwo(equation)
        return str(equation)


    def reducedFormOne(self, equation):
        """ Split la chaine par [+|-]
            pour chaque token du split, cherche des occurence de [x][^d]?
            supprime ces occurences puis calcul le token
            Ajoute les occurences au resultat du token  """
        splitter = re.split('(\+|\-)', equation)
        newEquation = str()
        state = 0
        for token in splitter:
            if '(' in token or state == 1:
                state = 1
                newEquation += token
                continue
            if ')' in token:
                state = 0
                continue
            if '^' + self.var in token:
                newEquation += token
                self.validPolynome = False
                continue
            find = re.findall('(\*|\^|\/)?(' + self.var + ')(\^\d+)?' , token)
            newVar = []
            for var in find:
                newVar.append(''.join(map(str,var)))
            for var in newVar:
                token = token.replace(var, '')
            if token != '+' and token != '-' and token != '':
                try:
                    newEquation += str(eval(token.replace('^', '**'))) + ''.join(newVar)
                except:
                    self.error = True
                    continue
            else:
                newEquation += token
        return newEquation

    def reducedFormTwo(self, equation):
        """ Recherche des additions ou soustractions de nombres et les calculs """
        find = re.findall('(.)?(\d+\.\d+|\d+)(\+|\-)(\d+\.\d+|\d+)(.)?' , equation)
        for token in find:
            tmp = ''.join(map(str,token))
            if tmp[-1] == '*' or tmp[-1] == '^' or tmp[-1] == '/':
                continue
            if tmp[0] == '*' or tmp[0] == '^' or tmp[0] == '/':
                continue
            else:
                try:
                    if not tmp[0].isnumeric():
                        tmp = tmp[1:-1]
                    else:
                        tmp = tmp[:-1]
                    equation = equation.replace(tmp, str(eval(tmp)))
                except:
                    continue
        return equation

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

    def setFunction(self, strInput):
        strInput = strInput.split('(')
        name = strInput[0]
        var = strInput[1].replace(')', '')
        return var, name

    def getFactor(self):
        factors = {}
        equation = self.reduced
        if self.error:
            return None, None
        find = re.findall('(\+|\-)?(\d+\.\d+|\d+)(\*)(' + self.var + ')(\^\d+)?', equation)
        if len(find) == 0:
            return None, None
        MaxDegree = -1
        for token in find:
            toDelete = ''.join(map(str,token))
            equation = equation.replace(toDelete, '')
            factor = token[4]
            factor = '1' if factor == '' else factor.replace('^', '')
            coef = -1 if token[0] == '-' else 1
            i = 1 if token[0] == '+' or token[0] == '-' or token[0] == '' else 0
            MaxDegree = int(factor) if MaxDegree < int(factor) else MaxDegree
            if factor in factors.keys():
                factors[factor] += float(token[i]) * coef
            else:
                factors[factor] = float(token[i]) * coef
            tmp = ''.join(map(str,token))
        try:
            res = eval(equation)
            factors['0'] = res
        except:
            return None, None
        return factors, MaxDegree

    def getFinalForm(self):
        factor, MaxDegree = self.factor
        equation = str()
        for token in factor:
            if factor[token] % 1 == 0:
                factor[token] = int(factor[token])
            if factor[token] > 0:
                factor[token] = '+' + str(factor[token])
            equation += ' ' + str(factor[token]) + self.var + '^' +token
        equation = equation.strip().replace(self.var + '^0', '').replace('^1', '')
        equation = self.name + '(' + self.var + ') = ' + equation
        return equation

    def calc(self, nb, var, fun):
        if self.error:
            value = self.formalize
        else:
            value = self.reduced
        value = value.replace(self.var, nb)
        Parsing = Parser(value)
        if len(Parsing.list) == 0 or Parsing.error != "":
            error = 1
            res = None
        else:
            res, error = evaluate(Parsing.list, var, fun)
        return res, error
