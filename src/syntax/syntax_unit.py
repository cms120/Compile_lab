from enum import Enum, unique


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

    def get_terminator(self) -> tuple:  # 获得一系列终结符
        pass
