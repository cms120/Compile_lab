from enum import unique, Enum

from src.lexical.token import LexicalUnitOp
RegexKeyword = {
    'star': '*',
    'point': '.',
    'line': '|',
    'l_par': '(',
    'r_par': ')'
}

@unique
class SyntaxUnit(Enum):
    pass
class Production:
    def __init__(self, left: str, right: list[str]):  # 产生式
        self.left = left
        self.right = right

    def __str__(self):
        str_m = self.left + ' -> '
        for su in self.right:
            str_m += su
        return str_m


class Grammar:
    def __init__(self, productions=None):
        if productions is None:
            productions = set()
        self.productions = productions

    def __str__(self):
        _str = ''
        for prod in self.productions:
            _str += str(prod) + '\n'
        return _str


def get_g_c_minus() -> Grammar:  # TODO 获得c--的文法
    grammar = Grammar(set())
    productions = [
        (SyntaxUnit.Program, [SyntaxUnit.compUnit]),
        (SyntaxUnit.compUnit, [SyntaxUnit])
    ]

    for prod in productions:
        grammar.productions.add(Production(prod[0], prod[1]))

    return grammar
