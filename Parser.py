from Number import *
from Complex import *
from Matrice import *
from Element import *
import re

class Parser():
    """docstring for Parser."""

    def __init__(self, strInput):
        self.list, self.error = self.parse(strInput)

    def __repr__(self):
        return self.list

    def solveError(self, list):
        for i, token in enumerate(list):
            if i + 2 < len(list):
                if list[i].type == 'operator' and list[i + 1].type == 'operator' \
                and list[i + 2].operand == 1 and list[i + 1].value == '-':
                    if isinstance(list[i + 2], Number):
                        del list[i + 1]
                        list[i + 1] = Number(str(list[i + 1].value * -1))
            if i + 1 < len(list) and i == 0 and  list[i].type != 'Matrice' and list[i].value == '-' and list[i + 1].operand == 1:
                if isinstance(list[i + 1], Number):
                    del list[i]
                    list[i] = Number(str(list[i].value * -1))

    def checkError(self, strInput):
        error = str()
        if strInput.count('(') != strInput.count(')'):
            error = 'Missing ()'
        return error

    def parse(self, strInput):
        """ Detect les element et les insere dans une liste """

        strInput = strInput.replace(' ', '')
        strInput = strInput.replace('+-', '-')
        i = 0
        list = []
        error = str()
        while i < len(strInput):
            if re.match('\d+?\*?i', strInput[i:]):
                find = re.search('\d+?\*?i', strInput[i:]).group(0)
                i += len(find) - 1
                list.append(Complex(find))
            elif re.match('\d+\.\d+\*?i', strInput[i:]):
                find = re.search('\d+\.\d+\*?i', strInput[i:]).group(0)
                i += len(find) - 1
                list.append(Complex(find))
            elif re.match('i', strInput[i:]):
                find = re.search('i', strInput[i:]).group(0)
                i += len(find) - 1
                list.append(Complex(find))
            elif re.match('\d+\.\d+', strInput[i:]):
                find = re.search('\d+\.\d+', strInput[i:]).group(0)
                i += len(find) - 1
                list.append(Number(find, 'float'))
            elif re.match('\d+', strInput[i:]):
                find = re.search('\d+', strInput[i:]).group(0)
                i += len(find) - 1
                list.append(Number(find, 'int'))
            elif re.match('[a-zA-Z]+\([a-zA-Z]+\)', strInput[i:]):
                find = re.search('[a-zA-Z]+\([a-zA-Z]+\)', strInput[i:]).group(0)
                i += len(find) -1
                if 'i' in find:
                    error = "\033[31mA function cannot contain i\033[0m"
                list.append(Element(find, 'defFunction'))
            elif re.match('[a-zA-Z]+\(\-?\d+\)', strInput[i:]):
                find = re.search('[a-zA-Z]+\(\-?\d+\)', strInput[i:]).group(0)
                i += len(find) -1
                if 'i' in find:
                    error = "\033[31mA function cannot contain i\033[0m"
                list.append(Element(find, 'callFunction'))
            elif re.match('[a-zA-Z]+', strInput[i:]):
                find = re.search('[a-zA-Z]+', strInput[i:]).group(0)
                i += len(find) - 1
                if 'i' in find:
                    error = "\033[31mA variable cannot contain i\033[0m"
                list.append(Element(find, 'var'))
            elif strInput[i] == '[':
                find = Matrice.getMatrice(strInput[i:])
                i += len(find) - 1
                matrice = Matrice(find)
                if not matrice.valid:
                    error = "\033[31mInvalid Matrice:\033[0m " + find
                list.append(matrice)
            elif re.match('\*\*', strInput[i:]):
                find = re.search('\*\*', strInput[i:]).group(0)
                i += len(find) - 1
                list.append(Element(find, 'operator'))
            elif strInput[i] in '+-*/%^=?()':
                list.append(Element(strInput[i], 'operator'))
            else:
                error = "\033[31mInvalid input:\033[0m " + strInput[i]
            i += 1
            if not error == "":
                break
        self.solveError(list)
        if error == "":
            error = self.checkError(strInput)
        return list, error
