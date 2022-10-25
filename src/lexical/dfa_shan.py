from typing import Set, Dict, Tuple

from lexical.finite_automation import FA, get_fa_c_minus


class DFA(FA):

    def __init__(self, k: set[str], letters: set[str], f: dict[tuple[str, str], set[str]], s: str, z: set[str]):
        super().__init__(k, letters, f, s, z)


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    # 用造表法实现
    dfa_k: Set[str] = set()
    dfa_s: str = '1'
    dfa_z: Set[str] = fa.z
    dfa_f: Dict[Tuple[str, str], Set[str]]

    # 存储表的若干行 每一行中list左侧是新的状态 右侧是 letter和其对应的状态
    sheet = [[set[dfa_s]]]
    k_new_set: Set[Set[str]] = set(sheet[0][0])

    i = 0
    while i < len(sheet):  # 遍历sheet每一行
        k_new = sheet[i][0]
        sheet[i][1] = fa_2_dfa_k_new_closure(k_new, fa)

        for k_new_new in sheet[i][1].values():
            if k_new_new not in k_new_set:
                k_new_set.add(k_new_new)
                sheet.append([k_new_new])
        i += 1


def get_dfa_by_sheet(sheet:list)->DFA:
    dfa_k=set()
    dfa_f=dict()
    for line in sheet :
        pass


def fa_2_dfa_k_new_closure(k_new: set[str], fa: FA) -> dict[str, set[str]]:  # 获得新状态对于所有letter的闭包
    res: Dict[str, Set[str]] = dict()

    for letter in fa.letters:  # 遍历每个字符
        k_new_closure = set()  # 新状态对于一个letter的闭包
        for k_old in k_new:  # 遍历状态集中每个状态
            for k in fa.f[(k_old, letter)]:  # 查询到的状态集
                k_new_closure.add(k)
        res[letter] = k_new_closure
    return res


def dfa_minimize(dfa: DFA) -> DFA:  # DFA最小化
    pass


def get_dfa_c_minus() -> DFA:  # 获得 c-- 确定化的DFA
    return fa_2_dfa(get_fa_c_minus())


def get_dfa_minimize_c_minus() -> DFA:  # 获得c--的 最小化 dfa
    return dfa_minimize(fa_2_dfa(get_fa_c_minus()))
