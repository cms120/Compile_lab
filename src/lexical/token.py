from enum import unique, IntEnum


@unique  # val值应该不相同
class LexicalUnit(IntEnum):  # 词法单元 TODO 删除,
    V = 1,  # 变量
    C = 2,  # 整数常数
    INT = 3,
    VOID = 4,
    RETURN = 5,
    CONST = 6,
    MAIN = 7,
    L_PAR = 20,  # (
    R_PAR = ')',  # )
    L_BRACE = '{',  # {
    R_BRACE = '}',  # }
    COMMA = 11,  # ,
    SEMICOLON = 12,  # ;
    OP = 13  # 运算符


class Token:
    def __init__(self, wordsUnit: str):
        self.words = wordsUnit
        self.type = self.get_type_by_words()
        self.val = self.get_val_by_words()

    def get_type_by_words(self) -> str:  # TODO
        pass

    def get_val_by_words(self) -> str:  # TODO
        pass
