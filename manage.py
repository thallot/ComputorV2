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
            print('Invalid Polynome')
    else:
        print('This function is not defined')

def assignFunction(ParseOne, ParseTwo, var, fun):
    name = ParseOne.list[0].value.split('(')[0]
    f = Function(ParseOne.list[0].value, ParseTwo.list)
    if f.valid:
        fun[name] = f
        if f.var in var.keys():
            print('\033[31mWarning : [', f.var, '] is a variable. This can cause unexpected behavior\033[37m')
        print(fun[name])
    else:
        print('Function ' + name + ' is invalid')
    return fun

def assignVar(ParseOne, ParseTwo, var, fun):
    res, error = evaluate(ParseTwo.list, var, fun)
    if error:
        print('Invalid assignement')
    elif not res == None:
        for key in fun:
            if fun[key].var == ParseOne.list[0].value:
                print('\033[31mWarning : [', ParseOne.list[0].value, '] is a variable of function [', \
                fun[key], ']\nThis can cause unexpected behavior\033[37m')
        var[ParseOne.list[0].value] = res
        print(res)
    return var
