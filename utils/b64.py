import base64


def b64en(data: bytes)-> str:
    return base64.b64encode(data).decode('utf-8')


def b64de(data: str)-> bytes:
    return base64.b64decode(data.encode('utf-8'))
