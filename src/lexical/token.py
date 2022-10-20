LexicalUnitKeyword = {
    '_int': 'int',
    '_void': 'void',
    '_return': 'return',
    '_const': 'const',
    '_main': 'main',
}
LexicalUnitDelimiter = {
    'l_par': '(',
    'r_par': ')',
    'l_brace': '{',
    'r_brace': '}',
    'comma': ',',
    'semicolon': ';'
}

LexicalUnitOp = {
    '_commonOp': '+-*/%',
    '_compareOp': '< > <= >= == !=',
    '_boolOp': '&& ||',
    '_assignOp': '='
}

LexicalUnitOther = {
    '_IDN': 'idn',  # 标识符: 变量名、函数名
    'C': 'c',  # 整形常数
    '_fp': 'fp',  # 浮点型常数
}


def merge_dict(d1: dict, d2: dict) -> dict:  # 合并两个字典 两个字典不能有相同的key
    res = dict()
    for k, v in d1.items():
        res[k] = v
    for k, v in d2.items():
        assert (k in res.keys(), '字典含有相同key')
        res[k] = v
    return res


LexicalUnit = merge_dict(merge_dict(LexicalUnitKeyword, LexicalUnitDelimiter),
                         merge_dict(LexicalUnitOp, LexicalUnitOther))


class Token:
    def __init__(self, lu: str, val: int):
        self.lu = lu
        self.val = val
