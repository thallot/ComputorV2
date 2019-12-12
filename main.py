from parsing import *
from varmanage import *
from functionmanage import *
from calc import *

def specialInput(history, varList, funList, str):
    spe = 0
    history.append(str)
    if str == "quit":
        exit("Ok, see you")
    elif str == '--history':
        print('__HISTORY__')
        history.pop()
        if len(history) == 0:
            print('Nothing')
        else:
            for token in history:
                print(token)
        spe = 1
    elif str == "--var":
        printVar(varList)
        spe = 1
    elif str == "--function":
        printFun(funList)
        spe = 1
    elif str == "--all":
        printVar(varList)
        printFun(funList)
        spe = 1
    return spe

def GetInput(varList, funList, history):
    strInput = input('> ')
    spe = specialInput(history, varList, funList, strInput)
    if spe:
        return 0, 1
    list, error, error_value = Parser(strInput)
    if error:
        print('Error : ', error_value)
    return list, error

if __name__ == '__main__':
    varList = []
    funList = []
    history = []
    while 1:
        list, error = GetInput(varList, funList, history)
        if not error:
            detectFunction(funList, varList, list)
            print(list)
            varList, isPrintVar = manageVar(list, varList, funList)
            funList, isPrintFun = manageFunction(list, funList, varList)
            if not (isPrintVar and isPrintFun):
                isPrint = manageCalc(list, varList, funList)
            if not (isPrintVar or isPrintFun or isPrint):
                print('Invalid input...')
