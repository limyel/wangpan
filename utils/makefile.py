import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = 1024


class MakeFile:
    def __init__(self, file_name, file_size):
        self.file = open(os.path.join(BASE_DIR, 'files/{}'.format(file_name)), 'wb')
        self.file.write(b' ' * file_size)

    def addFile(self, file_no, file_content):
        self.file.seek(file_no * SIZE)
        self.file.write(file_content)

    def __del__(self):
        self.file.close()
