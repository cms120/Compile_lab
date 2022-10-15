class State:
    FLAG = -1  # 每增加一个state +1 标记state

    def __init__(self, isEnd):
        self.isEnd = isEnd
        self.flag = State.get_flag()  # 状态转换图 标号
        self.transition = {}
        self.epsilonTransitions = []

    @classmethod
    def get_flag(cls) -> int:
        State.FLAG += 1
        return State.FLAG