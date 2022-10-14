import string


class FA:
    def __init__(self, k: list[str], letters: list[str], f: [tuple[tuple[str, str], list[str]]], s: str, z: list[str]):
        self.k = k  # 状态集
        self.letters = letters  # 字母表
        self.f = f  # 转换函数集 示例 f(S,0)={V,Q} 那么在list中存入的是 ( (S,0) , [V,Q] )
        self.s = s  # 唯一初态
        self.z = z  # 终态集

    def __str__(self):
        return 'k:\t' + str(self.k) + '\n' + \
               'letters:\t' + str(self.letters) + '\n' + \
               'f:\t' + str(self.f) + '\n' + \
               's:\t' + str(self.s) + '\n' + \
               'z:\t' + str(self.z) + '\n'

    def k_and_letters(self) -> bool:  # 检查初态 终态 和转换函数中的状态及输入字符是否在状态集和字符集中
        for z in self.z:
            if z not in self.k:
                return False
        if self.s not in self.k:
            return False

        for f in self.f:
            if f[0][0] not in self.k or f[0][1] not in self.letters:
                return False
            for k in f[1]:
                if k not in self.k:
                    return False
        return True


def get_fa_c_minus() -> FA:  # 获得c--的fa 手动构造
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
