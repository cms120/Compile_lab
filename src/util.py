from typing import List, Tuple


def read_file(file_path: str) -> List[str]:
    res = []
    f = open(file_path, 'r')
    for line in f.readlines():
        if line.endswith('\n'):
            res.append(line[:-1])
        else:
            res.append(line)
    f.close()
    return res


def write_file(content: str, file_name: str) -> None:
    with open(file_name, 'w') as f:
        f.write(content)


def check_set_if_exist(set1: set, items: set):
    """
    查看set1中是否含有至少一个item
    """
    for item in items:
        if item in set1:
            return True
    return False


def split_list(tuple_e: Tuple[str], ch: str = '|') -> List[Tuple[str]]:
    """
    以ch来分割list ch不能出现在开始和结尾 可以用()改变优先级
    :param tuple_e: (eqExp, relExp, |, eqExp, (, '==', |, '!=', ), relExp)
    :param ch: |

    :returns: [(eaExp, relExp), (eqExp, (, '==', |, '!=' ), relExp)]
    """
    indexes = []  # ch 的索引
    res: List[Tuple[str]] = []
    l_par = 0
    for i in range(len(tuple_e)):
        if tuple_e[i] == ch:
            if l_par == 0:  # 不在括号中
                indexes.append(i)
        if tuple_e[i] == '(':
            l_par += 1

        if tuple_e[i] == ')':
            l_par -= 1
    if len(indexes) == 0:
        res = [tuple_e]
    else:
        res.append(tuple_e[:indexes[0]])
        for i in range(len(indexes) - 1):
            res.append(tuple_e[indexes[i] + 1:indexes[i + 1]])
        res.append(tuple_e[indexes[-1] + 1:])

    return res


def tuple_str(t: tuple) -> str:
    if len(t) == 0:
        return '( )'
    res = '( '
    for s in t:
        res += str(s) + ' , '

    return res[:-3] + ' )'


def set_str(set_t: set) -> str:
    if len(set_t) == 0:
        return '{ }'
    res = '{ '
    for s in set_t:
        res += str(s) + ' , '

    return res[:-3] + ' }'
