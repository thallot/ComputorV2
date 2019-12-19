import Number as N

class Complex():
    """docstring for Complex."""

    def __init__(self, value=None, real=None, img=None):
        self.real, self.img = self.setComplex(value, real, img)
        self.type = 'Complex'
        self.operand = 1
        self.value = self.setValue()

    def __repr__(self):
        return self.value

    def __add__(self, other):
        if isinstance(other, N.Number):
            realPart = other.value + self.real
            return Complex(real = realPart, img = self.img)
        if isinstance(other, Complex):
            realPart = self.real + other.real
            imgPart = self.img + other.img
            if imgPart:
                return Complex(real = realPart, img = imgPart)
            else:
                return N.Number(realPart)

    def __sub__(self, other):
        if isinstance(other, N.Number):
            realPart = other.value - self.real
            return Complex(real = realPart, img = self.img)
        if isinstance(other, Complex):
            realPart = self.real - other.real
            imgPart = self.img - other.img
            if imgPart:
                return Complex(real = realPart, img = imgPart)
            else:
                return N.Number(realPart)

    def __mul__(self, other):
        if isinstance(other, N.Number):
            realPart = other.value * self.real
            imgPart = other.value * self.img
            return Complex(real = realPart, img = imgPart)
        if isinstance(other, Complex):
            realPart = self.real * other.real - self.img * other.img
            imgPart = self.real * other.img + self.img * other.real
            if imgPart:
                return Complex(real = realPart, img = imgPart)
            else:
                return N.Number(realPart)

    def __truediv__(self, other):
        if isinstance(other, N.Number):
            imgPart = self.img / other.value
            realPart = self.real / other.value
            return Complex(real = realPart, img = imgPart)
        if isinstance(other, Complex):
            realPart = ((self.real * other.real) + (self.img * other.img)) / (other.real ** 2 + other.img ** 2)
            imgPart = ((self.img * other.real) - (self.real * other.img)) / (other.real **2 + other.img ** 2)
            if imgPart:
                return Complex(real = realPart, img = imgPart)
            else:
                return N.Number(realPart)

    def __mod__(self, other):
        if isinstance(other, N.Number):
            realPart = other.value % self.real
            return Complex(real = realPart, img = self.img)
        if isinstance(other, Complex):
            realPart = ((self.real * other.real) + (self.img * other.img)) % (other.real ** 2 + other.img ** 2)
            imgPart = ((self.img * other.real) - (self.real * other.img)) % (other.real **2 + other.img ** 2)
            if imgPart:
                return Complex(real = realPart, img = imgPart)
            else:
                return N.Number(realPart)

    def __pow__(self, other):
        if isinstance(other, N.Number):
            realPart = self.real ** other.value
            imgPart = self.img
            if other.value % 2 == 0:
                imgPart *= -1
            return Complex(real = realPart, img = imgPart)
        if isinstance(other, Complex):
            realPart = self.real ** other.real
            imgPart = self.img ** other.img
            return Complex(real = realPart, img = imgPart)

    def setComplex(self, value, real, img):
        if not (real == None and img == None):
            return real, img
        value = value.replace('*', '').replace('+', '')
        if not value == None:
            part = value.split('i')
            if part[0] == '':
                part[0] = 0
            if part[1] == '':
                part[1] = 0
            return int(part[1]), int(part[0])
        else:
            return real, img

    def setValue(self):
        value = str()
        value += str(self.img)
        value += 'i'
        if self.real > 0:
            value += '+'
        if self.real:
            value += str(self.real)
        return value
