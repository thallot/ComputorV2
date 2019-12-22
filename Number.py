from Complex import *
from Matrice import *

class Number():
    """docstring for Number."""

    def __init__(self, value, type='float'):
        self.value, self.type = self.setNumber(value, type)
        self.operand = 1

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        if isinstance(other, Complex):
            realPart = self.value + other.real
            return Complex(real = realPart, img = other.img)
        else:
            print('\033[31mInvalid operation [+] between', self.type, 'and', other.type, '\033[0m')

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        if isinstance(other, Complex):
            realPart = self.value - other.real
            return Complex(real = realPart, img = other.img)
        else:
            print('\033[31mInvalid operation [-] between', self.type, 'and', other.type, '\033[0m')

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        if isinstance(other, Complex):
            realPart = self.value * other.real
            imgPart = self.value * other.img
            return Complex(real = realPart, img = imgPart)
        if isinstance(other, Matrice):
            x = str((self.value * other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('\033[31mInvalid operation [*] between', self.type, 'and', other.type, '\033[0m')

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        if isinstance(other, Complex):
            realPart = self.value / other.real
            imgPart = self.value / other.img
            return Complex(real = realPart, img = imgPart)
        if isinstance(other, Matrice):
            x = str((self.value / other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('\033[31mInvalid operation [/] between', self.type, 'and', other.type, '\033[0m')

    def __mod__(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        if isinstance(other, Complex):
            realPart = self.value % other.real
            imgPart = self.value % other.img
            return Complex(real = realPart, img = imgPart)
        if isinstance(other, Matrice):
            x = str((self.value % other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('\033[31mInvalid operation [%] between', self.type, 'and', other.type, '\033[0m')

    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
        if isinstance(other, Matrice):
            x = str((self.value ** other.value).tolist()).replace('],', '];').replace(' ', '')
            return Matrice(x)
        else:
            print('\033[31mInvalid operation [^] between', self.type, 'and', other.type, '\033[0m')

    def setNumber(self, value, type):
        if type == 'float':
            value = float(value)
            if value % 1 == 0:
                value = int(value)
                type = 'int'
        else:
            value = int(value)
        return value, type
