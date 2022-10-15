from lexical.FA import FA


class Regex:
    def __init__(self, re: str):
        self.re = re

    @classmethod
    def init_by_fa(cls, fa: FA):
        pass
