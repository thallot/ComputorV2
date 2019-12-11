from parsing import *
from var import *

def GetInput():
    str = input('> ')
    if str == "quit":
        exit()
    strEq, list, error, error_value = Parser(str)
    if error:
        print('Error : ', error_value)
    return list, strEq

if __name__ == '__main__':
    varList = []
    FunList = []
    while 1:
        list, strEq = GetInput()
        varList = manageVar(list, varList)
        print('DEBUG :', strEq)
