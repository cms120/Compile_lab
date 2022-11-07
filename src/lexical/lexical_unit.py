from enum import unique, Enum


@unique  # val值应该不相同
class LexicalUnit(Enum):
    INT = 'INT'  # 整形常数
    IDN = 'IDN'  # 标识符
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

    @classmethod
    def check_key(cls, key: str) -> bool:  # 检查key是否存在
        return key in cls.__members__.keys()

    @classmethod
    def check_val(cls, val: str) -> bool:  # 检查值是否存在
        return val in cls._value2member_map_.keys()
