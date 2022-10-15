from src.lexical.State import State


class Rules:

    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    @staticmethod
    def epsilon_transition(pre_state, next_state):
        pre_state.epsilonTransitions.append(next_state)

    @staticmethod
    def letter_transition(pre_state, next_state, letter):
        pre_state.transition[letter] = next_state

    @staticmethod
    def epsilon_rules():
        start = State(False)
        end = State(True)
        Rules.epsilon_transition(start, end)

        return start, end

    @staticmethod
    def letter_rules(letter):
        start = State(False)
        end = State(True)
        Rules.letter_transition(start, end, letter)

        return start, end

    @staticmethod
    def get_single_letters_rules(letter):
        start, end = Rules.letter_rules(letter)
        return Rules(start, end)

    @staticmethod
    def get_concat_rules(pre_rules, next_rules):
        Rules.epsilon_transition(pre_rules.end, next_rules.start)
        pre_rules.end.isEnd = False

        return Rules(pre_rules.start, next_rules.end)

    @staticmethod
    def get_union_rules(pre_rules, next_rules):
        start = State(False)
        Rules.epsilon_transition(start, pre_rules.start)
        Rules.epsilon_transition(start, next_rules.start)

        end = State(True)
        Rules.epsilon_transition(pre_rules.end, end)
        pre_rules.end.isEnd = False
        Rules.epsilon_transition(next_rules.end, end)
        next_rules.end.isEnd = False

        return Rules(start, end)

    @staticmethod
    def closure(rules):
        start = State(False)
        end = State(True)

        Rules.epsilon_transition(start, end)
        Rules.epsilon_transition(start, rules.start)

        Rules.epsilon_transition(rules.end, end)
        Rules.epsilon_transition(rules.end, rules.start)

        rules.end.isEnd = False

        return Rules(start, end)
