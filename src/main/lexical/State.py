class State:
    FLAG = -1

    def __init__(self, is_end: bool):
        self.is_end = is_end  # isEnd is bool
        self.start_flag = State.get_flag()
        self.end_flag = State.get_flag()
        self.transition = {}
        self.epsilonTransitions = []

    @staticmethod
    def get_flag():
        State.FLAG += 1
        return State.FLAG
