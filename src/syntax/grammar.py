import string
from enum import unique, Enum

from src.util import read_file


@unique
class SyntaxUnit(Enum):  # 非终结符的key是自己，val是注释
    # 终结符的key是名称，val是实际值

    # 正则表达式关键字 TODO
    regex_star = '*'
    regex_point = '.'
    regex_line = '|'
    regex_l_par = '('
    regex_r_par = ')'
    regex_question = '?'
    regex_hash = '#'  # TODO

    regex_int_const = '[0-9]+'  # 整形常数
    regex_ident = '[a-zA-Z_][a-zA-Z_0-9]*'  # 标识符

    # 终结符

    # 运算符
    _add = '\'+\''
    _minus = '\'-\''
    _plus = '\'*\''
    _exclamation = '\'!\''
    _divide = '\'/\''
    _int_divide = '\'%\''
    _assign = '\'=\''

    _equal = '\'==\''
    _less = '\'<\''
    _more = '\'>\''
    _less_or_equal = '\'<=\''
    _more_or_equal = '\'>=\''
    _not_equal = '\'!=\''
    _and = '\'&&\''
    _or = '\'||\''

    # 界符
    _comma = '\',\''
    _semicolon = '\';\''
    _l_par = '\'(\''
    _r_par = '\')\''
    _l_brace = '\'{\''
    _r_brace = '\'}\''

    _const = '\'const\''
    _void = '\'void\''
    _int = '\'int\''
    _return = '\'return\''
    _main = '\'main\''

    Program = 'program'
    compUnit = 'compUnit'
    EOF = 'eof'

    block = 'block'
    blockItem = 'block_item'

    decl = 'declaration'
    funcDef = 'function_define'
    funcType = 'function_type'
    funcFParams = 'function_f_params'
    funcFParam = 'function_f_param'
    funcRParams = 'func_r_params'
    funcRParam = 'function_r_param'

    varDecl = 'variable_declaration'
    varDef = 'variable_define'

    constDecl = 'const_declaration'
    constDef = 'const_define'
    constInitVal = 'const_initial_variable'
    constExp = 'const_expression'

    stmt = 'stmt'
    lVal = 'left_variable'

    bType = 'int'
    Ident = 'Ident'
    initVal = 'initial_variable'
    exp = 'expression'
    cond = 'cond'

    number = 'number'
    IntConst = 'int_const'

    lOrExp = 'left_or_expression'
    lAndExp = 'left_and_expression'
    primaryExp = 'primary_expression'
    addExp = 'add_expression'
    unaryExp = 'unary_expression'
    unaryOp = 'unary_op'
    mulExp = 'multiple_expression'
    relExp = 'res_expression'
    eqExp = 'equal_expression'

    add1 = 'add1'

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
        str_m = self.left.value + ' ->'
        for unit in self.right:
            str_m += ' ' + unit.value
        return str_m

    @staticmethod
    def init_by_string(line: str):
        left_right = line.split(' -> ')
        assert len(left_right) == 2, 'error left_right: ' + line

        right_groups = left_right[1].split(' ')
        assert len(right_groups) >= 1, 'error in right_group: ' + line

        assert SyntaxUnit.check_key(left_right[0]), 'error left: ' + line
        left = SyntaxUnit[left_right[0]]
        right = []
        for group in right_groups:
            assert group, line
            if group[0] in string.ascii_lowercase + string.ascii_uppercase:  # 非终结符
                assert SyntaxUnit.check_key(group), group + ' : ' + line  # 不在枚举类型中
                right.append(SyntaxUnit[group])

            else:  # 字符串 或者 正则表达式关键字
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


def get_g_c_minus_auto() -> Grammar:
    grammar = Grammar(set())
    content = read_file('src/syntax/c_minus_grammar.txt')
    lines = content.split('\n')

    for line in lines:
        i = 0
        while line[i] in string.digits + '. ':  # 跳过序号
            i += 1
        line = line[i:]
        if line.endswith(';'):
            line = line[:-1]
        grammar.productions.add(Production.init_by_string(line))

    return grammar
