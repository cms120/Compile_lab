from src.main.lexical.FA import FA


class DFA(FA):

    def __init__(self, k: list[str], letters: list[str], f: list[tuple[tuple[str, str], list[str]]], s: str, z: list[str]):
        super().__init__(k, letters, f, s, z)

        dfa_min = dfa_minimize(
            fa_2_dfa(
                FA(k, letters, f, s, z)))

        self.k = dfa_min.k
        self.letters = dfa_min.letters
        self.f = dfa_min.f
        self.s = dfa_min.s
        self.z = dfa_min.z


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    pass  # TODO


def dfa_minimize(dfa) -> DFA:  # DFA最小化
    pass  # TODO
