import os
import pickle
import random
from collections import deque
from typing import Set, Dict, Deque, Tuple, List

from src import util
from src.lexical.finite_automation import FA, get_fa_c_minus


class GetNewK:
    __FLAG = ''

    @classmethod
    def get_flag(cls) -> str:
        cls.__FLAG = str(int(cls.__FLAG) + 1)
        return cls.__FLAG

    @classmethod
    def reset(cls):
        cls.__FLAG = '-1'


class DFA:

    def __init__(self, k: set[str], letters: set[str], f: dict[tuple[str, str], str], s: str, z: set[str]):
        self.k = k  # 状态集
        self.letters = letters  # 字母表
        self.f = f  # 转换函数集 示例 f(S,0)=Q 那么在list中存入的是 ( (S,0) , Q )
        self.s = s  # 唯一初态Í
        self.z = z  # 终态集

    def __str__(self):
        return 'k:\t' + str(self.k) + '\n' + \
               'letters:\t' + str(self.letters) + '\n' + \
               'f:\t' + str(self.f) + '\n' + \
               's:\t' + str(self.s) + '\n' + \
               'z:\t' + str(self.z) + '\n'


def get_ks_closure(ks: set[str], fa: FA) -> tuple[str]:  # 获取若干个字符的epsilon闭包
    k_dead = set()  # 存储已访问过的状态
    k_live_stack: Deque[str] = deque(ks)  # 存储待访问的状态

    res: Set[str] = set()
    while len(k_live_stack) != 0:
        k = k_live_stack.pop()
        k_dead.add(k)
        res.add(k)

        k_news = fa.f.get((k, '$'))
        if k_news is None:
            continue
        for k_new in k_news:
            if k_new not in k_dead:
                k_live_stack.append(k_new)

    return tuple(res)


def get_ks_letter(ks: set[str], fa, letter) -> tuple[str]:
    """
    若干个状态 经letter到达的状态集
    ks : 已经是epsilon闭包
    """
    assert letter != '$'

    res = set()
    for k in ks:  # 查询每个字符 由letter可到达的状态
        ks_new = fa.f.get((k, letter))
        if ks_new is not None:
            res = res | set(ks_new)

    if len(res) == 0:  # 这些状态由letter不能到达别的状态
        return tuple()
    else:
        return get_ks_closure(res, fa)  # 返回这些状态的epsilon闭包


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    GetNewK.reset()
    fa_s_epsilon_closure = get_ks_closure({fa.s}, fa)  # 获得fa.s 的epsilon闭包

    dfa_k_stack: Deque[Tuple[str]] = deque([fa_s_epsilon_closure])  # 存储待访问的 dfa.k
    dfa_k_dead: Set[Tuple[str]] = set()  # 存储已访问过的 dfa.k

    dfa_k_dict = {fa_s_epsilon_closure: GetNewK.get_flag()}  # 存储dfa.k 的转化

    dfa_letters = fa.letters  # 维护dfa的letters
    dfa_letters.discard('$')  # dfa中不含$
    dfa_f: Dict[(str, str), str] = dict()
    dfa_z = set()  # 获得dfa的z

    while len(dfa_k_stack) != 0:
        dfa_k_now = dfa_k_stack.pop()
        dfa_k_dead.add(dfa_k_now)

        if util.check_set_if_exist(set(dfa_k_now), fa.z):  # 如果dfa.k 中含有任意一个fa.z 那么就是终态
            dfa_z.add(dfa_k_dict[dfa_k_now])

        for letter in fa.letters:  # 即求出表中的一格
            dfa_k_new = get_ks_letter(set(dfa_k_now), fa, letter)
            if len(dfa_k_new) == 0:
                continue  # 该格为空

            if dfa_k_new not in dfa_k_dead:  # 这个 dfa_k 未被访问过
                dfa_k_stack.append(dfa_k_new)

            if dfa_k_new not in dfa_k_dict.keys():  # 这个状态还没有转化
                dfa_k_dict[dfa_k_new] = GetNewK.get_flag()

            dfa_f[(dfa_k_dict[dfa_k_now], letter)] = dfa_k_dict[dfa_k_new]

    return DFA(set(dfa_k_dict.values()), dfa_letters, dfa_f, dfa_k_dict[fa_s_epsilon_closure], dfa_z)


def get_source_set(target_set: set, letter: str, dfa: DFA):
    res_set = set()
    for state in dfa.k:
        if dfa.f.get((state, letter), '#') in target_set:
            res_set.add(state)
    return res_set


def get_final_split_set(dfa: DFA) -> List[Set[str]]:  # 获得dfa的集合划分
    p = [dfa.k - dfa.z, dfa.z]
    w = [dfa.k - dfa.z, dfa.z]
    while w:
        s = random.choice(w)
        w.remove(s)

        for char in dfa.letters:
            la = get_source_set(s, char, dfa)
            for R in p:
                r1 = la & R
                r2 = R - r1
                s3 = R - la
                if len(r1) and len(s3):
                    p.remove(R)
                    p.append(r1)
                    p.append(r2)

                    if R in w:
                        w.remove(R)
                        w.append(r1)
                        w.append(r2)
                    else:
                        if len(r1) <= len(r2):
                            w.append(r1)
                        else:
                            w.append(r2)
    return p


def get_state_located_set_flag(p: List[Set[str]], state: str):  # 获得该state所在的state_set
    for state_set in p:
        if state in state_set:
            return state_set


def get_random_state(state_set: Set[str]):
    random_num = random.randint(0, len(state_set) - 1)
    for index, state in enumerate(state_set):
        if index == random_num:
            return state


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化

    GetNewK.reset()

    m_dfa_k: Set[str] = set()
    m_dfa_s: str = ''
    m_dfa_z: Set[str] = set()
    m_dfa_letters = dfa.letters
    m_dfa_f: Dict[(str, str), str] = dict()

    p = get_final_split_set(dfa)  # 得到划分后的集合

    representative_set = set()  # 每组选取一个代表并保存在Representative_Set
    for state_set in p:
        state = get_random_state(state_set)
        representative_set.add(state)

    set2flag = dict()
    for state_set in p:  # 为划分后的内部每个集合分配一个flag并存到字典
        set2flag[tuple(state_set)] = GetNewK.get_flag()

    for flag in set2flag.values():  # 将所有flag添加到m_dfa_k中获得m_dfa_k
        m_dfa_k.add(flag)
    for state in dfa.k:
        if state in dfa.s:
            m_dfa_s = set2flag[tuple(get_state_located_set_flag(p, state))]
        if state in dfa.z:
            if (set2flag[tuple(get_state_located_set_flag(p, state))]) not in m_dfa_z:
                m_dfa_z.add(set2flag[tuple(get_state_located_set_flag(p, state))])

    for state in representative_set:  # 遍历代表集合以获得m_dfa_f
        for letter in dfa.letters:
            if (state, letter) in dfa.f.keys() and m_dfa_f.get(
                    (set2flag[tuple(get_state_located_set_flag(p, state))], letter), '#') == '#':
                m_dfa_f[(set2flag[tuple(get_state_located_set_flag(p, state))], letter)] = set2flag[
                    tuple(get_state_located_set_flag(p, dfa.f.get((state, letter))))]

    return DFA(m_dfa_k, m_dfa_letters, m_dfa_f, m_dfa_s, m_dfa_z)


def get_dfa_c_minus() -> DFA:  # 获得 c-- 确定化的DFA
    return fa_2_dfa(get_fa_c_minus())


def get_dfa_minimize_c_minus(if_read_file=False) -> DFA:
    """
    ifReadFile: 是否从文件中读入 c--的dfa
    获得c--的 最小化 dfa
    """
    lexical_result_path = os.path.join('result', 'lexical')
    dfa: DFA
    if if_read_file:
        with open(os.path.join(lexical_result_path, "dfa.pkl"), 'rb') as file:
            dfa = pickle.loads(file.read())
        with open(os.path.join(lexical_result_path, "dfa.txt"), 'w+') as file:
            file.write(str(dfa))
    else:
        dfa = dfa_minimize(fa_2_dfa(get_fa_c_minus()))
        output_hal = open(os.path.join(lexical_result_path, "dfa.pkl"), 'wb')
        str_dfa = pickle.dumps(dfa)
        output_hal.write(str_dfa)
        output_hal.close()

    return dfa
