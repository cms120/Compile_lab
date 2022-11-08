from collections import deque
from typing import Deque, Tuple, List

from syntax.grammar import get_grammar_c_minus
from syntax.production import is_terminal
from util import write_file


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


def state_str(states: List[Tuple[Tuple[str]]]) -> str:
    pass


def analysis(tokens: Deque[str]) -> List[Tuple[Tuple[str]]]:  # TODO
    g = get_grammar_c_minus()
    g.set_first()

    # g.check_ll1()

    states: List[Tuple[Tuple[str]]] = list()
    prods = g.get_prods()
    non_ter_s: Deque[str] = deque([g.get_s()])

    while len(tokens) > 0:
        states.append(tuple([tuple(non_ter_s), tuple(tokens)]))  # 将符号栈和输入栈存储
        a: str = tokens.pop()  # 当前输入符号
        non_ter: str = non_ter_s.pop()
        if a == non_ter:
            continue

        tokens.append(a)  # a未匹配成功
        assert not is_terminal(non_ter)  # 不能匹配那么不能是非终结符

        now_first = g.get_ch_first(non_ter)
        if a in now_first:  # a属于其中一个候选首符集
            for r in prods.get(a):
                if a in g.get_r_first(r):
                    non_ter_s.append(r)
                    break
        else:  # a不属于任意一个候选首符集 让 $ 自动匹配now
            now_follow = g.get_ch_follow(non_ter)
            assert '$' in now_first and a in now_follow, non_ter_s + a  # 否则是语法错误

    # TODO
    write_file(states_format_str(states), 'src/syntax/LL1_analysis.txt')
    return states