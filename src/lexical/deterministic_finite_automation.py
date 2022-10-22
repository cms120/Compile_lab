from finite_automation import FA, get_fa_c_minus


class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # TODO:根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    # defaultNewStateL储存DFA备用状态字符
    defaultNewStateL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    dfa_k = []
    dfa_f = []
    dfa_letters = fa[1]
    dfa_s = ''
    dfa_z = []
    # Listdict储存状态集到状态字符的映射，用一个二维列表表示，如[['S','E'],'A']
    Listdict = []

    # 把fa的开始状态也设为dfa的开始状态，并建立状态集合到状态字符的映射
    char = defaultNewStateL[0]
    defaultNewStateL.remove(char)
    Listdict.append([[fa[3]], char])
    dfa_s = char

    # 如果传进来的fa只有一个状态，也把他设为终止状态
    if len(fa[0]) == 1:
        dfa_z.append[char]

    # ListOfStateList储存Listdict中的状态列表，便于遍历
    ListOfStateList = [list[0] for list in Listdict]

    # 遍历状态集，再遍历字符，再遍历状态。根据fa[2]即fa.f实现nfa确定化的子集法
    for StateList in ListOfStateList:
        for letter in fa[1]:
            StateList2 = []
            for State in StateList:
                for tuple in fa[2]:
                    if tuple[0] == (State, letter):
                        for Statee in tuple[1]:
                            if not StateList2.__contains__(Statee):
                                StateList2.append(Statee)

            # 如果StateList2不在ListOfStateList里，给它映射一个新状态字符，并准备交给dfa.f建立关系
            if not ListOfStateList.__contains__(StateList2) and not StateList2 == []:
                char = defaultNewStateL[0]
                defaultNewStateL.remove(char)
                Listdict.append([StateList2, char])
                ListOfStateList.append(StateList2)

            # 如果StateList2在ListOfStateList里，从Listdict找到StateList2对应的状态字符，并准备交给dfa.f
            if ListOfStateList.__contains__(StateList2) and not StateList2 == []:
                for list3 in Listdict:
                    if list3[0] == StateList2:
                        char = list3[1]

            # 构建dfa_f
            if not StateList2 == []:
                for list4 in Listdict:
                    if list4[0] == StateList:
                        dfa_f.append(((list4[1], letter), [char]))

                        # 构建dfa_z。如果StateList2里有fa的终结状态，则它对应的状态也是终结状态
                        for str in fa[4]:
                            if StateList2.__contains__(str) and not dfa_z.__contains__(char):
                                dfa_z.append(char)

    # 用Listdict的状态字符集构造dfa_k
    L = [list[1] for list in Listdict]
    for state in L:
        dfa_k.append(state)

    dfa = [
        dfa_k,
        dfa_letters,
        dfa_f,
        dfa_s,
        dfa_z
    ]

    return dfa
    pass


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合

    # 2.判断集合是否可“区分”

    # 3.对两个集合根据是否可再分继续划分集合，直到不可再划分为止

    pass


def get_dfa_c_minus() -> DFA:  # 获得c--的dfa
    return DFA.init_by_fa(get_fa_c_minus())
