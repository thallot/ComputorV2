import calc

class Variable():
    """Variable"""
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

    def __repr__(self):
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

def getVarInList(varList, name):
    """ retourne la variable demandee (par son nom) si elle existe """
    exist = 0
    for element in varList:
        if element.name == name:
            return 1, element
    return 0, 0

def defineVar(list, varList, funList):
    """ Assigne la valeur a une variable """
    if  list[2].value == '-':
        list[3].value *= -1
        del list[2]
    error, value = calc.evaluate(list[2:len(list)], varList, funList)
    if not error:
        newVar = Variable(list[0].value, value, 'FLOAT')
        addVar(varList, newVar)
        print(newVar.value)

def printVar(varList):
    print('__VARIABLES__')
    if len(varList) == 0:
        print('No variable defined')
    else:
        for variable in varList:
            print('-> {} = {}' .format(variable.name, variable.value))

def manageVar(list, varList, funList):
    """ Gere les assignations et l'affichage des variables """
    lenList = len(list)
    isPrint = 0
    if lenList >= 3 and list[0].type == 'VAR' and list[1].value == '=':
        isPrint = 1
        if lenList == 3 and list[2].type == 'VAR':
            exist, oldVar = getVarInList(varList, list[2].value)
            if exist and not oldVar.name == list[0].value:
                newVar = Variable(list[0].value, oldVar.value, oldVar.type)
                addVar(varList, newVar)
                print(newVar.value)
            else:
                print('Error')
        else:
            defineVar(list, varList, funList)
    if lenList == 1 and list[0].type == 'VAR':
        isPrint = 1
        exist, myVar = getVarInList(varList, list[0].value)
        if exist:
            print(myVar)
        else:
            print('Var {} unknown' .format(list[0].value))
    return varList, isPrint
