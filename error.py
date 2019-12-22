from Parser import *
from Function import *
from calc import *
from computorv1 import *

def checkInput(strInput):
    calc = 0
    if '--all' in strInput or '--var' in strInput or '--fun' in strInput or '--quit' in strInput:
        return '', 0, 0
    equalCount = strInput.count('=')
    if equalCount == 1 and strInput.split('=')[1] == '?':
        equalCount = 0
        strInput = strInput.replace('=?', '')
        calc = 1
    return strInput, equalCount, calc

def checkParser(ParseOne, ParseTwo, nbr):
    if nbr >= 1 and not ParseOne.error == "":
        print(ParseOne.error)
        return True
    if nbr >= 2 and not ParseTwo.error == "":
        print(ParseTwo.error)
        return True
    if len(ParseOne.list) == 0 or ( nbr >= 2 and len(ParseTwo.list) == 0):
        print('\033[31mInvalid Input\033[0m')
        return True
    return False
