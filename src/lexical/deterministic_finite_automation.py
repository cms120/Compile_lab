import random

from finite_automation import FA


class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # TODO:根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    defaultNewStateL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    dfa_k = []
    dfa_f = []
    dfa_letters = fa[1]
    dfa_s = ''
    dfa_z = []

    Listdict = []
    char = random.choice(defaultNewStateL)
    defaultNewStateL.remove(char)
    Listdict.append([[fa[3]], char])
    dfa_s = char
    if len(fa[0]) == 1:
        dfa_z.append[char]

    ListOfStateList = [list[0] for list in Listdict]
    for StateList in ListOfStateList:
        for letter in fa[1]:
            for State in StateList:
                for tuple in fa[2]:
                    if tuple[0] == (State, letter):
                        for Statee in tuple[1]:
                            StateList2 = []
                            if not StateList2.__contains__(Statee):
                                StateList2.append(Statee)
                if not ListOfStateList.__contains__(StateList2):
                    char = random.choice(defaultNewStateL)
                    defaultNewStateL.remove(char)
                    Listdict.append([StateList2, char])
                    ListOfStateList = [list[0] for list in Listdict]
                    for list4 in Listdict:
                        if list4[0] == StateList:
                            dfa_f.append((list4[1], letter), [char])

                    for str in fa[4]:
                        if StateList2.__contains__(str):
                            dfa_z.append(char)
                            break

    for value in dict.values():
        dfa_k.append(value)

    dfa = [
        dfa_k,
        dfa_letters,
        dfa_f,
        dfa_s,
        dfa_z
    ]

    return dfa


def dfa_minimize(dfa) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合

    # 2.判断集合是否可“区分”

    # 3.对两个集合根据是否可再分继续划分集合，直到不可再划分为止

    pass
