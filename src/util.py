from typing import List


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


def check_set_if_exist(set1: set, items: set):
    """
    查看set1中是否含有至少一个item
    """
    for item in items:
        if item in set1:
            return True
    return False

def spilt_list(l:List[str],ch:str)->List[List[str]]:
    """
    以ch来分割list
    """
    pass