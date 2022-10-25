from collections import deque
from typing import Set, Dict, Deque

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


def get_k_closure(k: str, fa: FA) -> tuple[str]:
    """
    获得一个旧的状态的关于一个字符的闭包
    k : 状态
    letter_in : 如果是一个输入字符 就将其加上 $

    """

    k_dead = set()  # 存储已访问过的状态
    k_live_stack: Deque[str] = deque(k)  # 存储待访问的状态
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


def get_k_letter_closure(k: str, fa: FA, letter) -> tuple[str]:
    """
    获取状态的闭包
    """
    epsilon_closure = set(get_k_closure(k, fa))  # 先获取epsilon闭包

    res = set()
    for k_new in epsilon_closure:
        ks_new = fa.f.get((k_new, letter))
        if ks_new is None:
            continue
        for k_new_new in ks_new:
            res.add(k_new_new)

    if len(res) == 0:
        return tuple()
    return tuple(res)


def get_ks_letter_closure(ks: set[str], fa, letter) -> tuple[str]:
    assert letter != '$'
    res = set()

    for k in ks:
        for k_new in get_k_letter_closure(k, fa, letter):
            res.add(k_new)

    return tuple(res)


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    GetNewK.reset()
    fa_s_epsilon_closure = get_k_closure(fa.s, fa)  # 获得fa.s 的epsilon闭包

    dfa_k_stack: Deque[Set[str]] = deque()
    dfa_k_stack.append(fa_s_epsilon_closure)

    dfa_letters = fa.letters

    if '$' in dfa_letters:
        dfa_letters.remove('$')  # dfa中不含 epsilon

    dfa_k_dict = dict()  # 存储dfa.k 的转化
    dfa_k_dict[fa_s_epsilon_closure] = GetNewK.get_flag()

    dfa_k_dead = set()  # 存储已访问过的 dfa.k

    dfa_f: Dict[(str, str), str] = dict()

    dfa_z = set()
    while len(dfa_k_stack) != 0:
        dfa_k_now = dfa_k_stack.pop()
        dfa_k_dead.add(dfa_k_now)

        z_flag = True  # 是否为终态
        for letter in fa.letters:
            dfa_k_new = get_ks_letter_closure(dfa_k_now, fa, letter)
            if len(dfa_k_new) == 0:
                continue
            else:
                z_flag = False

            if dfa_k_new not in dfa_k_dead:  # 这个状态未被访问过
                dfa_k_stack.append(dfa_k_new)

            if dfa_k_new not in dfa_k_dict.keys():  # 这个状态还没有转化
                dfa_k_dict[dfa_k_new] = GetNewK.get_flag()

            dfa_f[(dfa_k_dict[dfa_k_now], letter)] = dfa_k_dict[dfa_k_new]

        if z_flag:
            dfa_z.add(dfa_k_dict[dfa_k_now])

    return DFA(set(dfa_k_dict.values()), dfa_letters, dfa_f, dfa_k_dict[fa_s_epsilon_closure], dfa_z)


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化
    pass


def get_dfa_c_minus() -> DFA:  # 获得 c-- 确定化的DFA
    return fa_2_dfa(get_fa_c_minus())


def get_dfa_minimize_c_minus() -> DFA:  # 获得c--的 最小化 dfa
    return dfa_minimize(fa_2_dfa(get_fa_c_minus()))
