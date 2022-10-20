from enum import Enum, unique

LexicalUnitKeyword = {
    '_int': 'int',
    '_void': 'void',
    '_return': 'return',
    '_const': 'const',
    '_main': 'main',
}
LexicalUnitDelimiter = {
    'l_par': '(',
    'r_par': ')',
    'l_brace': '{',
    'r_brace': '}',
    'comma': ',',
    'semicolon': ';'
}

LexicalUnitOp = {
    '_commonOp': '+-*/%',
    '_compareOp': '< > <= >= == !=',
    '_boolOp': '&& ||',
    '_assignOp': '='
}

LexicalUnitOther = {
    '_IDN': 'idn',  # 标识符: 变量名、函数名
    'C': 'c',  # 整形常数
    'fp': 'fp',  # 浮点型常数
}


@unique
class LexicalUnit(Enum):  # 词法单元
    def __init__(self):
        for unit in LexicalUnitKeyword.items():
            LexicalUnit[unit[0]] = unit[1]
        for unit in LexicalUnitDelimiter.items():
            LexicalUnit[unit[0]] = unit[1]
        for unit in LexicalUnitOp.items():
            LexicalUnit[unit[0]] = unit[1]
        for unit in LexicalUnitOther.items():
            LexicalUnit[unit[0]] = unit[1]


class Token:
    def __init__(self, lu: LexicalUnit, val: int):
        self.lu = lu
        self.val = val
