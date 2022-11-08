from typing import List

from lexical.dfa import DFA, get_dfa_minimize_c_minus
from lexical.token import Token, LexicalUnit, tokens_to_format_str
from util import read_file, write_file


def get_token_by_content(content: str) -> Token:
    """
    分析一串字符所属的token

    :param content:一串字符 已经验证过可以被dfa接受
    :returns: token
    """
    assert len(content) > 0
    if LexicalUnit.check_val(content):  # 在unit中是否存在val
        return Token(LexicalUnit(content))
    elif content[0].isdigit():
        return Token(LexicalUnit('INT'), content)
    else:
        return Token(LexicalUnit('IDN'), content)


def get_token_list_by_line_dfa(dfa: DFA, line: str) -> List[Token]:
    """
    从一行c--代码中分析出tokens

    :param dfa: 最小化的dfa
    :param line: 一行c--代码
    :returns: tokens
    """
    res: List[Token] = []
    pre = nxt = 0  # 指针指向当前识别单词首位和正在识别的位置
    now_state = dfa.s
    is_end = 0

    while pre != len(line):
        if line[nxt:nxt + 2] == '//':
            break

        if line[nxt] == ' ' or line[nxt] == '\r' or line[nxt] == '\t':
            pre += 1
            nxt += 1
            continue

        while (now_state, line[nxt]) in dfa.f.keys() and dfa.f.get((now_state, line[nxt]), '') in dfa.f.values():
            if nxt == len(line) - 1:
                is_end = 1
                break
            now_state = dfa.f.get((now_state, line[nxt]))
            nxt += 1
        assert nxt + is_end > pre, 'line: ' + line + \
                                   '\tnxt: ' + str(nxt) + \
                                   '\tis_end: ' + str(is_end) + \
                                   '\tpre: ' + str(pre)
        res.append(get_token_by_content(line[pre:nxt + is_end]))

        if is_end == 1:
            break
        pre = nxt
        now_state = dfa.s

    return res


def get_token_list_by_content_dfa(dfa: DFA, content: List[str]) -> list[Token]:
    """
    从若干行c--程序中分析出tokens

    :param dfa: 最小化的dfa
    :param content: 若干行c--程序
    :returns: tokens
    """
    res = []
    for line in content:
        res.extend(get_token_list_by_line_dfa(dfa, line))
    return res


def analysis(file_path='resource/test.sy', is_read_file=True) -> list[Token]:  # 根据c--的dfa分析文件获得token list
    assert file_path.endswith(".sy"), 'file should end with .sy  ' + file_path

    tokens = get_token_list_by_content_dfa(get_dfa_minimize_c_minus(is_read_file), read_file(file_path))
    write_file(tokens_to_format_str(tokens), 'result/lexical/LA_tokens.txt')

    return tokens
