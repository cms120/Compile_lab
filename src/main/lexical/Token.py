from enum import unique, IntEnum


@unique  # val值应该不相同
class LexicalUnit(IntEnum):  # 词法单元
    _V = 1,  # 变量
    _C = 2,  # 整数常数
    _INT = 3,
    _VOID = 4,
    _RETURN = 5,
    _CONST = 6,
    _MAIN = 7,
    _LPAR = 8,  # (
    _RPAR = 9,  # )
    _LBRACE = 10,  # {
    _RBRACE = 11,  # }
    _COMMA = 11,  # ,
    _SEMICOLON = 12,  # ;
    _OP = 13  # 运算符


class Token:
    def __init__(self, lu: LexicalUnit, val: int):
        self.lu = lu
        self.val = val
