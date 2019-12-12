from calc import *
from copy import deepcopy
import parsing
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

def replaceVariable(function, value, funList, varList):
    variable = function.variable
    newList = deepcopy(function.value)
    error = 0
    for i, token in enumerate(newList):
        if token.type == 'VAR' and token.value == variable:
            token.type = 'FLOAT'
            token.value = float(value)
        if token.type == 'FUNCTION':
            name = token.value.split('(')[0]
            print(name, function.name)
            if not name == function.name:
                print(name, function)
                exist, subFunction = getFunctionInList(funList, name)
                if exist:
                    newSubList, error = replaceVariable(subFunction, value, funList, varList)
                    if not error:
                        res, error = functionmanage.funResult(name, varList, funList, value)
                        del newList[i]
                        newList.insert(i, parsing.Element('FLOAT', res, 1))
            else:
                error = 1
                break
    return newList, error

def printFun(funList):
    print('__FUNCTIONS__')
    if len(funList) == 0:
        print('No function defined')
    else:
        for function in funList:
            print('->', function)

def funResult(name, varList, funList, value=None):
    exist, myFunction = getFunctionInList(funList, name)
    tmp = re.search('(\((.*?)\))', name)
    if value == None:
        variable = tmp.group(0)[1:len(tmp.group(0))-1]
    else:
        variable = value
    if exist:
        newList, error = replaceVariable(myFunction, variable, funList, varList)
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
