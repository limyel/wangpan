def typeSupplement(data: str)-> str:
    # 对不够长对内容进行填充，type: 20，content: 1368
    length = 20
    new_data = data + ' ' * (length - len(data))
    return new_data


def contentSupplement(data: str)-> str:
    length = 1368
    new_data = data + ' ' * (length - len(data))
    return new_data


def noSupplement(data: int)-> str:
    length = 30
    # -1 表示不需要用到该参数
    if data == -1:
        data = ''
    else:
        data = str(data)
    new_data = data + ' ' * (length - len(data))
    return new_data