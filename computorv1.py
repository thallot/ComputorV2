from Function import *

def calcPolynome(function):
    """ Main fonction : Donne le resultat d'un polynome """
    values, MaxDegree = function.getPolynome()
    verbose = 0
    display = 0
    a = values[2]
    b = values[1]
    c = values[0]
    if MaxDegree == -2:
        print("All reel numbers are solution ( ∀ x ∈ ℝ  x est solution)")
        exit()
    elif MaxDegree == -1:
        print('Input is not a polynome')
        exit()
    print("Polynomial degree:", MaxDegree)
    if MaxDegree == 0:
        if c == 0:
            print("All reel numbers are solution ( ∀ x ∈ ℝ  x est solution)")
        else:
            print('No solution')
    elif MaxDegree == 1:
        print('The solution is:')
        if b == 0 and c != 0:
            print("No solution")
        elif b == 0 and c == 0:
            print("All reel numbers are solution ( ∀ x ∈ ℝ  x est solution)")
        else:
            if verbose == 1:
                print("\nCalcul : \n")
                print("     Result = -( " + str(c) + " / " + str(b) + ")")
                print("     Result = " + str(c/b * -1))
            else:
                print(c/b * -1)
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
            print('%9.6f ' %ResOne)
            print('%9.6f ' %ResTwo)
        elif delta == 0:
            if not a == 0:
                res =-b/(2*a)
            else:
                res = 0
            print('Discriminant is strictly null, solutions is:')
            print('%9.6f : ' %res)
        else:
            print('Discriminant is strictly negative, the two solutions are:')
            print('-' + str(int(b)) + ' + i√' + str(delta) + ' / 2 * ' + str(int(a)))
            print('-' + str(int(b)) + ' - i√' + str(delta) + ' / 2 * ' + str(int(a)))
        if display == 1:
            Display(values)
    elif MaxDegree == 3:
        print("The polynomial degree is stricly greater than 2, I can't solve.")
