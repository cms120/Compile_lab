from collections import deque
from typing import Deque, Tuple, List, Set

from lexical.token import Token, tokens_val
from syntax.grammar import get_grammar_c_minus, Grammar
from syntax.production import is_terminal
from util import write_file, tuple_str


def states_format_str(states: List[Tuple[Tuple[str]]]) -> str:
    res = ''
    index = 1
    for state in states:
        line = str(index) + '\t' + state[0][-1] + '#' + state[1][-1] + '\t'
        if state[1][-1] == "'EOF'":
            line += 'accept'
        elif is_terminal(state[1][-1]):
            line += 'move'
        else:
            line += 'reduction'
        res += line + '\n'
    return res


def states_str(states: List[Tuple[Tuple[str]]]) -> str:
    res = ''
    for state in states:
        res += 'non_terminals:\t' + tuple_str(state[0]) + '\tinput: ' + tuple_str(state[1]) + '\n'
    return res


def analysis_reduction(right: Set[Tuple[str]], token_val: str, g: Grammar, non_ter_s: Deque[str]):
    """
    找到匹配的产生式将其压入栈
    """
    for r in right:  # 遍历产生式 找到匹配的产生式
        if token_val in g.get_r_first(r):
            r_list = list(r)
            r_list.reverse()
            non_ter_s.extend(r_list)  # 将产生式依次压入进栈
            return
    assert True


def analysis(tokens: Deque[Token]) -> List[Tuple[Tuple[str]]]:
    g = get_grammar_c_minus()
    g.check_ll1()

    states: List[Tuple[Tuple[str]]] = list()
    prods = g.get_prods()
    non_ter_s: Deque[str] = deque([g.get_s()])

    while len(tokens) > 0:
        states.append(tuple([tuple(non_ter_s), tuple(tokens_val(tokens))]))  # 将符号栈和输入栈存储
        token: Token = tokens.popleft()  # 当前输入符号
        non_ter: str = non_ter_s.pop()
        if token.get_unit_val() == non_ter:  # 匹配成功
            continue

        tokens.appendleft(token)  # a未匹配成功
        assert not is_terminal(non_ter), non_ter  # 不能匹配那么不能是终结符

        now_first = g.get_ch_first(non_ter)
        if token.get_unit_val() in now_first:  # a属于其中一个候选首符集
            analysis_reduction(prods.get(non_ter), token.get_unit_val(), g, non_ter_s)

        else:  # a不属于任意一个候选首符集 让 $ 自动匹配now
            now_follow = g.get_ch_follow(non_ter)
            assert '$' in now_first and token.get_unit_val() in now_follow, str(
                non_ter_s) + ' token: ' + token.get_val()  # 否则是语法错误

    write_file(states_str(states), 'result/syntax/LL1_states.txt')
    write_file(states_format_str(states), 'result/syntax/LL1_analysis.txt')
    return states
