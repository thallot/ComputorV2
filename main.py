from parsing import *

if __name__ == '__main__':
    str = input('> ')
    list, error = CreateElementList(str)
    print(list, error)
