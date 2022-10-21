import string
from enum import unique, Enum


@unique
class SyntaxUnit(Enum):  # 非终结符的key是自己，val是注释
    # 终结符的key是名称，val是实际值
    star = '*'
    point = '.'
    line = '|'
    l_par = '('
    r_par = ')'

    _const = '\'const\''
    _comma = '\',\''
    _semicolon = '\';\''
    _int = '\'int\''
    _equal = '\'=\''

    Program = 'program'
    compUnit = 'compUnit'
    EOF = 'eof'

    decl = 'declaration'
    funcDef = 'function_define'

    varDecl = 'variable_declaration'
    varDef = 'variable_define'

    constDecl = 'const_declaration'
    constDef = 'const_define'
    constInitVal = 'const_initial_variable'
    constExp = 'const_expression'

    bType = 'int'
    Ident = 'Ident'

    @classmethod
    def check_key(cls, key: str) -> bool:  # 检查key是否存在
        return key in cls.__members__.keys()

    @classmethod
    def check_val(cls, val: str) -> bool:  # 检查值是否存在
        return val in cls._value2member_map_.keys()


class Production:
    def __init__(self, left: SyntaxUnit, right: tuple[SyntaxUnit]):  # 产生式
        self.left = left
        self.right = right

    def __str__(self):
        str_m = self.left + ' -> '
        for su in self.right:
            str_m += su
        return str_m

    @staticmethod
    def init_by_string(line: str):
        left_right = line.split(' -> ')
        assert len(left_right) == 2, 'error left_right: ' + line

        right_groups = left_right[1].split(' ')
        assert len(right_groups) >= 1, 'error in right_group: ' + line

        left = SyntaxUnit[left_right[0]]
        right = []
        for group in right_groups:
            if group[0] in string.ascii_lowercase + string.ascii_uppercase:  # 非终结符
                assert SyntaxUnit.check_key(group), group + ' : ' + line  # 不在枚举类型中
                right.append(SyntaxUnit[group])

            else:  # 字符串 或者 正则表达式字符
                assert SyntaxUnit.check_val(group), group + ' : ' + line  # 不在枚举类型的值中
                right.append(SyntaxUnit(group))

        production = Production(left, tuple(right))
        return production


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


def get_g_c_minus_auto() -> Grammar:  # TODO 获得c--的文法
    grammar = Grammar(set())

    with open('src/syntax/c_minus_grammar.txt', 'r') as f:
        for line in f:
            i = 0
            while line[i] in string.digits + '. ':  # 跳过序号
                i += 1
            line = line[i:-2]
            grammar.productions.add(Production.init_by_string(line))  # 跳过换行符和分号

    return grammar
