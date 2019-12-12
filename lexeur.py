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
    """ Decoupe une str en liste et l'insere dans equation """
    tmp = list(element)
    del equation[i]
    for part in tmp:
        equation.insert(i, part)
        i += 1

def FixList(equation):
    """ Découpe les str invalide et regroupe des caracteres pour former des élément cohérent """
    for i, element in enumerate(equation):
        if equation[i] == '*' and equation[i + 1] == '*':
            equation[i] = '**'
            del equation[i + 1]
        elif '(' in element:
            if not ')' in element:
                InsertPart(equation, element, i)
        elif ')' in element:
            if not '(' in element:
                InsertPart(equation, element, i)
        elif '[' in element:
            InsertPart(equation, element, i)
        elif ']' in element:
            InsertPart(equation, element, i)
        elif 'i' in element:
            GetComplexe(equation, element, i)
    for i, element in enumerate(equation):
        if '[' in element:
            GetMatrice(equation, element, i)

def GetMatrice(equation, element, i):
    """ Regroupe tous les caracteres d'une matrice """
    end = 1
    tmp = ""
    while end:
        if tmp == "":
            end = 0
        if i >= len(equation):
            break
        if equation[i] == ']':
            end -= 1
        elif equation[i] == '[':
            end += 1
        tmp += equation[i]
        del equation[i]
        if end == 0:
            break
    equation.insert(i, tmp)

def GetComplexe(equation, element, i):
    """ Genere un complexe """
    tmp = ""
    if i == 0 or i >= len(equation) - 2:
        return
    if equation[i - 1] == '*':
        del equation[i - 1]
        i -= 1
    if i > 1 and (equation[i - 2] == '-'):
        tmp += equation[i - 2]
        del equation[i - 2]
        i -= 1
    i -= 1
    j = k = i
    for i in range(i, i + 4):
        tmp += equation[i]
    for j in range(j, j + 4):
        del equation[k]
    equation.insert(k, tmp)

def CheckError(string, equation):
    error_value = ""
    error = 0
    if string.count('=') >= 2:
        error_value = 'Too much ='
        error = 1
    if string.count('(') != string.count(')'):
        error_value = 'Missing ()'
        error = 1
    return error, error_value

def Lexeur(string):
    """ Crée une liste (de lexeur) à partir d'une string """
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
    print(equation)
    error, error_value = CheckError(string, equation)
    if error:
        return equation, error, error_value
    return equation, error, error_value
