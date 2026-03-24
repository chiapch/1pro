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

    def collect_diagnostics(self) -> dict:
        object_type_counts: dict[str, int] = {}
        layer_counts = {
            "ground": 0,
            "surface": 0,
            "standing": 0,
            "air": 0,
        }
        non_empty_cells = 0
        total_moisture = 0.0

        for row in self.cells:
            for cell in row:
                cell_object_count = 0

                for layer in cell.get_layers_in_order():
                    objects = layer.get_objects()
                    layer_counts[layer.layer_name] += len(objects)
                    cell_object_count += len(objects)

                    for obj in objects:
                        object_type_counts[obj.object_type] = object_type_counts.get(obj.object_type, 0) + 1

                if cell_object_count > 0:
                    non_empty_cells += 1

                total_moisture += cell.ground_layer.moisture

        total_cells = self.width * self.height
        avg_moisture = total_moisture / total_cells if total_cells > 0 else 0.0
        return {
            "world_size": {"width": self.width, "height": self.height},
            "objects_total": sum(layer_counts.values()),
            "non_empty_cells": non_empty_cells,
            "avg_ground_moisture": round(avg_moisture, 6),
            "layer_object_counts": layer_counts,
            "object_type_counts": object_type_counts,
        }
