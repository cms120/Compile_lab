from typing import List

from src.lexical.dfa_shan import DFA, get_dfa_minimize_c_minus
from src.lexical.token import Token, LexicalUnit
from src.util import read_file2


def analysis(file_path='test.sy', is_read_file=True) -> list[Token]:  # 根据c--的dfa分析文件获得token list
    assert file_path.endswith(".sy"), 'file should end with .sy  ' + file_path
    return get_token_list_by_content_dfa(get_dfa_minimize_c_minus(is_read_file), read_file2(file_path))


def get_token_by_content(content_unit: str) -> Token:
    if LexicalUnit.check_val(content_unit):  # 在unit中是否存在val
        return Token(LexicalUnit(content_unit))
    elif content_unit[0].isdigit():
        return Token(LexicalUnit['regex_int_const'], content_unit)
    else:
        return Token(LexicalUnit['regex_ident'], content_unit)


def get_token_list_by_content_dfa(dfa: DFA, content: str) -> list[Token]:
    res: List[Token] = []
    pre = nxt = 0  # 指针指向当前识别单词首位和正在识别的位置
    now_state = dfa.s
    isEnd = 0
    while pre != len(content):
        if content[nxt] == ' ' or content[nxt] == '\r' or content[nxt] == '\n' or content[nxt] == '\t':
            pre += 1
            nxt += 1
            continue

        while (now_state, content[nxt]) in dfa.f.keys() and dfa.f.get((now_state, content[nxt]), '') in dfa.f.values():
            if nxt == len(content) - 1:
                isEnd = 1
                break
            now_state = dfa.f.get((now_state, content[nxt]))
            nxt += 1
        # assert now_state in dfa.z, 'error ' + now_state + ' ' + \
        #                            str(pre) + content[pre] + ' ' + str(nxt) + content[nxt]  # TODO 输出想要的信息 不会写

        res.append(get_token_by_content(content[pre:nxt + isEnd]))

        if isEnd == 1:
            break
        pre = nxt
        now_state = dfa.s

    return res


def get_token_list_by_line(dfa: DFA, line: str) -> List[Token]:
    res: List[Token] = []
    return res
