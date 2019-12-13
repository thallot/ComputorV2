from lexeur import *
import re
import numpy as np
import ast

class Element():
    """Element de l'equation"""
    def __init__(self, element):
        self.type = self.GetType(element)
        self.value = self.GetValue(element, self.type)
        self.operand = self.isOperand(self.type)
        self.imgPart , self.reelPart = self.getComplexe()
        self.matrice = self.GetMatrice()

    def __repr__(self):
        if self.type == 'INT' or self.type == 'FLOAT':
            return str(self.value)
        elif self.type == 'COMPLEXE':
            imgPart = str(self.imgPart) + 'i'
            reelPart = str(self.reelPart)
            if self.reelPart >= 0:
                reelPart = '+' + reelPart
            return imgPart + reelPart
        elif self.type == 'MATRICE':
            return ' ' + str(self.matrice)[1:-1]
        else:
            return ('Type {} | value {} | Operand : {}\n' .format(self.type, self.value, self.operand))

    def __add__(self, nb):
        if isinstance(nb, Element):
            if (self.type == 'INT' or self.type == 'FLOAT') \
            and (nb.type == 'INT' or nb.type == 'FLOAT'):
                newElem = Element(str(nb.value + self.value))
                return newElem
            elif  (self.type == 'INT' or self.type == 'FLOAT') \
            and nb.type == 'COMPLEXE':
                    imgPart = str(nb.imgPart) + 'i'
                    reelPart = str(nb.reelPart + self.value)
                    if nb.reelPart + self.value >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'COMPLEXE' and nb.type == 'COMPLEXE':
                    imgPart = str(nb.imgPart + self.imgPart) + 'i'
                    reelPart = str(nb.reelPart + self.reelPart)
                    if nb.reelPart + self.reelPart >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'MATRICE' and nb.type == 'MATRICE':
                return str(self.matrice + nb.matrice)
            elif self.type == 'MATRICE' and (nb.type == 'INT' or nb.type == 'FLOAT'):
                return str(self.matrice + nb.value)
            elif self.type == 'MATRICE' and nb.type == 'COMPLEXE':
                print('Can not calculate')
                return None
            else:
                return nb + self
        else:
            print('Error')

    def __mul__(self, nb):
        if isinstance(nb, Element):
            if (self.type == 'INT' or self.type == 'FLOAT') \
            and (nb.type == 'INT' or nb.type == 'FLOAT'):
                newElem = Element(str(nb.value * self.value))
                return newElem
            elif  (self.type == 'INT' or self.type == 'FLOAT') \
            and nb.type == 'COMPLEXE':
                    imgPart = str(nb.imgPart * self.value) + 'i'
                    reelPart = str(nb.reelPart * self.value)
                    if nb.reelPart + self.value >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'COMPLEXE' and nb.type == 'COMPLEXE':
                    imgPart = str(nb.imgPart * self.imgPart) + 'i'
                    reelPart = str(nb.reelPart * self.reelPart)
                    if nb.reelPart + self.reelPart >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'MATRICE' and nb.type == 'MATRICE':
                return str(self.matrice * nb.matrice)
            elif self.type == 'MATRICE' and (nb.type == 'INT' or nb.type == 'FLOAT'):
                return str(self.matrice * nb.value)
            elif self.type == 'MATRICE' and nb.type == 'COMPLEXE':
                print('Can not calculate')
                return None
            else:
                return nb * self
        else:
            print('Error')

    def __truediv__(self, nb):
        if isinstance(nb, Element):
            if (self.type == 'INT' or self.type == 'FLOAT') \
            and (nb.type == 'INT' or nb.type == 'FLOAT'):
                newElem = Element(str(self.value / nb.value))
                return newElem
            elif  (self.type == 'INT' or self.type == 'FLOAT') \
            and nb.type == 'COMPLEXE':
                    imgPart = str(self.imgPart / nb.value) + 'i'
                    reelPart = str(self.reelPart / nb.value)
                    if nb.reelPart / self.value >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'COMPLEXE' and nb.type == 'COMPLEXE':
                    imgPart = str(self.imgPart / nb.imgPart) + 'i'
                    reelPart = str(self.reelPart / nb.reelPart)
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'MATRICE' and nb.type == 'MATRICE':
                return str(self.matrice / nb.matrice)
            elif self.type == 'MATRICE' and (nb.type == 'INT' or nb.type == 'FLOAT'):
                return str(self.matrice / nb.value)
            elif self.type == 'MATRICE' and nb.type == 'COMPLEXE':
                print('Can not calculate')
                return None
            else:
                return nb / self
        else:
            print('Error')

    def __mod__(self, nb):
        if isinstance(nb, Element):
            if (self.type == 'INT' or self.type == 'FLOAT') \
            and (nb.type == 'INT' or nb.type == 'FLOAT'):
                newElem = Element(str(nb.value % self.value))
                return newElem
            elif  (self.type == 'INT' or self.type == 'FLOAT') \
            and nb.type == 'COMPLEXE':
                    imgPart = str(nb.imgPart % self.value) + 'i'
                    reelPart = str(nb.reelPart % self.value)
                    if nb.reelPart + self.value >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'COMPLEXE' and nb.type == 'COMPLEXE':
                    imgPart = str(nb.imgPart % self.imgPart) + 'i'
                    reelPart = str(nb.reelPart % self.reelPart)
                    if nb.reelPart + self.reelPart >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'MATRICE' and nb.type == 'MATRICE':
                return str(self.matrice % nb.matrice)
            elif self.type == 'MATRICE' and (nb.type == 'INT' or nb.type == 'FLOAT'):
                return str(self.matrice % nb.value)
            elif self.type == 'MATRICE' and nb.type == 'COMPLEXE':
                print('Can not calculate')
                return None
            else:
                return nb * self
        else:
            print('Error')

    def __pow__(self, nb):
        if isinstance(nb, Element):
            if (self.type == 'INT' or self.type == 'FLOAT') \
            and (nb.type == 'INT' or nb.type == 'FLOAT'):
                newElem = Element(str(self.value ** nb.value))
                return newElem
            elif  (self.type == 'INT' or self.type == 'FLOAT') \
            and nb.type == 'COMPLEXE':
                    imgPart = str(self.imgPart ** nb.value) + 'i'
                    reelPart = str(self.reelPart ** nb.value)
                    if nb.reelPart ** self.value >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'COMPLEXE' and nb.type == 'COMPLEXE':
                    imgPart = str(self.imgPart ** nb.imgPart) + 'i'
                    reelPart = str(self.reelPart ** nb.reelPart)
                    if nb.reelPart + self.reelPart >= 0:
                        reelPart = '+' + reelPart
                    newElem = Element(imgPart + reelPart)
                    return newElem
            elif self.type == 'MATRICE' and nb.type == 'MATRICE':
                return str(self.matrice ** nb.matrice)
            elif self.type == 'MATRICE' and (nb.type == 'INT' or nb.type == 'FLOAT'):
                return str(self.matrice ** nb.value)
            elif self.type == 'MATRICE' and nb.type == 'COMPLEXE':
                print('Can not calculate')
                return None
            else:
                return nb ** self
        else:
            print('Error')

    def GetValue(self, str, type):
        """ Retourne la valeur d'un numeric """
        if type == 'INT':
            return int(eval(str))
        elif type == 'FLOAT':
            return float(eval(str))
        else:
            return str

    def GetType(self, str):
        """ Retourne le type de str """
        type = "?"
        if str.isnumeric() or self.isNbr(str):
            if isinstance(eval(str), float):
                type = 'FLOAT'
            elif isinstance(eval(str), int):
                type = 'INT'
        else:
            if str == '(':
                type = 'BEGIN_P'
            elif str == ')':
                type = 'END_P'
            elif str == '[':
                type = 'BEGIN_C'
            elif str == ']':
                type = 'END_C'
            elif str == ',':
                type = 'SEP_NBR'
            elif str == ';':
                type = 'SEP_MATRICE'
            elif self.IsOperator(str):
                type = 'OP'
            elif self.isFunction(str):
                type = 'FUNCTION'
            elif self.isFunctionCall(str):
                type = 'FUNCALL'
            elif str.isalpha() and not 'i' in str:
                type = 'VAR'
            elif self.isComplexe(str):
                type = 'COMPLEXE'
            elif self.isMatrice(str):
                type = 'MATRICE'
        return type

    def GetMatrice(self):
        if self.type == 'MATRICE':
            tmp = np.array(ast.literal_eval(self.value.replace(';', ',')))
            return (tmp)

    def getComplexe(self):
        if self.type == 'COMPLEXE':
            tmp = self.value.split('i')
            if tmp[0] == '':
                tmp[0] = 0
            if tmp[1] == '':
                tmp[1] = 0
            return float(tmp[0]), float(tmp[1])
        return 0, 0

    def isOperand(self, type):
        if type == 'INT' or type == 'FLOAT' or type == 'COMPLEXE' or type == 'MATRICE':
            return 1
        return 0

    def IsOperator(self, element):
        """ Retourne 1 si l'element est un operateur """
        if element == '*' or element == '^' or element == '+' or element == '-'\
        or element == '%' or element == '/' or element == '=' or element == '?' \
        or element == '**':
            return 1
        return 0

    def isNbr(self, string):
        """Retourne vrai si str est numeric"""
        dot = string.count('.')
        if dot > 1:
            return False
        nb = 0
        for token in string:
            if token.isnumeric():
                nb += 1
        if nb == 0:
            return False
        return all(c in "0123456789." for c in string)

    def isComplexe(self, str):
        """Retourne vrai si str est un nbr complexe"""
        cptI = str.count('i')
        cptOP = str.count('+')
        cptOP += str.count('-')
        state = 0
        if len(str) == 1:
            return False
        for i in str:
            if i.isnumeric():
                state = 1
            if not i in "0123456789.+-i ":
                return False
        if not (cptOP <= 2 and cptI == 1 and state == 1):
            return False
        return True

    def isMatrice(self, str):
        """ Verifie que la matrice soit bien formate """
        open = str.count('[')
        close = str.count(']')
        sep = str.count(';')
        if not (open == close and open >= 2 and sep == open - 2):
            return False
        if not (str[0] == '[' and str[len(str) - 1] == ']'):
            return False
        tmp = str[1:len(str)-1:1]
        element = tmp.split(';')
        nbElem = []
        for line in element:
            if not (line[0] == '[' and line[len(line) - 1] == ']'):
                return False
            for c in line:
                if not (c.isnumeric() or c in '[,]'):
                    return False
            nbElem.append(len(re.findall('\d+', line)))
        if not (len(set(nbElem))) == 1:
            return False
        return True

    def isFunction(self, str):
        """ Verifie que la fonction soit bien formate """
        if len(str) <= 3:
            return False
        if re.match('[a-zA-Z]+\([a-zA-Z]+\)', str):
            return True
        return False

    def isFunctionCall(self, str):
        """ Verifie que l'appel a une fonction soit bien formate """
        if len(str) <= 3:
            return False
        if re.match('[a-zA-Z]+\([\d+]+\)', str):
            return True
        return False

def Parser(string):
    """ Cree une liste d'element a partir de l'input """
    list = []
    equation, error, error_value = Lexeur(string)
    if error:
        return list, error, error_value
    for i, element in enumerate(equation):
        list.append(Element(element))
        if list[i].type == '?':
            error = 1
            error_value = 'Unknown value ' + str(list[i].value)
    if len(list) > 2 and list[-1].value == '?' and list[-2].value == '=':
        del list[-1]
        del list[-1]
    return list, error, error_value
