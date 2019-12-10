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
                type = 'BEGIN'
            elif EquationPart == ')':
                type = 'END'
            elif IsOperator(EquationPart):
                type = 'OP'
            elif '(' and ')' in EquationPart:
                type = 'FUNCTION'
            elif EquationPart.isalpha():
                type = 'VAR'
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
        if '(' in element:
            if not ')' in element:
                InsertPart(equation, element, i)
        if ')' in element:
            if not '(' in element:
                InsertPart(equation, element, i)

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
    return equation

def CheckError(list):
    """ Check les erreur potentiel dans l'input """
    begin = 0
    end = 0
    for element in list:
        if element.type == '?':
            print('Wrong input', element.value)
            return 1
        elif element.value == '(':
            begin += 1
        elif element.value == ')':
            end += 1
    if end != begin:
        print("Missing bracket")
        return 1
    return 0

def CreateElementList(str):
    """ Crée une liste d'élement à partir de l'input """
    list = []
    equation = CreateList(str)
    for element in equation:
        list.append(Element(element))
    error = CheckError(list)
    return list, error
