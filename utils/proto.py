# 协议对拼装、拆解


items = ['type', 'md5', 'content']


def makeProto(*data)-> bytes:
    new_data = '@'.join(data)
    return new_data.encode('utf-8')


def unmakeProto(proto: bytes)-> dict:
    proto = proto.decode('utf-8').split('@')
    data = {items[x]: proto[x].strip() for x in range(3)}
    return data