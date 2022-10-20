from copy import deepcopy

from lexical import token
from src.lexical.deterministic_finite_automation import DFA


class LexicalAnaLysis:
    @staticmethod
    def Split_text2str(text: str) -> list[str]:  # TODO 根据某种规则将文本分割成字符串数组 好像不用实现了
        pass

    def __init__(self, dfa: DFA, filepath: str):
        self.dfa = dfa
        self.result = self.analysis(filepath)

    def process_present_Split_str(self, Split_str: str) -> list[token]:
        res = []
        Pre = Next = 0  # 指针指向当前识别单词首位和正在识别的位置
        now_state = self.dfa.s
        while Pre != len(Split_str):
            while self.dfa.f.get((now_state, Split_str[Next]), 0):
                if Next == len(Split_str):
                    break
                now_state = self.dfa.f.get((now_state, Split_str[Next]))
                Next += 1
            if now_state in self.dfa.z:  # 一次识别终止 停止在终态
                res.append(token(deepcopy(Split_str[Pre:Next+(Next == len(Split_str))]))) #莫名bug
                Pre = Next
                now_state = self.dfa.s
            else:   # TODO 识别失败应该抛出异常那种或者直接停止执行 未实现
                print("未能识别成功，可能出现无法识别的符号")
                break
        return res

    def analysis(self, filepath: str) -> list[token]:  # TODO 根据dfa扫描并且得到输出 set result
        res = []
        with open('filepath', 'r') as f:  # 读入待处理文本
            text = f.read()
        # textArray = LexicalAnaLysis.Split_text2str(text)  #之前的想法 将文本分割处理
        # for i in range(len(textArray)):
        #     for j in range(len(self.process_present_Split_str(textArray[i]))):  # 调用两次处理函数 可优化
        #         res.append(deepcopy(self.process_present_Split_str()[j]))
        for i in range(len(self.process_present_Split_str(text))):  # 调用两次处理函数 可优化
            res.append(deepcopy(self.process_present_Split_str(text)[i]))
        return res
