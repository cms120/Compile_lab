from collections import deque
from typing import Set, Dict, Deque, Tuple

import util
from lexical.finite_automation import FA, get_fa_c_minus


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


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化
    pass


def get_dfa_c_minus() -> DFA:  # 获得 c-- 确定化的DFA
    return fa_2_dfa(get_fa_c_minus())


def get_dfa_minimize_c_minus() -> DFA:  # 获得c--的 最小化 dfa
    return dfa_minimize(fa_2_dfa(get_fa_c_minus()))
