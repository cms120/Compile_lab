def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:  # 读入待处理文本
        text = f.read()

    return text



