from Parser import *
from Function import *
from calc import *
from computorv1 import *

def specialInput(strInput, var, fun):
    if strInput == '--var':
        print('\033[4mVARIABLES :\033[0m')
        for key in var:
            print('\033[93m ', key, '=', var[key], '\033[0m')
        return True
    elif strInput == '--fun':
        print('\033[4mFUNCTIONS :\033[0m')
        for key in fun:
            print('\033[93m ', fun[key], '\033[0m')
        return True
    elif strInput == '--all':
        print('\033[4mVARIABLES :\033[0m')
        for key in var:
            print('\033[93m ', key, '=', var[key], '\033[0m')
        print('\033[4mFUNCTIONS :\033[0m')
        for key in fun:
            print('\033[93m ', fun[key], '\033[0m')
        return True
    elif strInput =='--quit':
        exit()
    return False

def calculatePolynome(ParseOne, var, fun):
    function = None
    for key in fun:
        if key == ParseOne.list[0].value.split('(')[0]:
            function = fun[key]
    if not function == None:
        if function.validPolynome == True:
            calcPolynome(function)
        else:
            print('\033[31mInvalid Polynome\033[0m')
    else:
        print('\033[31mThis function is not defined\033[0m')

def assignFunction(ParseOne, ParseTwo, var, fun):
    name = ParseOne.list[0].value.split('(')[0]
    f = Function(ParseOne.list[0].value, ParseTwo.list)
    if f.valid:
        fun[name] = f
        if f.var in var.keys():
            print('\033[31mWarning : [', f.var, '] is a variable. This can cause unexpected behavior\033[0m')
        print('\033[32mAssignation:', fun[name], '\033[0m')
    else:
        print('\033[31mFunction ' + name + ' is invalid\033[0m')
    return fun

def assignVar(ParseOne, ParseTwo, var, fun):
    try:
        res, error = evaluate(ParseTwo.list, var, fun)
        if error:
            print('\033[31mInvalid assignement\033[0m')
        elif not res == None:
            for key in fun:
                if fun[key].var == ParseOne.list[0].value:
                    print('\033[31mWarning : [', ParseOne.list[0].value, '] is a variable of function [', \
                    fun[key], ']\nThis can cause unexpected behavior\033[0m')
            var[ParseOne.list[0].value] = res
            print('\033[32mAssignation:', ParseOne.list[0].value , ' = ', res, '\033[0m')
    except:
        print('\033[31mInvalid assignement\033[0m')
    return var

def printFunction(Parsing, var, fun, calc):
    explode = Parsing.list[0].value.split('(')
    name = explode[0]
    funVar = explode[1].replace(')', '')
    if name in fun.keys():
        if funVar == fun[name].var and not (funVar in var.keys()):
            print('\033[32mDefinition   :', fun[name],'\033[0m')
            if fun[name].otherVar:
                print('\033[32mActual value :', fun[name].actualValue(var),'\033[0m')
        else:
            try:
                res, error = evaluate(Parsing.list, var, fun)
                if error:
                    print('\033[31mInvalid equation\033[0m')
                elif not res == None:
                    print('\033[32mResult:',res,'\033[0m')
            except:
                print('\033[31mInvalid equation\033[0m')
    else:
        print('\033[31mFunction', name, 'is not defined\033[0m')

def printVar(Parsing, var, fun):
    name = Parsing.list[0].value
    if name in var.keys():
        print('\033[32mVariable:', var[name],'\033[0m')
    else:
        print('\033[31mVariable', name, 'is not defined\033[0m')

def doCalc(Parsing, var, fun):
    try:
        res, error = evaluate(Parsing.list, var, fun)
        if error:
            print('\033[31mInvalid equation\033[0m')
        elif not res == None:
            print('\033[32mResult:',res,'\033[0m')
    except:
        print('\033[31mInvalid equation\033[0m')
