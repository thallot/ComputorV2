from parsing import *
from var import *
from calc import *

def GetInput():
    str = input('> ')
    if str == "quit":
        exit()
    list, error, error_value = Parser(str)
    if error:
        print('Error : ', error_value)
    return list, error

if __name__ == '__main__':
    varList = []
    FunList = []
    while 1:
        list, error = GetInput()
        if not error:
            varList = manageVar(list, varList)
