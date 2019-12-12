from lexeur import *
import re

class Element():
    """Element de l'equation"""
    def __init__(self, type, value, operand):
        self.type = type
        self.value = value
        self.operand = operand

    def __repr__(self):
        return ('Type {} | value {}' .format(self.type, self.value))

def isOperand(type):
    if type == 'INT' or type == 'FLOAT' or type == 'COMPLEXE' or type == 'MATRICE':
        return 1
    return 0

def isNbr(str):
    """Retourne vrai si str est numeric"""
    dot = str.count('.')
    if dot > 1:
        return False
    return all(c in "0123456789." for c in str)

def isComplexe(str):
    """Retourne vrai si str est un nbr complexe"""
    cptI = str.count('i')
    cptOP = str.count('+')
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

def isMatrice(str):
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

def GetType(str):
    """ Retourne le type de str """
    type = "?"
    if str.isnumeric() or isNbr(str):
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
        elif IsOperator(str):
            type = 'OP'
        elif '(' and ')' in str and len(str) > 3:
            type = 'FUNCTION'
        elif str.isalpha() and not 'i' in str:
            type = 'VAR'
        elif isComplexe(str):
            type = 'COMPLEXE'
        elif isMatrice(str):
            type = 'MATRICE'
    return type

def GetValue(str, type):
    """ Retourne la valeur d'un numeric """
    if type == 'INT':
        return int(eval(str))
    elif type == 'FLOAT':
        return float(eval(str))
    else:
        return str

def checkErrorParsing(value, type, equation, i, error, error_value):
    tmp = GetType(equation[i - 1])
    if type == 'OP' and tmp == 'OP':
        if value == '-' and equation[i - 1] == '+':
            del list[i - 1]
        elif not (value == '-' or value == '?'):
            error = 1
            error_value = 'Double operator'
    elif type == '?':
        error = 1
        error_value = value
    return error, error_value

def Parser(string):
    """ Cree une liste d'élement à partir de l'input """
    list = []
    equation, error, error_value = Lexeur(string)
    if error:
        return list, error, error_value
    for i, element in enumerate(equation):
        type = GetType(element)
        value = GetValue(element, type)
        operand = isOperand(type)
        list.append(Element(type, value, operand))
        error, error_value = checkErrorParsing(value, type, equation, i, error, error_value)
    return list, error, error_value
