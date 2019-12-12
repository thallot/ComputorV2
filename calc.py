from parsing import *
import varmanage

def precedence(op):
    """ Determine les priorite entre les operateur """
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%' or op == '^':
        return 2
    return 0

def doOp(a, b, op):
    """ retourne le result a OP b """
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b
    if op == '^': return a ** b
    if op == '%': return a % b

def evaluate(list, varList):
    """ NPR Calc sur la liste du parser """
    values = []
    ops = []
    i = 0
    while i < len(list):
        if list[i].value == '(':
            ops.append(list[i].value)
        elif list[i].type == 'INT' or list[i].type == 'FLOAT':
            values.append(list[i].value)
        elif list[i].type == 'VAR':
            exist, var = varmanage.getVarInList(varList, list[i].value)
            if exist and (var.type == 'INT' or var.type == 'FLOAT'):
                values.append(var.value)
            else:
                print('La variable {} n\'existe pas' .format(list[i].value))
                return 1, 0
        elif list[i].value == ')':
            while len(ops) != 0 and ops[-1] != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(doOp(val1, val2, op))
            ops.pop()
        else:
            while (len(ops) != 0 and
                precedence(ops[-1]) >= precedence(list[i].value)):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                if (op == '/' or op == '%') and (val1 == 0 or val2 == 0):
                    print('Division by 0')
                    return
                values.append(doOp(val1, val2, op))
            ops.append(list[i].value)
        i += 1
    while len(ops) != 0:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        if (op == '/' or op == '%') and (val1 == 0 or val2 == 0):
            print('Division by 0')
            return
        values.append(doOp(val1, val2, op))
    return 0, values[-1]


# This code is contributed
# by Rituraj Jain
