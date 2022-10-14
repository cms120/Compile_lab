class FA:
    def __init__(self, k: list[int], letters: list[str], f: [[str]], s: int, z: int):
        self.k = k  # 状态集
        self.letters = letters  # 字母表
        self.f = f  # 转换函数
        self.s = s  # 唯一初态
        self.z = z  # 终态集
