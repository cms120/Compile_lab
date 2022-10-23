from collections import deque

from src.lexical.regex import get_re_postfix_c_minus
from src.lexical.state import State


class Rules:

    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    def __str__(self):
        return 'Rules:{start:\t' + str(self.start) + '\n' + \
               'end:\t' + str(self.end) + '}\n'

    @staticmethod
    def __epsilon_transition(pre: State, nxt: State):  # 创建 epsilon transition
        pre.epsilonTransitions.append(nxt)

    @staticmethod
    def __letter_transition(pre_state: State, next_state: State, letter: str):  # 创建 普通 transition
        pre_state.transitions[letter] = next_state

    @staticmethod
    def __epsilon_rules() -> tuple[State, State]:  # 创建 epsilon 规则
        start = State(False)
        end = State(True)
        Rules.__epsilon_transition(start, end)

        return start, end

    @staticmethod
    def __letter_rules(letter) -> tuple[State, State]:  # 创建普通规则
        start = State(False)
        end = State(True)
        Rules.__letter_transition(start, end, letter)

        return start, end

    @staticmethod
    def get_epsilon_rules():
        start, end = Rules.__epsilon_rules()
        return Rules(start, end)

    @staticmethod
    def get_single_letters_rules(letter):
        start, end = Rules.__letter_rules(letter)
        return Rules(start, end)

    @staticmethod
    def get_concat_rules(pre_rules, next_rules):
        Rules.__epsilon_transition(pre_rules.end, next_rules.start)
        pre_rules.end.is_end = False

        return Rules(pre_rules.start, next_rules.end)

    @staticmethod
    def get_union_rules(pre_rules, next_rules):

        start = State(False)
        Rules.__epsilon_transition(start, pre_rules.start)
        Rules.__epsilon_transition(start, next_rules.start)

        end = State(True)
        Rules.__epsilon_transition(pre_rules.end, end)
        pre_rules.end.is_end = False
        Rules.__epsilon_transition(next_rules.end, end)
        next_rules.end.is_end = False

        return Rules(start, end)

    @staticmethod
    def closure(rules):
        start = State(False)
        end = State(True)

        Rules.__epsilon_transition(start, end)
        Rules.__epsilon_transition(start, rules.start)

        Rules.__epsilon_transition(rules.end, end)
        Rules.__epsilon_transition(rules.end, rules.start)

        rules.end.is_end = False

        return Rules(start, end)

    @staticmethod
    def init_by_re_postfix(re_postfix):
        State.reset()
        if re_postfix == '':
            return Rules.get_epsilon_rules()  # fa 的转换函数
        stack = deque()
        for i in range(len(re_postfix)):
            if re_postfix[i] == '.':
                rules_nxt = stack.pop()
                rules_pre = stack.pop()
                new_rules = Rules.get_concat_rules(rules_pre, rules_nxt)
                stack.append(new_rules)
            elif re_postfix[i] == '|':
                rules_nxt = stack.pop()
                rules_pre = stack.pop()
                new_rules = Rules.get_union_rules(rules_pre, rules_nxt)
                stack.append(new_rules)
            elif re_postfix[i] == '*':
                rules = stack.pop()
                new_rules = Rules.closure(rules)
                stack.append(new_rules)
            elif re_postfix[i] == '\\':
                rules = Rules.get_single_letters_rules(re_postfix[i+1])
                stack.append(rules)
                continue
            else:
                rules = Rules.get_single_letters_rules(re_postfix[i])
                stack.append(rules)
        return stack.pop()


def get_rules_c_minus() -> Rules:  # 获得c--的rules
    return Rules.init_by_re_postfix(get_re_postfix_c_minus())
