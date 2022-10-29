from typing import List

from src.lexical.dfa_shan import DFA, get_dfa_minimize_c_minus
from src.lexical.token import Token, LexicalUnit
from src.util import read_file


def analysis(file_path='test.sy', is_read_file=True) -> list[Token]:  # 根据c--的dfa分析文件获得token list
    assert file_path.endswith(".sy"), 'file should end with .sy  ' + file_path
    res = get_token_list_by_content_dfa(get_dfa_minimize_c_minus(is_read_file), read_file(file_path))
    res_output(res)
    return res


def res_output(tokens: List[Token], file='lexical_result.txt') -> None:



def get_token_by_content(content: str) -> Token:
    if LexicalUnit.check_val(content):  # 在unit中是否存在val
        return Token(LexicalUnit(content))
    elif content[0].isdigit():
        return Token(LexicalUnit['regex_int_const'], content)
    else:
        return Token(LexicalUnit['regex_ident'], content)


def get_token_list_by_content_dfa(dfa: DFA, content: List[str]) -> list[Token]:
    res = []
    for line in content:
        res.extend(get_token_list_by_line_dfa(dfa, line))
    return res


def get_token_list_by_line_dfa(dfa: DFA, line: str) -> List[Token]:
    res: List[Token] = []
    pre = nxt = 0  # 指针指向当前识别单词首位和正在识别的位置
    now_state = dfa.s
    isEnd = 0

    while pre != len(line):
        if line[nxt:nxt + 2] == '//':
            break

        if line[nxt] == ' ' or line[nxt] == '\r' or line[nxt] == '\t':
            pre += 1
            nxt += 1
            continue

        while (now_state, line[nxt]) in dfa.f.keys() and dfa.f.get((now_state, line[nxt]), '') in dfa.f.values():
            if nxt == len(line) - 1:
                isEnd = 1
                break
            now_state = dfa.f.get((now_state, line[nxt]))
            nxt += 1

        res.append(get_token_by_content(line[pre:nxt + isEnd]))

        if isEnd == 1:
            break
        pre = nxt
        now_state = dfa.s

    return res
