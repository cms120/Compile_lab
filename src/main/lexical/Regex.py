from lexical.FA import FA


class Regex:
    RegexExpression = '(a|b)*c'

    def __init__(self, re: str):
        self.re = re

    def get_regex_pofix(self) -> str:  # 得到后缀表达式
        specials = {'*': 50, '.': 40, '|': 30}

        pofix = ""
        stack = ""

        # Loop through the string one character at a time
        for c in self.re:
            if c == '(':
                stack = stack + c
            elif c == ')':
                while stack[-1] != '(':
                    pofix, stack = pofix + stack[-1], stack[:-1]
                # Remove '(' from stack
                stack = stack[:-1]
            elif c in specials:
                while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                    pofix, stack = pofix + stack[-1], stack[:-1]
                stack = stack + c
            else:
                pofix = pofix + c

        while stack:
            pofix, stack = pofix + stack[-1], stack[:-1]

        return pofix

    @classmethod
    def init_by_fa(cls, fa: FA):
        pass
