# 协议对拼装、拆解 1486
from . import supplement


items = ['type', 'md5', 'filemd5', 'no', 'content']


def makeProto(*data)-> bytes:
    data = list(data)
    data[0] = supplement.typeSupplement(data[0])
    data[3] = supplement.noSupplement(data[3])
    data[4] = supplement.contentSupplement(data[4])
    new_data = '@'.join(data)
    return new_data.encode('utf-8')


def unmakeProto(proto: bytes)-> dict:
    proto = proto.decode('utf-8').split('@')
    data = {items[x]: proto[x].strip() for x in range(len(proto))}
    return data