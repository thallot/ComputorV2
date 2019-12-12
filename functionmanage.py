from calc import *
from copy import deepcopy
import varmanage
import re

class Function():
    """Fonction"""
    def __init__(self, name, value,variable):
        self.name = name
        self.value = value
        self.variable = variable

    def __repr__(self):
        rep = ""
        for token in self.value:
            rep += " " +  str(token.value)
        return ('{}({}) = {}' .format(self.name, self.variable, rep))

def addFunction(funList, newFunction):
    """ Ajoute une function a la liste ou la modifie si elle existe deja"""
    exist = 0
    for element in funList:
        if element.name == newFunction.name:
            element.value = newFunction.value
            element.variable = newFunction.variable
            exist = 1
    if exist == 0:
        funList.append(newFunction)

def getFunctionInList(funList, name):
    if '(' in name:
        name = name.split('(')[0]
    """ retourne la function demandee (par son nom) si elle existe """
    exist = 0
    for element in funList:
        if element.name == name:
            return 1, element
    return 0, 0

def defineFunction(list, funList):
    """ Assigne une valeur a une function """
    tmp = re.search('(\((.*?)\))', list[0].value)
    variable = tmp.group(0)[1:len(tmp.group(0))-1]
    value = list[2:len(list)]
    name = list[0].value.split('(')[0]
    newFunction = Function(name, value, variable)
    addFunction(funList, newFunction)
    print(newFunction)

def replaceVariable(function, value):
    variable = function.variable
    newList = deepcopy(function.value)
    error = 0
    for token in newList:
        if token.type == 'VAR' and token.value == variable:
            token.type = 'FLOAT'
            token.value = float(value)
    return newList, error

def printFun(funList):
    print('__FUNCTIONS__')
    if len(funList) == 0:
        print('No function defined')
    else:
        for function in funList:
            print('->', function)

def funResult(name, varList, funList):
    exist, myFunction = getFunctionInList(funList, name)
    tmp = re.search('(\((.*?)\))', name)
    variable = tmp.group(0)[1:len(tmp.group(0))-1]
    if exist:
        newList, error = replaceVariable(myFunction, variable)
        if not error:
            error, res = evaluate(newList, varList, funList)
            if not error:
                return res, 0
            else:
                print('Function {} is invalid.' .format(myFunction.name))
        else:
            print('Function {} is invalid' .format(myFunction.name))
    else:
        print('Function {} unknown' .format(list[0].value))
    return 0, 0

def manageFunction(list, funList, varList):
    """ Gere les assignations et l'affichage des function """
    lenList = len(list)
    isPrint = 0
    if lenList >= 3 and list[0].type == 'FUNCTION' and list[1].value == '=':
        isPrint = 1
        defineFunction(list, funList)
    if lenList == 1 and list[0].type == 'FUNCALL':
        isPrint = 1
        res, error = funResult(list[0].value, varList, funList)
        if not error:
            print(res)
    return funList, isPrint
