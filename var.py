import numpy as np

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

def manageVar(list, varList):
    """ Gere les assignations et l'affichage des variables """
    lenList = len(list)
    if lenList >= 3 and list[0].type == 'VAR' and list[1].value == '=':
        if lenList == 3 and (list[2].type == 'INT' or list[2].type == 'FLOAT' \
        or list[2].type == 'COMPLEXE' or list[2].type == 'MATRICE'):
            newVar = Variable(list[0].value, list[2].value, list[2].type)
            addVar(varList, newVar)
            print(newVar)
        elif lenList == 4 and list[2].value == '-' and (list[3].type == 'INT' \
        or list[3].type == 'FLOAT' or list[3].type == 'COMPLEXE' or list[3].type == 'MATRICE'):
            newVar = Variable(list[0].value, list[3].value * -1, list[3].type)
            addVar(varList, newVar)
            print(newVar)
        else:
            print('Do calc')#Faire op pour trouver la valeur de la variable
    if lenList == 1 and list[0].type == 'VAR':
        exist, myVar = getVar(varList, list[0].value)
        if exist:
            print(myVar)
        else:
            print('Var {} unknown' .format(list[0].value))
    return varList
