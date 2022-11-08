from collections import deque
from typing import List, Deque

from c_mimus import c_minus_keyword, c_minus_op
from lexical.lexical_unit import LexicalUnit


class Token:
    def __init__(self, unit: LexicalUnit, val=''):
        self.__unit = unit
        self.__val = val

    def __str__(self) -> str:
        if self.__unit == LexicalUnit.IDN:
            return 'IDN: ' + self.__val
        elif self.__unit == LexicalUnit.INT:
            return 'INT: ' + self.__val
        else:
            return str(self.__unit.value)

    def get_val(self) -> str:
        """
        获得程序原本符号
        """
        if self.__unit == LexicalUnit.IDN or self.__unit == LexicalUnit.INT:
            return "'" + self.__val + "'"
        else:
            return "'" + str(self.__unit.value) + "'"

    def format_str(self) -> str:
        """
        格式化输出token
        """
        if self.__unit == LexicalUnit.IDN:
            return self.__val + '\t<IDN,' + self.__val + '>'
        elif self.__unit == LexicalUnit.INT:
            return self.__val + '\t<INT,' + self.__val + '>'
        else:
            res = self.__unit.value + '\t<'
            if self.__unit.value in c_minus_keyword:
                res += 'KW, >'
            elif self.__unit.value in c_minus_op:
                res += 'OP, >'
            else:
                res += 'SE, >'
            return res

    def get_unit_name(self) -> str:
        return self.__unit.name

    def get_unit_val(self) -> str:
        """
        获得终结符
        """
        return "'" + str(self.__unit.value) + "'"


def tokens_val(tokens: Deque[Token]) -> List[str]:
    """
    将tokens转为程序
    """
    res = []
    for token in tokens:
        res.append(token.get_val())
    return res


def tokens_to_format_str(tokens: List[Token]) -> str:
    res = ''
    for token in tokens:
        res += token.format_str() + '\n'
    return res


def tokens_to_deque(tokens: List[Token]) -> Deque[str]:
    """
    将tokens翻转为stack
    """
    res: Deque[str] = deque()
    for token in tokens:
        res.append("'" + token.get_val() + "'")

    res.reverse()
    return res
