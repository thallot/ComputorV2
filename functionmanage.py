from calc import *
import varmanage
import re

class Function():
    """Fonction"""
    def __init__(self, name, value,variable):
        self.name = name
        self.value = value
        self.variable = variable

    def __repr__(self):
        return ('{} de {} = {}' .format(self.name, self.variable, self.value))

def addFunction(functionList, newFunction):
    """ Ajoute une function a la liste ou la modifie si elle existe deja"""
    exist = 0
    for element in functionList:
        if element.name == newFunction.name:
            element.value = newFunction.value
            element.variable = newFunction.variable
            exist = 1
    if exist == 0:
        functionList.append(newFunction)

def getFunctionInList(functionList, name):
    if '(' in name:
        name = name.split('(')[0]
    """ retourne la function demandee (par son nom) si elle existe """
    exist = 0
    for element in functionList:
        if element.name == name:
            return 1, element
    return 0, 0

def defineFunction(list, functionList):
    print('ADD FUNCTION')
    """ Assigne une valeur a une function """
    tmp = re.search('(\((.*?)\))', list[0].value)
    variable = tmp.group(0)[1:len(tmp.group(0))-1]
    value = list[2:len(list)]
    name = list[0].value.split('(')[0]
    newFunction = Function(name, value, variable)
    addFunction(functionList, newFunction)

def replaceVariable(function, value):
    variable = function.variable
    list = function.value
    error = 0
    for token in list:
        if token.type == 'VAR' and token.value == variable:
            token.type = 'FLOAT'
            token.value = float(value)
        if token.type == 'FUNCTION' or token.type == 'FUNCALL':
            error = 1
    function.value = list
    return function, error

def printFun(funList):
    for function in funList:
        print('->', function)

def manageFunction(list, functionList, varList):
    """ Gere les assignations et l'affichage des function """
    lenList = len(list)
    if lenList >= 3 and list[0].type == 'FUNCTION' and list[1].value == '=':
        defineFunction(list, functionList)
    if lenList == 1 and list[0].type == 'FUNCALL':
        exist, myFunction = getFunctionInList(functionList, list[0].value)
        tmp = re.search('(\((.*?)\))', list[0].value)
        variable = tmp.group(0)[1:len(tmp.group(0))-1]
        if exist:
            function, error = replaceVariable(myFunction, variable)
            if not error:
                error, res = evaluate(function.value, varList)
                if not error:
                    print(res)
                else:
                    print('Function {} is invalid' .format(myFunction.name))
            else:
                print('Function {} is invalid' .format(myFunction.name))
        else:
            print('Function {} unknown' .format(list[0].value))
    return functionList
