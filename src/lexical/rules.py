from src.lexical.state import State


class Rules:

    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    def __str__(self):
        return 'state0:\t' + str(self.start.flag) + '\n' + \
               'state1:\t' + str(self.end.flag) + '\n'

    @staticmethod
    def epsilon_transition(pre: State, nxt: State):  # 创建 epsilon transition
        pre.epsilonTransitions.append(nxt)

    @staticmethod
    def letter_transition(pre_state: State, next_state: State, letter: str):  # 创建 普通 transition
        pre_state.transition[letter] = next_state

    @staticmethod
    def epsilon_rules() -> tuple[State, State]:  # 创建 epsilon 规则
        start = State(False)
        end = State(True)
        Rules.epsilon_transition(start, end)

        return start, end

    @staticmethod
    def letter_rules(letter) -> tuple[State, State]:  # 创建普通规则
        start = State(False)
        end = State(True)
        Rules.letter_transition(start, end, letter)

        return start, end

    @staticmethod
    def get_epsilon_rules():
        start, end = Rules.epsilon_rules()
        return Rules(start, end)

    @staticmethod
    def get_single_letters_rules(letter):
        start, end = Rules.letter_rules(letter)
        return Rules(start, end)

    @staticmethod
    def get_concat_rules(pre_rules, next_rules):
        Rules.epsilon_transition(pre_rules.end, next_rules.start)
        pre_rules.end.is_end = False

        return Rules(pre_rules.start, next_rules.end)

    @staticmethod
    def get_union_rules(pre_rules, next_rules):
        start = State(False)
        Rules.epsilon_transition(start, pre_rules.start)
        Rules.epsilon_transition(start, next_rules.start)

        end = State(True)
        Rules.epsilon_transition(pre_rules.end, end)
        pre_rules.end.is_end = False
        Rules.epsilon_transition(next_rules.end, end)
        next_rules.end.is_end = False

        return Rules(start, end)

    @staticmethod
    def closure(rules):
        start = State(False)
        end = State(True)

        Rules.epsilon_transition(start, end)
        Rules.epsilon_transition(start, rules.start)

        Rules.epsilon_transition(rules.end, end)
        Rules.epsilon_transition(rules.end, rules.start)

        rules.end.is_end = False

        return Rules(start, end)
