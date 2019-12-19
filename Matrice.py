import re
import numpy as np
import ast
from Number import *

class Matrice():
    """docvalueing for Matrice."""

    def __init__(self, value):
        self.valid = self.isValidMatrice(value)
        self.type = 'Matrice'
        self.operand = 1
        self.string = self.getString(value)
        self.value = self.getValue(value)

    def __repr__(self):
        result = str()
        for line in self.string:
            result += str(line) + '\n'
        return result[:len(result)-1]

    def __add__(self, other):
        if isinstance(other, Matrice):
            x = str((self.value + other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('Invalid Operation')

    def __sub__(self, other):
        if isinstance(other, Matrice):
            x = str((self.value * other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('Invalid Operation')

    def __mul__(self, other):
        if isinstance(other, Matrice):
            x = str((self.value * other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        if other.type == 'int' or other.type == 'float':
            x = str((self.value * other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('Invalid Operation')

    def __truediv__(self, other):
        if isinstance(other, Matrice):
            x = str((self.value / other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        if other.type == 'int' or other.type == 'float':
            x = str((self.value / other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('Invalid Operation')

    def __mod__(self, other):
        if isinstance(other, Matrice):
            x = str((self.value % other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        if other.type == 'int' or other.type == 'float':
            x = str((self.value % other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('Invalid Operation')

    def __pow__(self, other):
        if isinstance(other, Matrice):
            x = str((self.value ** other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        if other.type == 'int' or other.type == 'float':
            x = str((self.value ** other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('Invalid Operation')

    def isValidMatrice(self, value):
        """ Verifie que la matrice soit bien formate """
        open = value.count('[')
        close = value.count(']')
        sep = value.count(';')
        if not (open == close and open >= 2 and sep == open - 2):
            return False
        if not (value[0] == '[' and value[len(value) - 1] == ']'):
            return False
        tmp = value[1:len(value)-1:1]
        element = tmp.split(';')
        nbElem = []
        for line in element:
            if not (line[0] == '[' and line[len(line) - 1] == ']'):
                return False
            if not (line[1].isnumeric() and line[len(line) - 2].isnumeric()):
                return False
            for c in line:
                if not (c.isnumeric() or c in '[,]'):
                    return False
            nbElem.append(len(re.findall('\d+', line)))
        if not (len(set(nbElem))) == 1:
            return False
        return True

    def getMatrice(strInput):
        """ Regroupe tous les caracteres d'une matrice """
        tmp = ""
        end = i = 0
        while i < len(strInput):
            if strInput[i] == ']':
                end -= 1
            elif strInput[i] == '[':
                end += 1
            tmp += strInput[i]
            if end == 0:
                break
            i += 1
        return tmp

    def getString(self, value):
        if not self.valid:
            return None
        value = value[1:len(value) - 1]
        matrice = value.split(';')
        result = []
        for line in matrice:
            result.append(line)
        return result

    def getValue(self, value):
        if not self.valid:
            return None
        matrice = np.array(ast.literal_eval(value.replace(';', ',')))
        return np.array(matrice)
