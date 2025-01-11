from src.game.grid.cell import Cell

class PlayerCell(Cell):
    def __init__(self, id, x, y):
        super().__init__(x, y)
        self.id = id
        self.sign = str(self.id)

