from Parser import *
from Function import *
from calc import *
from computorv1 import *
from error import *
from manage import *

if __name__ == '__main__':

    var = {}
    fun = {}
    while True:
        strInput = input('\033[36m> ').replace(' ', '')
        print('\033[37m', end='')
        if specialInput(strInput, var, fun):
            continue
        strInput, equalCount = checkInput(strInput)
        if equalCount == 0:
            Parsing = Parser(strInput)
            if checkParser(Parsing, None, 1):
                continue
            else:
                res, error = evaluate(Parsing.list, var, fun)
                if error:
                    print('\033[31mInvalid equation\033[37m')
                elif not res == None:
                    print(res)
        elif equalCount == 1:
            strInput = strInput.split('=')
            ParseOne = Parser(strInput[0])
            ParseTwo = Parser(strInput[1])
            if checkParser(ParseOne, ParseTwo, 2):
                continue
            if len(ParseOne.list) == 1:
                if ParseOne.list[0].type == 'defFunction' and len(ParseTwo.list) == 2 and ParseTwo.list[-1].value == '?':
                    calculatePolynome(ParseOne, var, fun)
                elif ParseOne.list[0].type == 'defFunction':
                    fun = assignFunction(ParseOne, ParseTwo, var, fun)
                elif ParseOne.list[0].type == 'var':
                    var = assignVar(ParseOne, ParseTwo, var, fun)
                else:
                    print('\033[31mInvalid Input\033[37m')
        else:
            print('\033[31mInvalid input :\033[37m Double operator =')
