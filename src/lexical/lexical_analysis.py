from copy import deepcopy

from src.lexical.deterministic_finite_automation import DFA
from src.lexical.token import Token
from src.util import read_file


class LexicalAnaLysis:

    def __init__(self, dfa: DFA, filepath: str):
        self.dfa = dfa
        self.result = self.analysis(filepath)

    def analysis(self, file_path: str) -> list[Token]:  # TODO 根据dfa扫描并且得到输出 set result
        return self.get_token_list_by_content_dfa(self.dfa, read_file(file_path))

    @staticmethod
    def get_token_list_by_content_dfa(dfa: DFA, content: str) -> list[Token]:
        res = []
        pre = nxt = 0  # 指针指向当前识别单词首位和正在识别的位置
        now_state = dfa.s
        while pre != len(content):
            while dfa.f.get((now_state, content[nxt]), 0):
                if nxt == len(content):
                    break
                now_state = dfa.f.get((now_state, content[nxt]))
                nxt += 1
            assert now_state in dfa.z, 'error'  # TODO 输出想要的信息

            res.append(Token(deepcopy(content[pre:nxt + (nxt == len(content))])))  # 莫名bug
            pre = nxt
            now_state = dfa.s

        return res
