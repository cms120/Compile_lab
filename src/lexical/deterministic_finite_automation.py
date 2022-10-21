from sqlalchemy import false

from src.lexical.finite_automation import FA
from src.lexical.rules import Rules
from src.lexical.state import State


class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # TODO:根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


def epsilon_closure_Move(I: list, letter: str, fa: FA):  # 将集合I转为J=move(I,letter)，再转为Ia=epsilon_closure{j}
    J = []
    I_letter = []
    for state in I:  # move动作
        key = (state, str)
        if (fa.f[key] != None):
            J.append(fa.f[key])

    for state in J:  # 得到Ia
        for state_2 in state.epsilonTransitions:
            if not (I_letter.__contains__(state_2)):
                I_letter.append[state_2]

    return I_letter
    pass


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化

    ListOfNewStateList = []  # 存储某状态经过epsilon_closure_Move后得到的状态列表
    dict1 = {}  # 字典dict1存储状态集——>新状态的映射
    state = State(False)
    Allstate = State.get_state_all  # get_state_all是不是改成静态方法好点？

    for state1 in Allstate:  # 获得fa的开始状态
        if (fa.s == state1.get_flag):
            S0 = state1

    for letter in fa.letters:
        ListOfNewStateList.append(epsilon_closure_Move(S0.epsilonTransitions, letter,
                                                       fa))  # 开始状态的Epsilon闭包通过letter达到的状态组成一个新状态集，存进ListOfNewStateList
        state2 = State(false)
        dict1[epsilon_closure_Move(S0.epsilonTransitions, letter, fa)] = state2  # 把初始状态集映射到一个新的状态
        # S0.transitions[letter]=state2

    for StateList in ListOfNewStateList:  # 遍历ListOfNewStateList中的状态集，经每个letter通过epsilon_closure_Move得到新的状态集再加进ListOfNewStateList再遍历，重复这个过程直到不产生新的状态集为止
        for letter in fa.letters:
            NewStateList = epsilon_closure_Move(StateList, letter, fa)
            if not (ListOfNewStateList.__contains__(NewStateList)):
                ListOfNewStateList.append(NewStateList)
                state3 = state(false)
                dict1[NewStateList] = state3  # 同样将得到的状态集NewStateList映射到一个新状态
                dict1[StateList].transitions[letter] = dict1[
                    NewStateList]  # 设置原状态的transitions映射：StateList映射到的原状态——letter——>NewStateList映射到的新状态

    rules = Rules(dict1.get(next(iter(dict1))),
                  dict1.get(list(dict1.keys())[-1]))  # 取字典中第一个值（状态）和最后一个值作为rule的start和end（python3中字典是按序存储的）

    Dfa = Rules.init_by_rules(rules)  # 根据规则构造FA，得到的是DFA

    return Dfa
    pass


def dfa_minimize(dfa) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合

    # 2.判断集合是否可“区分”

    # 3.对两个集合根据是否可再分继续划分集合，直到不可再划分为止

    pass
