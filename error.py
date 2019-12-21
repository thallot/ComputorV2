from Parser import *
from Function import *
from calc import *
from computorv1 import *

def specialInput(strInput, var, fun):
    if strInput == '--var':
        print('__VARIABLES__')
        for key in var:
            print(' ', key, '=', var[key])
        return True
    elif strInput == '--fun':
        print('__FUNCTIONS__')
        for key in fun:
            print(' ', fun[key])
        return True
    elif strInput == '--all':
        print('__VARIABLES__')
        for key in var:
            print(' ', key, '=', var[key])
        print('__FUNCTION__')
        for key in fun:
            print(' ', fun[key])
        return True
    elif strInput =='--quit':
        exit()
    return False

def checkInput(strInput):
    if '--all' in strInput or '--var' in strInput or '--fun' in strInput or '--quit' in strInput:
        return '', 0
    equalCount = strInput.count('=')
    if equalCount == 1 and strInput.split('=')[1] == '?':
        equalCount = 0
        strInput = strInput.replace('=?', '')
    return strInput, equalCount

def checkParser(ParseOne, ParseTwo, nbr):
    if nbr >= 1 and not ParseOne.error == "":
        print(ParseOne.error)
        return True
    if nbr >= 2 and not ParseTwo.error == "":
        print(ParseTwo.error)
        return True
    if len(ParseOne.list) == 0 or ( nbr >= 2 and len(ParseTwo.list) == 0):
        print('\033[31mInvalid Input\033[37m')
        return True
    return False
