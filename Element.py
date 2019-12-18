import re

class Element():
    """docstring for Element."""

    def __init__(self, strInput, type):
        self.type = type
        self.value = strInput
        self.operand = 0

    def __repr__(self):
        return self.value
