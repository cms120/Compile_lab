class State:
    __FLAG = -100  # 每增加一个state +1 标记state -100值无意义

    def __init__(self, is_end):
        self.is_end = is_end
        self.flag = State.get_flag()  # 状态转换图 标号
        self.transition = {}
        self.epsilonTransitions = []
        State.flag_plus()

    @classmethod
    def get_flag(cls) -> int:
        return cls.__FLAG

    @classmethod
    def flag_plus(cls):
        cls.__FLAG += 1

    @classmethod
    def reset_flag(cls):
        cls.__FLAG = 0
