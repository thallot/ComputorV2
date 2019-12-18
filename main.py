from Parser import *
from Function import *
from calc import *


if __name__ == '__main__':

    var = {}
    fun = {}
    while True:
        strInput = input('> ')
        equalCount = strInput.count('=')
        if equalCount == 0:
            Parsing = Parser(strInput)
            if not Parsing.error == "":
                print(Parsing.error)
                continue
            if len(Parsing.list) == 0:
                continue
            else:
                res, error = evaluate(Parsing.list, var, fun)
                if error:
                    print('Invalid equation')
                elif not res == None:
                    print(res)
        elif equalCount == 1:
            strInput = strInput.split('=')
            ParseOne = Parser(strInput[0])
            ParseTwo = Parser(strInput[1])
            if len(ParseOne.list) == 0 or len(ParseTwo.list) == 0:
                print('Invalid Input')
                continue
            if not ParseOne.error == "":
                print(ParseOne.error)
                continue
            if not ParseTwo.error == "":
                print(ParseTwo.error)
                continue
            if len(ParseOne.list) == 1:
                if ParseOne.list[0].type == 'defFunction' and len(ParseTwo.list) == 2 and ParseTwo.list[-1].value == '?':
                    print('Calc polynome')
                elif ParseOne.list[0].type == 'defFunction':
                    name = ParseOne.list[0].value.split('(')[0]
                    f = Function(ParseOne.list[0].value, ParseTwo.list)
                    if f.valid:
                        fun[name] = f
                        print(fun[name])
                    else:
                        print('Function ' + name + ' is invalid')
                elif ParseOne.list[0].type == 'var':
                    res, error = evaluate(ParseTwo.list, var, fun)
                    if error:
                        print('Invalid assignement')
                    elif not res == None:
                        var[ParseOne.list[0].value] = res
                        print(res)
                else:
                    print('Invalid Input')
        else:
            print('Invalid input')
