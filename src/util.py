from typing import List


def read_file(file_path: str) -> List[str]:
    res = []
    for line in open(file_path, 'r').readlines():
        if line.endswith('\n'):
            res.append(line[:-1])
        else:
            res.append(line)
    return res


def check_set_if_exist(set1: set, items: set):
    """
    查看set1中是否含有至少一个item
    """
    for item in items:
        if item in set1:
            return True
    return False
