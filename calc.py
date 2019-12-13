from parsing import *
import varmanage
import functionmanage

def precedence(op):
    """ Determine les priorite entre les operateur """
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%' or op == '^':
        return 2
    return 0

def doOp(a, b, op):
    """ retourne le result a OP b """

    if op == '*' or op == '**': return a * b
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '/': return a / b
    if op == '^': return a ** b
    if op == '%': return a % b


def evaluate(list, varList, funList):
    """ NPR Calc sur la liste du parser """
    values = []
    ops = []
    i = 0
    while i < len(list):
        if list[i].value == '(':
            ops.append(list[i].value)
        elif list[i].operand:
            values.append(list[i])
        elif list[i].type == 'VAR':
            exist, var = varmanage.getVarInList(varList, list[i].value)
            if exist and (var.type == 'INT' or var.type == 'FLOAT'):
                values.append(var.value)
            else:
                return 1, 0
        elif list[i].type == 'FUNCALL':
            res, error = functionmanage.funResult(list[i].value, varList, funList)
            if error:
                return 1, 0
            else:
                values.append(res)
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
                if len(values) >= 2:
                    val2 = values.pop()
                    val1 = values.pop()
                else:
                    return 1, 0
                op = ops.pop()
                if (op == '/' or op == '%') and (val1 == 0 or val2 == 0):
                    print('Division by 0')
                    return
                values.append(doOp(val1, val2, op))
            ops.append(list[i].value)
        i += 1
    while len(ops) != 0:
        if len(values) >= 2:
            val2 = values.pop()
            val1 = values.pop()
        else:
            return 1, 0
        op = ops.pop()
        if (op == '/' or op == '%') and (val2 == 0):
            return 1, 0
        values.append(doOp(val1, val2, op))
    return 0, values[-1]

def manageCalc(list, varList, funList):
    lenList = len(list)
    isPrint = 0
    if lenList == 1 and list[0].type != 'FUNCALL' and list[0].type != 'VAR':
        isPrint = 1
        print(list[0].value)
    if lenList >= 2 and list[1].value != '=':
        isPrint = 1
        error, res = evaluate(list, varList, funList)
        if not error:
            print(res)
        else:
            print('Invalid input')
    return isPrint
