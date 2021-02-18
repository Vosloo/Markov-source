import string
from random import choices

class ZeroOrder:
    def __init__(self):
        self.chars = string.ascii_lowercase + ' '
        self.probability = 1 / len(self.chars)


    def next(self) -> str:
        """
        Generates one random character (including space).\n
        If many characters are to be generated it is advised to use get_chars method.
        """
        return ''.join(choices(self.chars, [self.probability] * len(self.chars)))


    def get_chars(self, no_chars=100) -> str:
        """
        Generates no_chars random characters (including space).
        """
        return ''.join(choices(self.chars, [self.probability] * len(self.chars), k=no_chars))