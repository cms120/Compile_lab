from typing import List


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:  # 读入待处理文本
        text = f.read()

    return text


def read_file2(file_path: str) -> List[str]:
    return open(file_path, 'r').readlines()


def check_set_if_exist(set1: set, items: set):
    """
    查看set1中是否含有至少一个item
    """
    for item in items:
        if item in set1:
            return True
    return False
