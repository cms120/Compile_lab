import random
import string
from copy import deepcopy

from finite_automation import FA, get_fa_c_minus


class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # TODO:根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


def generate_random_str(randomlength):  # randomlength最大取值为26*2+10=62
    '''
   从字符串“0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ”
   中随机抽取randomlength个字符组成状态字符串
    '''
    a = string.digits

    str_list = random.sample(string.digits + string.ascii_letters, randomlength)
    random_str = ''.join(str_list)
    return random_str


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    # defaultNewStateL储存DFA备用状态字符
    dfa_k = []
    dfa_f = []
    dfa_letters = fa.letters
    dfa_s = ''
    dfa_z = []
    # Listdict储存状态集到状态字符的映射，用一个二维列表表示，如[['S','E'],'A']
    Listdict = []

    # 把fa的开始状态也设为dfa的开始状态，并建立状态集合到状态字符的映射
    strr = generate_random_str(2)
    Listdict.append([[fa.s], strr])
    dfa_s = strr

    # 如果传进来的fa只有一个状态，也把他设为终止状态
    if len(fa.k) == 1:
        dfa_z.append[strr]

    # ListOfStateList储存Listdict中的状态列表，便于遍历
    ListOfStateList = [list[0] for list in Listdict]

    # 遍历状态集，再遍历字符，再遍历状态。根据fa[2]即fa.f实现nfa确定化的子集法
    for StateList in ListOfStateList:
        for letter in fa.letters:
            StateList2 = []
            for State in StateList:
                for tuple in fa.f:
                    if tuple[0] == (State, letter):
                        for Statee in tuple[1]:
                            if not StateList2.__contains__(Statee):
                                StateList2.append(Statee)

            # 如果StateList2不在ListOfStateList里，给它映射一个新状态字符串，并准备交给dfa.f建立关系
            if not ListOfStateList.__contains__(StateList2) and not StateList2 == []:
                ListOfStateList.append(StateList2)
                while 1:
                    L = [list[1] for list in Listdict]
                    strr = generate_random_str(2)
                    if not L.__contains__(strr):
                        Listdict.append([StateList2, strr])
                        break

            # 如果StateList2在ListOfStateList里，从Listdict找到StateList2对应的状态字符串，并准备交给dfa.f
            if ListOfStateList.__contains__(StateList2) and not StateList2 == []:
                for list3 in Listdict:
                    if list3[0] == StateList2:
                        strr = list3[1]

            # 构建dfa_f
            if not StateList2 == []:
                for list4 in Listdict:
                    if list4[0] == StateList:
                        dfa_f.append(((list4[1], letter), [strr]))

                        # 构建dfa_z。如果StateList2里有fa的终结状态，则它对应的状态也是终结状态
                        for str in fa.z:
                            if StateList2.__contains__(str) and not dfa_z.__contains__(strr):
                                dfa_z.append(strr)

    # 用Listdict的状态字符集构造dfa_k
    L = [list[1] for list in Listdict]
    for state in L:
        dfa_k.append(state)

    dfa = FA(dfa_k, dfa_letters, dfa_f, dfa_s, dfa_z)

    return dfa
    pass


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合
    dfa_nz = set(dfa.k) - set(dfa.z)
    dfa_z = set(dfa.z)

    # defaultNewStateL储存最小化DFA备用状态字符
    mdfa_k = []
    mdfa_f = []
    mdfa_letters = dfa.letters
    mdfa_s = ''
    mdfa_z = []
    #target=[]#转移结果
    def get_source_set(target_set, char):
        source_set = set()
        for state in dfa.k:

            try:
                for puple in dfa.f:
                  if puple[0] == (state,char) :
                      for statee in puple[1]:
                          if statee in target_set:
                             source_set.add(state)
                            # print(source_set)

            except KeyError:

                pass
        #print(source_set)
        return source_set


    P = [dfa_z, dfa_nz]
    W = [dfa_z, dfa_nz]
    # 2得到划分出的新的状态集

    while W:

        A = random.choice(W)
        W.remove(A)

        for char in dfa.letters:
            X = get_source_set(A, char)
            ''' print(W)
            print(P)
            print(A)
            print(X)'''
            P_temp = []

            for Y in P:
                S = X & Y
                S1 = Y - X

                if len(S) and len(S1):
                    P_temp.append(S)
                    P_temp.append(S1)

                    if Y in W:
                        W.remove(Y)
                        W.append(S)
                        W.append(S1)
                    else:
                        if len(S) <= len(S1):
                            W.append(S)
                        else:
                            W.append(S1)
                else:
                    P_temp.append(Y)
            P = deepcopy(P_temp)
    # P即为所求状态集
    # Listdict储存状态集到状态字符的映射，用一个二维列表表示，如[['S','E'],'A']
    Listdict = []


    # 将新的状态集用字符表示
    for state in P :
        strr = generate_random_str(2)
        Listdict.append([state, strr])
    # 得到新的k,f,s,z
    for state in P:
        for letter in dfa.letters:
            for list in Listdict :
                if list[0]==state:

                    for statee in list[0]:
                        for list1 in dfa.f:
                            if list1[0]==(statee,letter) :
                                #if not mdfa_f.__contains__(((list[1], letter), list1[1])):



                                      mdfa_f.append(((list[1], letter), list1[1]))

                        if statee in dfa.s:
                            mdfa_s = list[1]
                        if statee in dfa.z:
                            if not mdfa_z.__contains__(list[1]):
                              mdfa_z.append(list[1])

    for list2 in mdfa_f:
        for list in Listdict:
            for state1 in list[0]:

                if list2[1][0] == state1 :
                    list2[1][0] = list[1]








    # 如果传进来的fa只有一个状态，也把他设为终止状态
    if len(dfa.k) == 1:
        strr = generate_random_str(2)
        mdfa_z.append[strr]

    L = [list[1] for list in Listdict]
    for state in L:
        mdfa_k.append(state)
    mdfa_letters = dfa.letters
    lmdfa_f=[]
    for item in mdfa_f:
        if lmdfa_f.count(item)<1:
            lmdfa_f.append(item)
    mdfa = FA(mdfa_k, mdfa_letters, lmdfa_f, mdfa_s, mdfa_z)
    return mdfa

    pass


def get_dfa_c_minus() -> DFA:  # 获得c--的dfa
    return DFA.init_by_fa(get_fa_c_minus())

