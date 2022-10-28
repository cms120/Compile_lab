from copy import deepcopy

from lexical.token import Token, LexicalUnit
from src.lexical.dfa_shan import DFA, get_dfa_minimize_c_minus
from src.util import read_file


def analysis(file_path='test.sy') -> list[Token]:  # 根据c--的dfa分析文件获得token list
    return get_token_list_by_content_dfa(get_dfa_minimize_c_minus(), read_file(file_path))


def get_token_list_by_content_dfa(dfa: DFA, content: str) -> list[Token]:
    res = []
    pre = nxt = 0  # 指针指向当前识别单词首位和正在识别的位置
    now_state = dfa.s
    while pre != len(content):
        if content[nxt] == ' ' or content[nxt] == '\r' or content[nxt] == '\n' or content[nxt] == '\t':
            pre += 1
            nxt += 1
            continue
        while (now_state, content[nxt]) in dfa.f.keys() and dfa.f.get((now_state, content[nxt]), '#') in dfa.f.values():
            if nxt == len(content):
                break
            now_state = dfa.f.get((now_state, content[nxt]))
            nxt += 1
        assert now_state in dfa.z, 'error'  # TODO 输出想要的信息 不会写

        content_unit = deepcopy(content[pre:nxt + (nxt == len(content))])
        if content_unit in LexicalUnit.name:
            res.append(Token(LexicalUnit(content_unit)))
        elif content_unit[0].isdigit():
            res.append(Token(LexicalUnit['regex_int_const'], content_unit))
        else:
            res.append(Token(LexicalUnit['regex_ident'], content_unit))
        pre = nxt
        now_state = dfa.s

    return res
