import hashlib


def fileMd5(fileName: str)-> str:
    with open(fileName, 'rb') as f:
        data = hashlib.md5()
        for i in f.readlines():
            data.update(i)
        return data.hexdigest()


def bytesMd5(message: bytes):
    return hashlib.md5(message).hexdigest()