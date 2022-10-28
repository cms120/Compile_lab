from enum import unique, Enum


@unique  # val值应该不相同
class LexicalUnit(Enum):
    regex_int_const = '[0-9]+'  # 整形常数
    regex_ident = '[a-zA-Z_][a-zA-Z_0-9]*'  # 标识符
    # 终结符

    # 运算符
    _add = '+'
    _minus = '-'
    _plus = '*'
    _exclamation = '!'
    _divide = '/'
    _int_divide = '%'
    _assign = '='

    _equal = '=='
    _less = '<'
    _more = '>'
    _less_or_equal = '<='
    _more_or_equal = '>='
    _not_equal = '!='
    _and = '&&'
    _or = '||'

    # 界符
    _comma = ','
    _semicolon = ';'
    _l_par = '('
    _r_par = ')'
    _l_brace = '{'
    _r_brace = '}'

    _const = 'const'
    _void = 'void'
    _int = 'int'
    _return = 'return'
    _main = 'main'


class Token:
    def __init__(self, words_unit: LexicalUnit, val=''):
        self.words = words_unit
        self.val = val
