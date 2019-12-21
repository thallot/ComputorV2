from Parser import *
from Function import *
from calc import *
from computorv1 import *

def calculatePolynome(ParseOne, var, fun):
    function = None
    for key in fun:
        if key == ParseOne.list[0].value.split('(')[0]:
            function = fun[key]
    if not function == None:
        if function.validPolynome == True:
            calcPolynome(function)
        else:
            print('\033[31mInvalid Polynome\033[37m')
    else:
        print('\033[31mThis function is not defined\033[37m')

def assignFunction(ParseOne, ParseTwo, var, fun):
    name = ParseOne.list[0].value.split('(')[0]
    f = Function(ParseOne.list[0].value, ParseTwo.list)
    if f.valid:
        fun[name] = f
        if f.var in var.keys():
            print('\033[31mWarning : [', f.var, '] is a variable. This can cause unexpected behavior\033[37m')
        print('\033[32mAssignation:', fun[name], '\033[37m')
    else:
        print('\033[31mFunction ' + name + ' is invalid\033[37m')
    return fun

def assignVar(ParseOne, ParseTwo, var, fun):
    res, error = evaluate(ParseTwo.list, var, fun)
    if error:
        print('\033[31mInvalid assignement\033[37m')
    elif not res == None:
        for key in fun:
            if fun[key].var == ParseOne.list[0].value:
                print('\033[31mWarning : [', ParseOne.list[0].value, '] is a variable of function [', \
                fun[key], ']\nThis can cause unexpected behavior\033[37m')
        var[ParseOne.list[0].value] = res
        print('\033[32mAssignation:', ParseOne.list[0].value , ' = ', res, '\033[37m')
    return var

def printFunction(Parsing, var, fun):
    explode = Parsing.list[0].value.split('(')
    name = explode[0]
    funVar = explode[1].replace(')', '')
    if name in fun.keys():
        if funVar == fun[name].var:
            print('\033[32mFunction:', fun[name],'\033[37m')
        else:
            try:
                res, error = evaluate(Parsing.list, var, fun)
                if error:
                    print('\033[31mInvalid equation\033[37m')
                elif not res == None:
                    print('\033[32mResult:',res,'\033[37m')
            except:
                print('\033[31mInvalid equation\033[37m')
    else:
        print('\033[31mFunction', name, 'is not defined\033[37m')

def printVar(Parsing, var, fun):
    name = Parsing.list[0].value
    if name in var.keys():
        print('\033[32mVariable:', var[name],'\033[37m')
    else:
        print('\033[31mVariable', name, 'is not defined\033[37m')

def doCalc(Parsing, var, fun):
    try:
        res, error = evaluate(Parsing.list, var, fun)
        if error:
            print('\033[31mInvalid equation\033[37m')
        elif not res == None:
            print('\033[32mResult:',res,'\033[37m')
    except:
        print('\033[31mInvalid equation\033[37m')
