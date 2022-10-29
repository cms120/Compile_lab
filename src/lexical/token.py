from src.c_mimus import c_minus_keyword, c_minus_op
from src.lexical.lexical_unit import LexicalUnit


class Token:
    def __init__(self, words_unit: LexicalUnit, val=''):
        self.words = words_unit
        self.val = val

    def __str__(self):
        if self.words == LexicalUnit.regex_ident:
            return 'IDN: ' + self.val
        elif self.words == LexicalUnit.regex_int_const:
            return 'INT: ' + self.val
        else:
            return self.words.value

    def format_str(self):  # TODO
        """
        格式化输出token
        """
        if self.words == LexicalUnit.regex_ident:
            return self.val + '\t<IDN,' + self.val + '>'
        elif self.words == LexicalUnit.regex_int_const:
            return self.val + '\t<INT,' + self.val + '>'
        else:
            res = self.words.value + '\t<'
            if self.words.value in c_minus_keyword:
                res += 'KE, >'
            elif self.words.value in c_minus_op:
                res += 'OP, >'
            else:
                res += 'SE, >'
            return res
