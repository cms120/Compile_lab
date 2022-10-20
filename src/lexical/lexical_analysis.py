from copy import deepcopy

from src.lexical.deterministic_finite_automation import DFA
from src.lexical.token import Token


class LexicalAnaLysis:

    def __init__(self, dfa: DFA, filepath: str):
        self.dfa = dfa
        self.result = self.analysis(filepath)

    def get_token_by_content(self, content: str) -> list[Token]:
        res = []
        Pre = Next = 0  # 指针指向当前识别单词首位和正在识别的位置
        now_state = self.dfa.s
        while Pre != len(content):
            while self.dfa.f.get((now_state, content[Next]), 0):
                if Next == len(content):
                    break
                now_state = self.dfa.f.get((now_state, content[Next]))
                Next += 1
            if now_state in self.dfa.z:  # 一次识别终止 停止在终态
                res.append(Token(deepcopy(content[Pre:Next + (Next == len(content))])))  # 莫名bug
                Pre = Next
                now_state = self.dfa.s
            else:  # TODO 识别失败应该抛出异常那种或者直接停止执行 未实现
                print("未能识别成功，可能出现无法识别的符号")
                return []  # TODO 错误处理程序
        return res

    def analysis(self, filepath: str) -> list[Token]:  # TODO 根据dfa扫描并且得到输出 set result
        with open(filepath, 'r') as f:  # 读入待处理文本
            text = f.read()
        return self.get_token_by_content(text)
