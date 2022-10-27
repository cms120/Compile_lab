import random
import string
from copy import deepcopy
from typing import List, Set

from src.lexical.finite_automation import FA, get_fa_c_minus


class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # TODO:根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


def generate_random_str(randomlength):  # randomlength最大取值为26*2+10=62
    """
   从字符串“0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ”
   中随机抽取randomlength个字符组成状态字符串
    """
    a = string.digits

    str_list = random.sample(string.digits + string.ascii_letters, randomlength)
    random_str = ''.join(str_list)
    return random_str


def epsilon_closure(I: list, fa: FA):
    EC = I
    faf = fa.f
    f_to_list = list(faf.items())
    for state in EC:
        for tuple in f_to_list:
            if tuple[0] == (state, '$'):
                for Statee in tuple[1]:
                    if not EC.__contains__(Statee):
                        EC.append(Statee)

    return EC


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    #输入状态转换
    i = 0
    faf = fa.f
    fa_f_list  = list(faf.items())
    fa_letter_list = list(fa.letters)
    fa_z_list =fa.z
    dfa_k = []
    dfa_f = []
    #dfa_letters里不含有‘$'
    dfa_letters= fa_letter_list
    if dfa_letters.__contains__('$'):
     dfa_letters.remove('$')
    
    dfa_s = ''
    dfa_z = []
    # Listdict储存状态集到状态字符的映射，用一个二维列表表示，如[['S','E'],'A']
    Listdict = []

    # 把fa的开始状态也设为dfa的开始状态，并建立状态集合到状态字符的映射
    
    Listdict.append([set(epsilon_closure([fa.s], fa)), str(i)])
    dfa_s ='s'+ str(i)

    # 如果传进来的fa只有一个状态，也把他设为终止状态
    if len(list(fa.k)) == 1:
        dfa_z.append['s'+ str(i)]

    # ListOfStateList储存Listdict中的状态列表，便于遍历
    ListOfStateList = [list[0] for list in Listdict]

    # 遍历状态集，再遍历字符，再遍历状态。根据fa[2]即fa.f实现nfa确定化的子集法
    for StateList in ListOfStateList:
        for letter in fa_letter_list:
            if not letter == '$':
                StateList2 = []
                for State in StateList:
                    for tuple in fa_f_list:
                        if tuple[0] == (State, letter):
                            for Statee in tuple[1]:
                                if not StateList2.__contains__(Statee):
                                    StateList2.append(Statee)

                EC_StateList2 = epsilon_closure(StateList2, fa)
                C_EC_StateList2 = set(EC_StateList2)  # 转化为set，以免不同顺序的list被重复识别
                # 如果C_EC_StateList2不在ListOfStateList里，给它映射一个新状态字符串，并准备交给dfa.f建立关系
                if not ListOfStateList.__contains__(C_EC_StateList2) and not EC_StateList2 == []:
                    ListOfStateList.append(C_EC_StateList2)
                    i = i + 1
                    strr = 's'+str(i)
                    Listdict.append([set(EC_StateList2), strr])

                # 如果C_EC_StateList2在ListOfStateList里，从Listdict找到EC_StateList2对应的状态字符串，并准备交给dfa.f
                if ListOfStateList.__contains__(C_EC_StateList2) and not EC_StateList2 == []:
                    for list3 in Listdict:
                        if list3[0] == C_EC_StateList2:
                            strr = list3[1]

                # 构建dfa_f
                if not EC_StateList2 == []:
                    for list4 in Listdict:  # 从Listdict里找到StateList对应的状态字符串
                        if list4[0] == StateList:
                            if not list4[1] == '0':
                                dfa_f.append(((list4[1], letter), [strr]))
                            else:
                                dfa_f.append((('s'+list4[1], letter), [strr]))
                            # 构建dfa_z。如果StateList2里有fa的终结状态，则它对应的状态也是终结状态
                            for stre in fa_z_list:
                                if EC_StateList2.__contains__(stre) and not dfa_z.__contains__(strr):
                                    dfa_z.append(strr)

    # 用Listdict的状态字符集构造dfa_k
    L = [list[1] for list in Listdict]
    for state in L:
        if state=='0':
            dfa_k.append('s'+state)
        else:
            dfa_k.append(state)

    # 状态转换
    dfa_k = set(dfa_k)
    dfa_letters = set(dfa_letters)
    L1 = [list[0] for list in dfa_f]
    L2 = [list[1] for list in dfa_f]
    z = zip(L1, L2)
    dfa_f = dict(z)
    dfa_z = set(dfa_z)
    dfa = FA(dfa_k, dfa_letters, dfa_f, dfa_s, dfa_z)

    return dfa
    pass


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合
    dfa_nz = dfa.k - dfa.z
    dfa_z = dfa.z

    # defaultNewStateL储存最小化DFA备用状态字符
    mdfa_k = set()
    mdfa_f = []
    mdfa_letters = dfa.letters
    mdfa_s = ''
    mdfa_z = set()

    # target=[]#转移结果
    def get_source_set(target_set, char):
        source_set = set()
        for state in dfa.k:
            # print(states)
            try:
                for f in dfa.f:
                    if f == (state, char):
                        for statee in dfa.f[f]:

                            if statee in target_set:
                                source_set.add(state)
                            #   print(source_set)

            except KeyError:

                pass
        # print(source_set)
        return source_set

    P: List[Set[str]] = [dfa_z, dfa_nz]
    W: List[Set[str]] = [dfa_z, dfa_nz]
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
    Listdict: List[List[Set[str], str]] = []

    # 将新的状态集用字符表示
    for states in P:
        strr = generate_random_str(2)
        Listdict.append([states, strr])

    # 得到新的k,f,s,z
    for states in P:
        for letter in dfa.letters:
            for list4 in Listdict:
                if list4[0] == states:

                    for state in list4[0]:
                        for list1 in dfa.f:
                            if list1 == (state, letter):
                                # if not mdfa_f.__contains__(((list[1], letter), list1[1])):

                                tar = dfa.f[list1]
                                mdfa_f.append(((list4[1], letter), tar))

                        if state in dfa.s:
                            mdfa_s = list4[1]
                        if state in dfa.z:
                            if not mdfa_z.__contains__(list4[1]):
                                mdfa_z.add(list4[1])
    l1 = []
    l2 = []
    for list2 in mdfa_f:
        for list3 in Listdict:
            for state1 in list3[0]:

                if list2[1][0] == state1:
                    list2[1][0] = list3[1]

    # 如果传进来的fa只有一个状态，也把他设为终止状态
    if len(dfa.k) == 1:
        strr = generate_random_str(2)
        mdfa_z.add(strr)

    L = [list[1] for list in Listdict]
    for states in L:
        mdfa_k.add(states)
    mdfa_letters = dfa.letters
    lmdfa_f = []
    for item in mdfa_f:
        if lmdfa_f.count(item) < 1:
            lmdfa_f.append(item)
    for i in lmdfa_f:
        l1.append(i[0])
        l2.append(i[1])
    z = zip(l1, l2)

    z1 = list(z)
    z2 = dict(z1)

    mdfa = FA(mdfa_k, mdfa_letters, z2, mdfa_s, mdfa_z)
    return mdfa


def get_dfa_c_minus() -> DFA:  # 获得 c-- 确定化的DFA
    return fa_2_dfa(get_fa_c_minus())


def get_dfa_minimize_c_minus() -> DFA:  # 获得c--的 最小化 dfa
    return DFA.init_by_fa(get_fa_c_minus())
