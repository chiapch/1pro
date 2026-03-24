from world.cell import Cell
from config import WORLD_WIDTH, WORLD_HEIGHT


class WorldGrid:
    def __init__(self) -> None:
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.cells = [
            [Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def update(self, dt: float) -> None:
        for row in self.cells:
            for cell in row:
                for layer in cell.get_layers_in_order():
                    if hasattr(layer, "update"):
                        layer.update(dt)

        snapshot = []

        for row in self.cells:
            for cell in row:
                for layer in cell.get_layers_in_order():
                    for obj in list(layer.get_objects()):
                        snapshot.append((cell.x, cell.y, layer.layer_name, obj))

        for cell_x, cell_y, layer_name, obj in snapshot:
            if hasattr(obj, "update"):
                try:
                    obj.update(dt, self, cell_x, cell_y)
                except TypeError:
                    obj.update(dt)