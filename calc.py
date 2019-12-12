from parsing import *

def doCalc(list, start, end):
    tmp = list[start:end]
    print(tmp)
    res = evaluate(tmp)
    return res
# expression where list are
# separated by space.

# Function to find precedence
# of operators.
def precedence(op):

    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0

# Function to perform arithmetic
# operations.
def doOp(a, b, op):

    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a // b
    if op == '^': return a ** b

# Function that returns value of
# expression after evaluation.
def evaluate(list):
    values = []
    ops = []
    i = 0
    while i < len(list):
        if list[i].value == '(':
            ops.append(list[i].value)
        elif list[i].type == 'INT' or list[i].type == 'FLOAT':
            values.append(list[i].value)
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
    return values[-1]


# This code is contributed
# by Rituraj Jain
