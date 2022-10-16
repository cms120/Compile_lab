class State:
    __FLAG = -100  # 每增加一个state +1 标记state -100值无意义

    def __init__(self, is_end: bool):
        self.is_end = is_end
        self.flag = State.get_flag()  # 状态转换图 标号
        self.transition = {}
        self.epsilonTransitions = []
        State.flag_plus()

    def __str__(self):
        res = ''
        res += 'State:{is_end:\t' + str(self.is_end) + '\t' + 'flag:\t' + str(self.flag) + '\n'
        res += 'transition:\t{ '
        for k, v in self.transition.items():
            res += '(' + str(k) + ',' + str(v.flag) + ') '
        res += '}\n'
        res += 'epsilon:\t[ '
        for state in self.epsilonTransitions:
            res += str(state.flag) + ' '
        res += ']}\n'
        return res

    @classmethod
    def get_flag(cls) -> int:
        return cls.__FLAG

    @classmethod
    def flag_plus(cls):
        cls.__FLAG += 1

    @classmethod
    def reset_flag(cls):
        cls.__FLAG = 0
