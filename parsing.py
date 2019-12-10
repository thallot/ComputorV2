class Element():
    """Element de l'équation"""
    def __init__(self, EquationPart):
        self.type = self.GetType(EquationPart)
        self.value = self.GetValue(EquationPart)

    def __repr__(self):
        return ('Type {} | value {}\n' .format(self.type, self.value))

    def isnbr(self, EquationPart):
        """Retourne vrai si EquationPart est numeric"""
        c = 0
        if len(EquationPart) == 1:
            return False
        for i in EquationPart:
            if i=='.':
                c += 1
            else :
                pass
        if c > 1:
            return False
        return all(c in "0123456789.+-" for c in EquationPart)

    def isComplexe(self, EquationPart):
        """Retourne vrai si EquationPart est numeric"""
        cptI = 0
        cptOP = 0
        if len(EquationPart) == 1:
            return False
        for i in EquationPart:
            if i == 'i':
                cptI += 1
            elif i == '+' or i == '-':
                cptOP += 1
            if not( i == 'i' or i in "0123456789.+-" or i == '-' or i == '+' or i == ' '):
                return False
        if not (cptOP == 1 and cptI == 1):
            return False
        return True

    def GetType(self, EquationPart):
        """ Retourne le type de EquationPart """
        type = "?"
        if EquationPart.isnumeric() or self.isnbr(EquationPart):
            if isinstance(eval(EquationPart), float):
                type = 'FLOAT'
            elif isinstance(eval(EquationPart), int):
                type = 'INT'
        else:
            if EquationPart == '(':
                type = 'BEGIN_P'
            elif EquationPart == ')':
                type = 'END_P'
            elif EquationPart == '[':
                type = 'BEGIN_C'
            elif EquationPart == ']':
                type = 'END_C'
            elif EquationPart == ',':
                type = 'SEP_NBR'
            elif EquationPart == ';':
                type = 'SEP_MATRICE'
            elif IsOperator(EquationPart):
                type = 'OP'
            elif '(' and ')' in EquationPart and len(EquationPart) > 3:
                type = 'FUNCTION'
            elif EquationPart.isalpha() and not 'i' in EquationPart:
                type = 'VAR'
            elif self.isComplexe(EquationPart):
                type = 'IMGN'
        return type

    def GetValue(self, EquationPart):
        """ Retourne la valeur d'un numeric """
        if self.type == 'INT':
            return int(eval(EquationPart))
        elif self.type == 'FLOAT':
            return float(eval(EquationPart))
        else:
            return EquationPart

def IsOperator(element):
    """ Retourne 1 si l'élément est un opérateur """
    if element == '*' or element == '^' or element == '+' or element == '-'\
    or element == '%' or element == '/' or element == '=' or element == '?' \
    or element == '**':
        return 1
    return 0

def CleanBuffer(nb, str, equation):
    """ Ajoute le contenue du buffer a la liste équation s'il n'est pas vide """
    if not nb == "":
        equation.append(nb.strip())
        nb = ""
    if not str == "":
        equation.append(str.strip())
        str = ""
    return nb, str

def CleanList(equation):
    """ Supprimes les élements vide et les espaces de l'équation """
    while ' ' in equation:
        del equation[equation.index(' ')]
    while '' in equation:
        del equation[equation.index('')]

def InsertPart(equation, element, i):
    tmp = list(element)
    del equation[i]
    for part in tmp:
        equation.insert(i, part)
        i += 1

def FixList(equation):
    for i, element in enumerate(equation):
        if equation[i] == '*' and equation[i + 1] == '*':
            equation[i] = '**'
            del equation[i + 1]
        elif '(' in element:
            if not ')' in element:
                InsertPart(equation, element, i)
        elif '[' in element:
            InsertPart(equation, element, i)
        elif ']' in element:
            InsertPart(equation, element, i)
        elif 'i' in element:
            CreateImaginaire(equation, element, i)

def CreateImaginaire(equation, element, i):
    tmp = ""
    if i == 0:
        print("Invalid input with imaginary number")
        return
    elif equation[i - 1].isnumeric() and i + 2 < len(equation):
        ins = i - 1
        tmp += equation[i - 1]
        tmp += equation[i]
        del equation[i]
        del equation[i - 1]
        tmp += ' '
        tmp += equation[i - 1]
        tmp += ' '
        tmp += equation[i]
        del equation[i - 1]
        del equation[i - 1]
    elif equation[i - 2].isnumeric() and i + 2 < len(equation):
        ins = i - 2
        tmp += equation[i - 2]
        tmp += equation[i - 1]
        tmp += equation[i]
        del equation[i]
        del equation[i - 1]
        del equation[i - 2]
        tmp += ' '
        tmp += equation[i - 2]
        tmp += ' '
        tmp += equation[i - 1]
        del equation[i - 1]
        del equation[i - 2]
    else:
        print("Invalid input with imaginary number")
        return
    tmp = tmp.replace('*', '', 1)
    equation.insert(ins, tmp)

def CreateList(string):
    """ Crée une liste à partir d'une string """
    equation = []
    nb = ""
    str = ""
    split = list(string)
    for i, element in enumerate(split):
        if IsOperator(element):
            nb, str = CleanBuffer(nb, str, equation)
            equation.append(element)
        elif element.isnumeric() or element == '.':
            nb += element
            if not str == "":
                equation.append(str.strip())
                str = ""
        elif not element == " ":
            str += element
            if not nb == "":
                equation.append(nb.strip())
                nb = ""
    CleanBuffer(nb, str, equation)
    CleanList(equation)
    FixList(equation)
    error = CheckError(equation)
    return equation, error

def CheckError(list):
    """ Check les erreur potentiel dans l'input """
    begin = [0, 0]
    end = [0, 0]
    for element in list:
        if element == '(':
            begin[0] += 1
        elif element == ')':
            end[0] += 1
        elif element == '[':
            begin[1] += 1
        elif element == ']':
            end[1] += 1
    if end[0] != begin[0]:
        print("Missing bracket : ()\n")
        return 1
    if end[1] != begin[1]:
        print("Missing bracket : []\n")
        return 1
    return 0

def CreateElementList(str):
    """ Crée une liste d'élement à partir de l'input """
    list = []
    equation, error = CreateList(str)
    for element in equation:
        list.append(Element(element))
    return list, error
