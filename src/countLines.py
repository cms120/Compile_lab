import os


def collect_files(dir_r):
    """
    在指定目录下统计所有的py文件，以列表形式返回
    """
    filelist = []
    for parent, dir_names, file_names in os.walk(dir_r):
        for filename in file_names:
            if filename.endswith('.py'):
                # 将文件名和目录名拼成绝对路径，添加到列表里
                filelist.append(os.path.join(parent, filename))
    return filelist


def calc_line_num(file):
    """
    计算单个文件内的代码行数
    """
    with open(file) as fp:
        content_list = fp.readlines()
        code_num_ = 0  # 当前文件代码行数计数变量
        blank_num_ = 0  # 当前文件空行数计数变量
        annotate_num_ = 0  # 当前文件注释行数计数变量
        for content in content_list:
            content = content.strip()
            # 统计空行
            if content == '':
                blank_num_ += 1
            # 统计注释行
            elif content.startswith('#') or content.startswith('"""'):
                annotate_num_ += 1
            # 统计代码行
            else:
                code_num_ += 1
    # 返回代码行数，空行数，注释行数
    return code_num_, blank_num_, annotate_num_


if __name__ == '__main__':
    test_dir = os.path.join('test')
    files = collect_files(os.getcwd())
    total_code_num = 0  # 统计文件代码行数计数变量
    total_blank_num = 0  # 统计文件空行数计数变量
    total_annotate_num = 0  # 统计文件注释行数计数变量
    for f in files:
        code_num, blank_num, annotate_num = calc_line_num(f)
        total_code_num += code_num
        total_blank_num += blank_num
        total_annotate_num += annotate_num

    print('代码总行数为：  %s' % total_code_num)
    print('空行总行数为：  %s' % total_blank_num)
    print('注释行总行数为： %s' % total_annotate_num)
