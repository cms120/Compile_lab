from collections import deque
from typing import Dict, Set, Deque

from lexical.regex.rules import Rules, get_rules_c_minus
from lexical.regex.state import State


def print_rules(rules):
    print(rules.start.flag, rules.end.flag)


class FA:
    # epsilon 用 $ 表示
    def __init__(self, k: set[str],
                 letters: set[str],
                 f: dict[tuple[str, str], set[str]],  # 转换函数 存储start letter ends
                 s: str,
                 z: set[str]):
        self.k = k  # 状态集
        self.letters = letters  # 字母表
        self.f = f  # 转换函数集 示例 f(S,0)={V,Q} 那么在list中存入的是 ( (S,0) , [V,Q] )
        self.s = s  # 唯一初态Í
        self.z = z  # 终态集

    def __str__(self):

        return 'k:\t' + str(self.k) + '\n' + \
               'letters:\t' + str(self.letters) + '\n' + \
               'f:\t' + str(self.f) + '\n' + \
               's:\t' + str(self.s) + '\n' + \
               'z:\t' + str(self.z) + '\n'

    def k_and_letters(self) -> bool:  # 检查初态 终态 和转换函数中的状态及输入字符是否在状态集和字符集中
        for z in self.z:
            if z not in self.k:
                return False
        if self.s not in self.k:
            return False

        for f in self.f:
            if f[0][0] not in self.k or f[0][1] not in self.letters:
                return False
            for k in f[1]:
                if k not in self.k:
                    return False
        return True

    @staticmethod
    def init_by_rules(rules: Rules):  # 根据rules构造fa
        fa_f: Dict[tuple[str, str], set[str]] = dict()
        fa_k: Set[str] = set()
        fa_letters: Set[str] = set()
        fa_s: str
        fa_z: Set[str] = set()

        state_live: Deque[State] = deque()  # 需要遍历的state
        state_dead: Set[State] = set()  # 已遍历过的state

        state_live.append(rules.start)
        fa_s = rules.start.flag  # 维护fa开始字符
        while state_live:
            now = state_live.pop()
            if now in state_dead:  # live 中可能有重复 因此该state如果遍历过 跳过
                continue

            state_dead.add(now)
            fa_k.add(now.flag)  # 维护状态集

            if now.is_end:  # 是终态
                fa_z.add(now.flag)
                continue

            for state in now.epsilonTransitions:  # epsilon
                if state not in state_dead:
                    state_live.append(state)
                key = (now.flag, '$')  # key 为起始state letter

                if key not in fa_f.keys():
                    fa_f[key] = set()

                fa_f[key].add(str(state.flag))

            for letter, state in now.transitions.items():
                if state not in state_dead:
                    state_live.append(state)
                key = (now.flag, letter)  # key 为起始state letter

                if key not in fa_f.keys():
                    fa_f[key] = set()

                fa_f[key].add(str(state.flag))
                fa_letters.add(letter)  # 维护字符集

        return FA(fa_k, fa_letters, fa_f, fa_s, fa_z)


def get_fa_c_minus() -> FA:  # 获得c--的fa
    return FA.init_by_rules(get_rules_c_minus())
