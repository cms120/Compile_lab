class State:
    __FLAG = ''  # 每增加一个state +1 标记state -100值无意义
    __STATE_ALL = set()

    def __init__(self, is_end: bool):
        self.is_end = is_end
        self.flag = State.get_flag()  # 状态转换图 标号
        self.transitions = {}
        self.epsilonTransitions = []
        State.__STATE_ALL.add(self)
        State.flag_plus()

    def __hash__(self):
        return hash(self.flag)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.flag == other.flag
        return False

    def __str__(self):

        res = 'State:{'
        if self.is_end:
            res += 'end,'
        res += 'flag: ' + self.flag + ' '

        if len(self.transitions) != 0:
            res += 'transition:\t{ '
            for k, v in self.transitions.items():
                res += '(' + str(k) + ',' + v.flag + ') '
            res += '}\n'

        if len(self.epsilonTransitions) != 0:
            res += 'epsilon:\t[ '
            for state in self.epsilonTransitions:
                res += state.flag + ' '
            res += ']'
        res += '}\n'

        return res

    @classmethod
    def get_state_all(cls):
        return cls.__STATE_ALL

    @classmethod
    def get_flag(cls) -> str:
        return cls.__FLAG

    @classmethod
    def flag_plus(cls):
        cls.__FLAG = str(int(cls.__FLAG) + 1)

    @classmethod
    def reset(cls):
        cls.__STATE_ALL.clear()
        cls.__FLAG = '0'
