def deleteLine(file, lineContent):
    '''
    :param file: 文件全局路径
    :param lineContent: 要删除行的内容
    :return:
    '''
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # print(lines)
    with open(file, "w", encoding="utf-8") as f_w:
        for line in lines:
            if lineContent in line:
                continue
            f_w.write(line)