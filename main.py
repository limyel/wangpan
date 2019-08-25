from views import application
from models import models


class Main:
    def __init__(self):
        self.root = application.Root()
        self.application = application.Application(self.root, self)
        self.root.mainloop()


if __name__ == '__main__':
    main = Main()