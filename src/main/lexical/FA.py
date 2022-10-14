import string


class FA:
    def __init__(self, k: list[int], letters: list[str], f: [[str]], s: int, z: int):
        self.k = k  # 状态集
        self.letters = letters  # 字母表
        self.f = f  # 转换函数
        self.s = s  # 唯一初态
        self.z = z  # 终态集

    def __str__(self):
        return 'k:\t' + str(self.k) + '\n' + \
               'letters:\t' + str(self.letters) + '\n' + \
               'f:\t' + str(self.f) + '\n' + \
               's:\t' + str(self.s) + '\n' + \
               'z:\t' + str(self.z) + '\n'


def get_fa_c_minus() -> FA:
    return FA(k=None,
              letters=get_fa_c_minus_letters(),
              f=None,
              s=None,
              z=None)


def get_fa_c_minus_letters() -> list[str]:
    letters = ['+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|',  # 运算符
               '(', ')', '{', '}', ',', ';', '_', ]  # 界符

    for letter in string.ascii_lowercase:
        letters.append(letter)
    for letter in string.ascii_uppercase:
        letters.append(letter)
    for i in range(10):
        letters.append(str(i))

    return letters
