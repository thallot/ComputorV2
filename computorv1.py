from Function import *

def calcPolynome(function):
    """ Main fonction : Donne le resultat d'un polynome """
    values, MaxDegree = function.getFactor()
    if values == None:
        print('\033[31mCannot calculate\033[0m')
        return None
    verbose = 0
    display = 0
    if '2' in values:
        a = values['2']
    else:
        a = 0
    if '1' in values:
        b = values['1']
    else:
        b = 0
    if '0' in values:
        c = values['0']
    else:
        c = 0
    if MaxDegree == -2:
        print("\033[32mAll reel numbers are solution ( ∀ x ∈ ℝ  x est solution)\033[0m")
        exit()
    elif MaxDegree == -1:
        print('\033[31mInput is not a polynome\033[0m')
        exit()
    print("Polynomial degree:", MaxDegree)
    if MaxDegree == 0:
        if c == 0:
            print("\033[32mAll reel numbers are solution ( ∀ x ∈ ℝ  x est solution)\033[0m")
        else:
            print('\033[32mNo solution\033[0m')
    elif MaxDegree == 1:
        print('The solution is:')
        if b == 0 and c != 0:
            print("\033[32mNo solution\033[0m")
        elif b == 0 and c == 0:
            print("\033[32mAll reel numbers are solution ( ∀ x ∈ ℝ  x est solution)\033[0m")
        else:
            if verbose == 1:
                print("\nCalcul : \n")
                print("     Result = -( " + str(c) + " / " + str(b) + ")")
                print("     Result = " + str(c/b * -1))
            else:
                print('\033[32m', c/b * -1, '\033[0m')
        if display == 1:
            Display(values)
    elif MaxDegree == 2:
        delta = (b*b)-(4*a*c)
        if (delta > 0):
            racineDelta = delta ** 0.5
            if not a == 0:
                ResOne = ((b * -1) - racineDelta) / (2 * a)
                ResTwo = ((b * -1) + racineDelta) / (2 * a)
            else:
                ResOne = 0
                ResTwo = 0
            if verbose == 1:
                print("\nCalcul : \n")
                print("     Delta = (" + str(b) + ")² - 4 * " + str(a) + " * " + str(c))
                print("     Delta = %.2f\n" %delta)
                print("     R1 = (-" + str(b) + " - √" + str(delta) + ") / (2 * " + str(a) + ")")
                print("     R1 = " + str(round(racineDelta - b, 2)) + " / " + str(2 * a))
                print("     R1 = %.2f\n" %ResOne)
                print("     R2 = (-" + str(b) + " + √" + str(delta) + ") / (2 * " + str(a)  + ")")
                print("     R1 = " + str(round(racineDelta - b, 2))+ " / " + str(2 * a))
                print("     R2 = %.2f\n" %ResTwo)
            print('Discriminant is strictly positive, the two solutions are:')
            print('\033[32m%9.6f \033[0m' %ResOne)
            print('\033[32m%9.6f \033[0m' %ResTwo)
        elif delta == 0:
            if not a == 0:
                res =-b/(2*a)
            else:
                res = 0
            print('Discriminant is strictly null, solutions is:')
            print('\033[32m%9.6f \033[0m' %res)
        else:
            print('Discriminant is strictly negative, the two solutions are:')
            print('\033[32m-' + str(int(b)) + ' + i√' + str(delta) + ' / 2 * ' + str(int(a)) + '\033[0m')
            print('\033[32m-' + str(int(b)) + ' - i√' + str(delta) + ' / 2 * ' + str(int(a)) + '\033[0m')
        if display == 1:
            Display(values)
    elif MaxDegree == 3:
        print("\033[32mThe polynomial degree is stricly greater than 2, I can't solve.\033[0m")
