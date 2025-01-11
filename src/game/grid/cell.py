class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sign = "."

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_sign(self, sign):
        self.sign = sign