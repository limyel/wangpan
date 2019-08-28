from collections import UserDict
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = 1024


class OrderedDict:
    def __init__(self, filename: str, size: int):
        self.data = {}
        self.order = []
        self.file = open(os.path.join(BASE_DIR, 'files/{}'.format(filename)), 'wb')
        self.file.write(b' ' * size)

    def __getitem__(self, item: int):
        return self.data[item]

    def __setitem__(self, key: int, value: bytes):
        self.data[key] = 1
        if len(self.order) == 0:
            self.order.append(key)
            self.file.write(value)
        else:
            self.orderList(key)
            self.file.seek()

    def orderList(self, key: int):
        # 对新加入对元素进行排序，同时合并可以合并的元素
        self.order.append(key)
        self.order.sort()
        index = self.order.index(key)
        try:
            # 与后面的元素合并
            if self.order[index] + self.data[key] == self.order[index+1]:
                self.data[key] += self.data[self.order[index+1]]
                self.data.pop(self.order[index+1])
                self.order.pop(index+1)
        except Exception:
            pass
        try:
            # 与前面的元素合并
            if self.order[index] - self.data[self.order[index-1]] == self.order[index-1]:
                self.data[self.order[index-1]] += self.data[key]
                self.data.pop(key)
                self.order.pop(index)
        except Exception:
            pass

    def __del__(self):
        self.file.close()
        del self.data
        del self.order
