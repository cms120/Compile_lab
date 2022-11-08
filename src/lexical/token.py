from collections import deque
from typing import List, Deque

from c_mimus import c_minus_keyword, c_minus_op
from lexical.lexical_unit import LexicalUnit


class Token:
    def __init__(self, words: LexicalUnit, val=''):
        self.words = words
        self.val = val

    def __str__(self) -> str:
        if self.words == LexicalUnit.IDN:
            return 'IDN: ' + self.val
        elif self.words == LexicalUnit.INT:
            return 'INT: ' + self.val
        else:
            return str(self.words.value)

    def get_val(self) -> str:
        if self.words == LexicalUnit.IDN or self.words == LexicalUnit.INT:
            return self.val
        else:
            return str(self.words.value)

    def format_str(self) -> str:
        """
        格式化输出token
        """
        if self.words == LexicalUnit.IDN:
            return self.val + '\t<IDN,' + self.val + '>'
        elif self.words == LexicalUnit.INT:
            return self.val + '\t<INT,' + self.val + '>'
        else:
            res = self.words.value + '\t<'
            if self.words.value in c_minus_keyword:
                res += 'KW, >'
            elif self.words.value in c_minus_op:
                res += 'OP, >'
            else:
                res += 'SE, >'
            return res


def tokens_to_str(tokens: List[Token]) -> str:
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
