from parsing import *
from varmanage import *
from functionmanage import *
from calc import *

def specialInput(varList, funList, str):
    if str == "quit":
        exit("Ok, see you")
    elif str == "--var":
        printVar(varList)
    elif str == "--function":
        printFun(funList)

def GetInput(varList, funList):
    strInput = input('> ')
    specialInput(varList, funList, strInput)
    list, error, error_value = Parser(strInput)
    if error:
        print('Error : ', error_value)
    return list, error

if __name__ == '__main__':
    varList = []
    funList = []
    while 1:
        list, error = GetInput(varList, funList)
        detectFunction(funList, varList, list)
        print(list)
        if not error:
            varList = manageVar(list, varList)
            funList = manageFunction(list, funList, varList)
