from Number import *
from Element import *

def precedence(op):
    """ Determine les priorite entre les operateur """
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%' or op == '^':
        return 2
    if op == '**':
        return 3
    return 0

def doOp(a, b, op):
    """ retourne le result a OP b """
    if not(a.type == 'Matrice' or b.type == 'Matrice') and op == '**':
        print('Operator ** is only for Matrice')
        return
    if op == '*' or op == '**': return a * b
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '/': return a / b
    if op == '^': return a ** b
    if op == '%': return a % b


def evaluate(list, var, fun):
    """ NPR Calc sur la liste du parser """
    values = []
    ops = []
    i = 0
    error = (0, 1)

    while i < len(list):
        if list[i].type == 'var':
            if list[i].value in var.keys():
                list[i] = var[list[i].value]
            else:
                return error
        elif list[i].type == 'defFunction':
            name = list[i].value.split('(')[0]
            nb = list[i].value.split('(')[1].replace(')', '')
            if nb.isalpha() and nb in var.keys():
                nb = var[nb]
                function = name + '(' + str(nb) + ')'
                list[i] = Element(function, 'callFunction')
        i+=1
    i = 0
    while i < len(list):
        if list[i].type == 'operator' and list[i].value == '(':
            ops.append(list[i].value)
        elif list[i].operand:
            values.append(list[i])
        elif list[i].type == 'callFunction':
            if list[i].value.split('(')[0] in fun.keys():
                function = fun[list[i].value.split('(')[0]]
                nb = list[i].value.split('(')[1].replace(')', '')
                res, error = function.calc(nb, var, fun)
                if error:
                    return error
                elif not res == None:
                    values.append(res)
            else:
                return error
        elif list[i].type == 'operator' and list[i].value == ')':
            while len(ops) != 0 and ops[-1] != '(' and len(values) >= 2:
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(doOp(val1, val2, op))
            if len(ops):
                ops.pop()
        else:
            while (len(ops) != 0 and
                precedence(ops[-1]) >= precedence(list[i].value)):
                if len(values) >= 2:
                    val2 = values.pop()
                    val1 = values.pop()
                else:
                    return error
                op = ops.pop()
                if (op == '/' or op == '%') and (val1 == 0 or val2 == 0):
                    return error
                values.append(doOp(val1, val2, op))
            ops.append(list[i].value)
        i += 1
    while len(ops) != 0:
        if len(values) >= 2:
            val2 = values.pop()
            val1 = values.pop()
        else:
            return error
        op = ops.pop()
        if (op == '/' or op == '%') and (val2.value == 0):
            return error
        values.append(doOp(val1, val2, op))
    if len(values) > 1:
        res = None
    return values[-1], 0
