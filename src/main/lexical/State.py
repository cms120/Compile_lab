class State:
    FLAG = -1

    def __init__(self, isEnd):
        self.isEnd = isEnd  # isEnd is bool
        self.start_flag = State.get_flag()
        self.end_flag = State.get_flag()
        self.transition = {}
        self.epsilonTransitions = []

    @classmethod
    def get_flag(cls):
        State.FLAG += 1
        return State.FLAG

