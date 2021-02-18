from random import choices

class FirstOrder:
    def __init__(self, probabilities):
        self.probabilities: dict = probabilities

    def next(self) -> str:
        """
        Generates one random character.\n
        May include spaces and numbers - depends on sample text the probabilities were based on.\n
        If many characters are to be generated it is advised to use get_chars method.
        """
        return ''.join(choices(list(self.probabilities.keys()), list(self.probabilities.values())))


    def get_chars(self, no_chars=100) -> str:
        """
        Generates no_chars random characters (including spaces and numbers).
        """
        return ''.join(choices(list(self.probabilities.keys()), list(self.probabilities.values()), k=no_chars))