from src.game.grid.cell import Cell

class BarrierCell(Cell):
    def __init__(self, x, y, sign, active=False):
        super().__init__(x, y)
        self.barrier = []
        self.sign = sign
        self.active = active

    def set_active(self, active):
        self.active = active




