import numpy as np
from calc import *

class Variable():
    """Variable"""
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

    def __repr__(self):
        if self.type == 'MATRICE':
            print(np.array(self.value.replace(';', ',')))
        return ('{}' .format(self.value))

def addVar(varList, newVar):
    """ Ajoute une variable a la liste ou la modifie si elle existe deja"""
    exist = 0
    for element in varList:
        if element.name == newVar.name:
            element.value = newVar.value
            element.type = newVar.type
            exist = 1
    if exist == 0:
        varList.append(newVar)

def getVar(varList, name):
    """ retourne la variable demandé (par son nom) si elle existe """
    exist = 0
    for element in varList:
        if element.name == name:
            return 1, element
    return 0, 0

def defineVar(list, varList):
    """ Assigne la valeur a une variable """
    if  list[2].value == '-':
        list[3].value *= -1
        del list[2]
    value = evaluate(list[2:len(list)])
    if not value == None:
        newVar = Variable(list[0].value, value, 'FLOAT')
        addVar(varList, newVar)
        print(newVar)
    else:
        print('Error in defineVar')

def manageVar(list, varList):
    """ Gere les assignations et l'affichage des variables """
    lenList = len(list)
    if lenList >= 3 and list[0].type == 'VAR' and list[1].value == '=':
        if lenList == 3 and list[2].type == 'VAR':
            exist, oldVar = getVar(varList, list[2].value)
            if exist and not oldVar.name == list[0].value:
                newVar = Variable(list[0].value, oldVar.value, oldVar.type)
                addVar(varList, newVar)
                print(newVar)
            else:
                print('Error')
        else:
            defineVar(list, varList)
    if lenList == 1 and list[0].type == 'VAR':
        exist, myVar = getVar(varList, list[0].value)
        if exist:
            print(myVar)
        else:
            print('Var {} unknown' .format(list[0].value))
    return varList
