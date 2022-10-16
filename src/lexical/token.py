from enum import unique, IntEnum


@unique  # val值应该不相同
class LexicalUnit(IntEnum):  # 词法单元
    V = 1,  # 变量
    C = 2,  # 整数常数
    INT = 3,
    VOID = 4,
    RETURN = 5,
    CONST = 6,
    MAIN = 7,
    LPAR = 8,  # (
    RPAR = 9,  # )
    LBRACE = 10,  # {
    RBRACE = 11,  # }
    COMMA = 11,  # ,
    SEMICOLON = 12,  # ;
    OP = 13  # 运算符


class Token:
    def __init__(self, lu: LexicalUnit, val: int):
        self.lu = lu
        self.val = val
